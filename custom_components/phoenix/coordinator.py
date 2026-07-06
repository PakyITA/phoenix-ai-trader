from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .storage import read_settings, read_status, update_settings

_LOGGER = logging.getLogger(__name__)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class PhoenixDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, data_dir: str):
        super().__init__(
            hass,
            _LOGGER,
            name="Phoenix AI Trader",
            update_interval=timedelta(seconds=5),
        )
        self.data_dir = data_dir

    async def _async_update_data(self) -> dict[str, Any]:
        data = await self.hass.async_add_executor_job(read_status, self.data_dir)
        await self._maybe_notify_demo_end(data)
        await self._maybe_send_telegram_alert(data)
        return data

    async def _maybe_notify_demo_end(self, data: dict[str, Any]) -> None:
        if not data.get("demo_expired") and not data.get("locked"):
            return

        settings = await self.hass.async_add_executor_job(read_settings, self.data_dir)
        if settings.get("demo_end_notice_sent"):
            return

        persistent_notification.async_create(
            self.hass,
            "La prova gratuita di Phoenix AI Trader e terminata. Apri Phoenix per continuare.",
            title="Phoenix AI Trader",
            notification_id="phoenix_demo_end",
        )

        await self.hass.async_add_executor_job(
            update_settings,
            self.data_dir,
            {
                "demo_end_notice_sent": True,
                "demo_end_notice_at": _now_string(),
            },
        )

    async def _maybe_send_telegram_alert(self, data: dict[str, Any]) -> None:
        if data.get("locked") or data.get("demo_expired"):
            return

        settings = await self.hass.async_add_executor_job(read_settings, self.data_dir)
        if not settings.get("telegram_enabled", False):
            return

        service_name = str(settings.get("telegram_service", "notify.telegram")).strip()
        if not service_name or "." not in service_name:
            _LOGGER.warning("Phoenix Telegram service is invalid: %s", service_name)
            return

        pnl = float(data.get("total_profit") or 0.0)
        pnl_percent = float(data.get("total_profit_percent") or 0.0)
        threshold_eur = float(settings.get("alert_threshold_eur", 10.0) or 10.0)
        threshold_percent = float(settings.get("alert_threshold_percent", 1.0) or 1.0)

        if abs(pnl) < threshold_eur and abs(pnl_percent) < threshold_percent:
            return

        direction = "profit" if pnl >= 0 else "loss"
        last_direction = settings.get("last_alert_direction")
        last_alert_at = _parse_dt(settings.get("last_alert_at"))
        cooldown_hours = int(settings.get("alert_cooldown_hours", 24) or 24)

        if last_alert_at and last_direction == direction:
            if datetime.now() - last_alert_at < timedelta(hours=cooldown_hours):
                return

        domain, service = service_name.split(".", 1)
        emoji = "P" if pnl >= 0 else "L"
        verb = "guadagnando" if pnl >= 0 else "perdendo"
        sign = "+" if pnl >= 0 else ""
        equity = float(data.get("equity") or 0.0)
        balance = float(data.get("balance") or 0.0)
        invested = float(data.get("invested_amount") or 0.0)

        message = (
            f"{emoji} Phoenix AI Trader\n\n"
            f"Stai {verb} {sign}{pnl:.2f} EUR\n"
            f"Rendimento: {sign}{pnl_percent:.2f}%\n"
            f"Equity attuale: {equity:.2f} EUR\n"
            f"Liquidita: {balance:.2f} EUR\n"
            f"Investito: {invested:.2f} EUR"
        )

        try:
            await self.hass.services.async_call(
                domain,
                service,
                {"message": message},
                blocking=False,
            )
        except Exception:
            _LOGGER.exception("Unable to send Phoenix Telegram alert")
            return

        await self.hass.async_add_executor_job(
            update_settings,
            self.data_dir,
            {
                "last_alert_at": _now_string(),
                "last_alert_direction": direction,
                "last_alert_value": pnl,
            },
        )
