from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .storage import PHOENIX_VERSION, read_settings, read_status, update_settings

_LOGGER = logging.getLogger(__name__)

GITHUB_MANIFEST_URL = "https://raw.githubusercontent.com/PakyITA/phoenix-ai-trader/main/custom_components/phoenix/manifest.json"
UPDATE_CHECK_INTERVAL_MINUTES = 5


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _version_tuple(value: str | None) -> tuple[int, ...]:
    parts = str(value or "0").split(".")
    numbers: list[int] = []
    for part in parts:
        clean = "".join(ch for ch in part if ch.isdigit())
        numbers.append(int(clean or 0))
    return tuple(numbers)


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
        await self._maybe_notify_update_available()
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

    async def _maybe_notify_update_available(self) -> None:
        settings = await self.hass.async_add_executor_job(read_settings, self.data_dir)
        last_check = _parse_dt(settings.get("update_last_check_at"))
        if last_check and datetime.now() - last_check < timedelta(minutes=UPDATE_CHECK_INTERVAL_MINUTES):
            return

        try:
            session = async_get_clientsession(self.hass)
            async with session.get(GITHUB_MANIFEST_URL, timeout=10) as response:
                if response.status != 200:
                    _LOGGER.debug("Phoenix update check returned HTTP %s", response.status)
                    return
                payload = json.loads(await response.text())
        except Exception:
            _LOGGER.debug("Unable to check Phoenix update", exc_info=True)
            return

        await self.hass.async_add_executor_job(
            update_settings,
            self.data_dir,
            {"update_last_check_at": _now_string()},
        )

        latest_version = str(payload.get("version") or "").strip()
        if not latest_version:
            return

        current_version = PHOENIX_VERSION
        update_available = _version_tuple(latest_version) > _version_tuple(current_version)

        await self.hass.async_add_executor_job(
            update_settings,
            self.data_dir,
            {
                "update_latest_version": latest_version,
                "update_current_version": current_version,
                "update_available": update_available,
            },
        )

        if not update_available:
            return

        if settings.get("update_notice_version") == latest_version:
            return

        persistent_notification.async_create(
            self.hass,
            f"Nuova versione disponibile: {latest_version}. Versione installata: {current_version}. Aggiorna Phoenix da HACS o da GitHub.",
            title="Phoenix AI Trader - Aggiornamento disponibile",
            notification_id="phoenix_update_available",
        )

        await self.hass.async_add_executor_job(
            update_settings,
            self.data_dir,
            {
                "update_notice_version": latest_version,
                "update_notice_at": _now_string(),
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
