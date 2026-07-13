from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .paper_trader import maybe_open_paper_position
from .scanner import build_crypto_scan
from .storage import PHOENIX_VERSION, read_settings, read_status, update_settings

_LOGGER = logging.getLogger(__name__)

GITHUB_MANIFEST_URL = "https://raw.githubusercontent.com/PakyITA/phoenix-ai-trader/main/custom_components/phoenix/manifest.json"
UPDATE_CHECK_INTERVAL_MINUTES = 5
SCAN_INTERVAL_SECONDS = 60
TOP_SETUP_ALERT_SCORE = 80
TOP_SETUP_ALERT_COOLDOWN_HOURS = 3
TELEGRAM_MARKDOWN_V2_RESERVED = "_*[]()~`>#+-=|{}.!"


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


def _telegram_escape(value: Any) -> str:
    text = str(value or "")
    return "".join(f"\\{char}" if char in TELEGRAM_MARKDOWN_V2_RESERVED else char for char in text)


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
        if not data.get("locked") and not data.get("demo_expired"):
            await self._maybe_run_scanner(data)
            data = await self.hass.async_add_executor_job(read_status, self.data_dir)
            await self._maybe_open_paper_position(data)
            data = await self.hass.async_add_executor_job(read_status, self.data_dir)
        await self._maybe_notify_demo_end(data)
        await self._maybe_notify_update_available()
        await self._maybe_send_top_setup_alert(data)
        await self._maybe_send_telegram_alert(data)
        return data

    async def _record_telegram_status(self, status: str, context: str, error: str | None = None) -> None:
        payload = {
            "last_telegram_at": _now_string(),
            "last_telegram_status": status,
            "last_telegram_context": context,
            "last_telegram_error": error or "",
        }
        await self.hass.async_add_executor_job(update_settings, self.data_dir, payload)

    async def _maybe_run_scanner(self, data: dict[str, Any]) -> None:
        last_scan = _parse_dt(data.get("last_scan_at"))
        if last_scan and datetime.now() - last_scan < timedelta(seconds=SCAN_INTERVAL_SECONDS):
            return

        scan_payload = build_crypto_scan(data)
        scan_payload["last_scan_at"] = _now_string()
        await self.hass.async_add_executor_job(update_settings, self.data_dir, {"last_scan_at": scan_payload["last_scan_at"]})
        from .storage import read_json, status_path, write_json

        status = await self.hass.async_add_executor_job(read_json, status_path(self.data_dir), {})
        status.update(scan_payload)
        await self.hass.async_add_executor_job(write_json, status_path(self.data_dir), status)

    async def _maybe_open_paper_position(self, data: dict[str, Any]) -> None:
        settings = await self.hass.async_add_executor_job(read_settings, self.data_dir)
        from .storage import read_json, status_path, trades_path, write_json

        status = await self.hass.async_add_executor_job(read_json, status_path(self.data_dir), {})
        updated_status, event = maybe_open_paper_position({**status, **data}, settings)
        await self.hass.async_add_executor_job(write_json, status_path(self.data_dir), updated_status)
        if event is None:
            return

        trades = await self.hass.async_add_executor_job(read_json, trades_path(self.data_dir), [])
        if not isinstance(trades, list):
            trades = []
        trades.append(event)
        await self.hass.async_add_executor_job(write_json, trades_path(self.data_dir), trades[-500:])

        message = (
            "🤖 Phoenix AI Trader\n\n"
            "Posizione virtuale aperta automaticamente\n"
            f"Coin: {event['pair']}\n"
            f"Investito: {event['amount']:.2f} EUR\n"
            f"Score: {event['score']}/100\n\n"
            "Modalità Paper Trading: nessun ordine reale eseguito."
        )
        await self._send_telegram_message(message, blocking=True, context="auto_paper_buy")

    async def _telegram_config(self) -> tuple[dict[str, Any], str, str] | None:
        settings = await self.hass.async_add_executor_job(read_settings, self.data_dir)
        if not settings.get("telegram_enabled", False):
            _LOGGER.debug("Phoenix Telegram is disabled")
            return None

        service_name = str(settings.get("telegram_service", "notify.telegram")).strip()
        if not service_name or "." not in service_name:
            _LOGGER.warning("Phoenix Telegram service is invalid: %s", service_name)
            return None

        domain, service = service_name.split(".", 1)
        return settings, domain, service

    async def _send_telegram_message(self, message: str, *, blocking: bool = True, context: str = "generic") -> bool:
        config = await self._telegram_config()
        if config is None:
            await self._record_telegram_status("disabled", context, "Telegram disabled or invalid service")
            return False

        _settings, domain, service = config
        service_data = {"message": _telegram_escape(message)}

        try:
            await self.hass.services.async_call(
                domain,
                service,
                service_data,
                blocking=blocking,
            )
        except Exception as err:
            _LOGGER.exception("Unable to send Phoenix Telegram message")
            await self._record_telegram_status("failed", context, str(err))
            return False

        await self._record_telegram_status("sent", context)
        return True

    async def _maybe_send_top_setup_alert(self, data: dict[str, Any]) -> None:
        if data.get("locked") or data.get("demo_expired"):
            return

        top20 = data.get("top20") if isinstance(data.get("top20"), list) else []
        top = top20[0] if top20 else {}
        symbol = str(top.get("symbol") or data.get("top_crypto") or "").strip()
        pair = str(top.get("pair") or data.get("top_pair") or symbol or "N/D")
        score = int(top.get("score") or data.get("top_score") or 0)
        confidence = str(top.get("confidence") or data.get("top_confidence") or "N/D")
        quality = str(top.get("quality") or data.get("top_quality") or "N/D")
        risk = str(top.get("market_risk") or data.get("market_risk") or "N/D")

        if not symbol or symbol == "N/D" or score < TOP_SETUP_ALERT_SCORE:
            return

        settings = await self.hass.async_add_executor_job(read_settings, self.data_dir)
        last_symbol = str(settings.get("last_top_setup_alert_symbol", ""))
        last_score = int(settings.get("last_top_setup_alert_score", 0) or 0)
        last_at = _parse_dt(settings.get("last_top_setup_alert_at"))

        same_or_weaker_setup = last_symbol == symbol and score <= last_score
        in_cooldown = bool(last_at and datetime.now() - last_at < timedelta(hours=TOP_SETUP_ALERT_COOLDOWN_HOURS))
        if same_or_weaker_setup and in_cooldown:
            return

        message = (
            "🔥 Phoenix AI Trader\n\n"
            "Nuovo setup interessante trovato\n"
            f"Coin: {pair}\n"
            f"Score: {score}/100\n"
            f"Confidenza: {confidence}\n"
            f"Qualità: {quality}\n"
            f"Rischio mercato: {risk}\n\n"
            "Modalità Paper Trading: nessun ordine reale eseguito."
        )

        sent = await self._send_telegram_message(message, blocking=True, context="top_setup")
        if not sent:
            return

        await self.hass.async_add_executor_job(
            update_settings,
            self.data_dir,
            {
                "last_top_setup_alert_at": _now_string(),
                "last_top_setup_alert_symbol": symbol,
                "last_top_setup_alert_score": score,
            },
        )

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

        config = await self._telegram_config()
        if config is None:
            return
        settings, _domain, _service = config

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

        sent = await self._send_telegram_message(message, blocking=True, context="pnl_alert")
        if not sent:
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
