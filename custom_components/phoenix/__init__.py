from __future__ import annotations

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from homeassistant.components import frontend
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.event import async_call_later, async_track_time_interval

from .actions import reset_mission, update_phoenix_settings
from .const import (
    CONF_ALERT_COOLDOWN_HOURS,
    CONF_ALERT_THRESHOLD_EUR,
    CONF_ALERT_THRESHOLD_PERCENT,
    CONF_DATA_DIR,
    CONF_DURATION_UNIT,
    CONF_DURATION_VALUE,
    CONF_EMAIL,
    CONF_LICENSE_KEY,
    CONF_START_CAPITAL,
    CONF_TARGET_CAPITAL,
    CONF_TELEGRAM_CHAT_ID,
    CONF_TELEGRAM_ENABLED,
    CONF_TELEGRAM_SERVICE,
    DEFAULT_ACTIVATION_CODE,
    DEFAULT_ALERT_COOLDOWN_HOURS,
    DEFAULT_ALERT_THRESHOLD_EUR,
    DEFAULT_ALERT_THRESHOLD_PERCENT,
    DEFAULT_DURATION_UNIT,
    DEFAULT_DURATION_VALUE,
    DEFAULT_EMAIL,
    DEFAULT_START_CAPITAL,
    DEFAULT_TARGET_CAPITAL,
    DEFAULT_TELEGRAM_CHAT_ID,
    DEFAULT_TELEGRAM_ENABLED,
    DEFAULT_TELEGRAM_SERVICE,
    DOMAIN,
    PLATFORMS,
)
from .storage import ensure_data_files, read_settings, read_status, update_settings
from .update_notifier import async_check_update

_LOGGER = logging.getLogger(__name__)

MISSION_UNIT_SECONDS = {
    "hours": 3600,
    "days": 86400,
    "weeks": 604800,
    "months": 2592000,
    "years": 31536000,
}


def _parse_dt(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _mission_is_active(status: dict[str, Any]) -> bool:
    if status.get("locked") or status.get("demo_expired"):
        return False

    mission = status.get("mission") if isinstance(status.get("mission"), dict) else {}
    start_date = _parse_dt(mission.get("start_date"))
    duration_value = int(mission.get("duration_value") or 0)
    duration_unit = str(mission.get("duration_unit") or "hours")
    seconds = duration_value * MISSION_UNIT_SECONDS.get(duration_unit, 0)

    if not start_date or seconds <= 0:
        return True

    return datetime.now() < start_date + timedelta(seconds=seconds)


def _payload_or_saved(payload: dict, settings: dict, key: str, default=None):
    value = payload.get(key)
    if value is None or value == "":
        return settings.get(key, default)
    return value


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    try:
        local_path = Path(__file__).parent / "www"

        try:
            from homeassistant.components.http import StaticPathConfig

            await hass.http.async_register_static_paths(
                [StaticPathConfig("/phoenix_ai_trader", str(local_path), False)]
            )
        except Exception:
            hass.http.register_static_path(
                "/phoenix_ai_trader",
                str(local_path),
                cache_headers=False,
            )

        frontend.async_register_built_in_panel(
            hass,
            component_name="custom",
            sidebar_title="Phoenix AI Trader",
            sidebar_icon="mdi:chart-line",
            frontend_url_path="phoenix-ai-trader",
            config={
                "_panel_custom": {
                    "name": "phoenix-ai-trader-panel",
                    "module_url": "/phoenix_ai_trader/phoenix-panel.js?v=053",
                    "embed_iframe": False,
                    "trust_external_script": True,
                }
            },
            require_admin=False,
        )

    except Exception:
        _LOGGER.exception("Unable to register Phoenix AI Trader sidebar panel")

    return True


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = dict(entry.data or {})
    options = dict(entry.options or {})

    data.setdefault(CONF_START_CAPITAL, DEFAULT_START_CAPITAL)
    data.setdefault(CONF_TARGET_CAPITAL, DEFAULT_TARGET_CAPITAL)
    data.setdefault(CONF_DURATION_VALUE, DEFAULT_DURATION_VALUE)
    data.setdefault(CONF_DURATION_UNIT, DEFAULT_DURATION_UNIT)
    data.setdefault(CONF_EMAIL, DEFAULT_EMAIL)
    data.setdefault(CONF_LICENSE_KEY, DEFAULT_ACTIVATION_CODE)
    data.setdefault(CONF_TELEGRAM_ENABLED, DEFAULT_TELEGRAM_ENABLED)
    data.setdefault(CONF_TELEGRAM_SERVICE, DEFAULT_TELEGRAM_SERVICE)
    data.setdefault(CONF_TELEGRAM_CHAT_ID, DEFAULT_TELEGRAM_CHAT_ID)
    data.setdefault(CONF_ALERT_THRESHOLD_EUR, DEFAULT_ALERT_THRESHOLD_EUR)
    data.setdefault(CONF_ALERT_THRESHOLD_PERCENT, DEFAULT_ALERT_THRESHOLD_PERCENT)
    data.setdefault(CONF_ALERT_COOLDOWN_HOURS, DEFAULT_ALERT_COOLDOWN_HOURS)

    hass.config_entries.async_update_entry(
        entry,
        data=data,
        options=options,
        version=11,
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    config = {**entry.data, **entry.options}
    data_dir = entry.data[CONF_DATA_DIR]

    await hass.async_add_executor_job(
        ensure_data_files,
        data_dir,
        float(config.get(CONF_START_CAPITAL, DEFAULT_START_CAPITAL)),
        float(config.get(CONF_TARGET_CAPITAL, DEFAULT_TARGET_CAPITAL)),
        int(config.get(CONF_DURATION_VALUE, DEFAULT_DURATION_VALUE)),
        config.get(CONF_DURATION_UNIT, DEFAULT_DURATION_UNIT),
        config.get(CONF_EMAIL, DEFAULT_EMAIL),
        config.get(CONF_LICENSE_KEY, DEFAULT_ACTIVATION_CODE),
        bool(config.get(CONF_TELEGRAM_ENABLED, DEFAULT_TELEGRAM_ENABLED)),
        config.get(CONF_TELEGRAM_SERVICE, DEFAULT_TELEGRAM_SERVICE),
        config.get(CONF_TELEGRAM_CHAT_ID, DEFAULT_TELEGRAM_CHAT_ID),
        float(config.get(CONF_ALERT_THRESHOLD_EUR, DEFAULT_ALERT_THRESHOLD_EUR)),
        float(config.get(CONF_ALERT_THRESHOLD_PERCENT, DEFAULT_ALERT_THRESHOLD_PERCENT)),
        int(config.get(CONF_ALERT_COOLDOWN_HOURS, DEFAULT_ALERT_COOLDOWN_HOURS)),
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {**config, CONF_DATA_DIR: data_dir}

    async def _send_startup_telegram() -> None:
        try:
            status = await hass.async_add_executor_job(read_status, data_dir)
            settings = await hass.async_add_executor_job(read_settings, data_dir)

            if not settings.get(CONF_TELEGRAM_ENABLED, False):
                return
            if not _mission_is_active(status):
                return

            telegram_service = str(settings.get(CONF_TELEGRAM_SERVICE) or DEFAULT_TELEGRAM_SERVICE).strip()
            if not telegram_service or "." not in telegram_service:
                return

            domain, service = telegram_service.split(".", 1)
            equity = float(status.get("equity") or 0.0)
            balance = float(status.get("balance") or 0.0)
            open_positions = int(status.get("open_positions") or 0)
            top_pair = str(status.get("top_pair") or status.get("top_crypto") or "N/D")
            top_score = int(status.get("top_score") or 0)

            message = (
                "🦅 Phoenix AI Trader è in esecuzione\n\n"
                "Missione attiva dopo il riavvio di Home Assistant.\n"
                f"Equity: {equity:.2f} EUR\n"
                f"Liquidità: {balance:.2f} EUR\n"
                f"Posizioni aperte: {open_positions}\n"
                f"Top setup: {top_pair} ({top_score}/100)\n\n"
                "Modalità Paper Trading: nessun ordine reale eseguito."
            )

            await hass.services.async_call(
                domain,
                service,
                {"message": message},
                blocking=True,
            )
            await hass.async_add_executor_job(
                update_settings,
                data_dir,
                {
                    "last_telegram_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_telegram_status": "sent",
                    "last_telegram_context": "startup",
                    "last_telegram_error": "",
                },
            )
        except Exception as err:
            _LOGGER.exception("Unable to send Phoenix startup Telegram message")
            await hass.async_add_executor_job(
                update_settings,
                data_dir,
                {
                    "last_telegram_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_telegram_status": "failed",
                    "last_telegram_context": "startup",
                    "last_telegram_error": str(err),
                },
            )

    async def _handle_update_settings(call: ServiceCall) -> None:
        payload = dict(call.data or {})
        await hass.async_add_executor_job(update_phoenix_settings, data_dir, payload)
        saved_settings = await hass.async_add_executor_job(read_settings, data_dir)

        mapped_options = {
            CONF_START_CAPITAL: float(saved_settings.get(CONF_START_CAPITAL, DEFAULT_START_CAPITAL)),
            CONF_TARGET_CAPITAL: float(saved_settings.get(CONF_TARGET_CAPITAL, DEFAULT_TARGET_CAPITAL)),
            CONF_DURATION_VALUE: int(saved_settings.get(CONF_DURATION_VALUE, DEFAULT_DURATION_VALUE)),
            CONF_DURATION_UNIT: saved_settings.get(CONF_DURATION_UNIT, DEFAULT_DURATION_UNIT),
            CONF_EMAIL: saved_settings.get(CONF_EMAIL, DEFAULT_EMAIL),
            CONF_LICENSE_KEY: saved_settings.get("license_key", DEFAULT_ACTIVATION_CODE),
            CONF_TELEGRAM_ENABLED: bool(saved_settings.get(CONF_TELEGRAM_ENABLED, DEFAULT_TELEGRAM_ENABLED)),
            CONF_TELEGRAM_SERVICE: saved_settings.get(CONF_TELEGRAM_SERVICE, DEFAULT_TELEGRAM_SERVICE),
            CONF_TELEGRAM_CHAT_ID: saved_settings.get(CONF_TELEGRAM_CHAT_ID, DEFAULT_TELEGRAM_CHAT_ID),
            CONF_ALERT_THRESHOLD_EUR: float(saved_settings.get(CONF_ALERT_THRESHOLD_EUR, DEFAULT_ALERT_THRESHOLD_EUR)),
            CONF_ALERT_THRESHOLD_PERCENT: float(saved_settings.get(CONF_ALERT_THRESHOLD_PERCENT, DEFAULT_ALERT_THRESHOLD_PERCENT)),
            CONF_ALERT_COOLDOWN_HOURS: int(saved_settings.get(CONF_ALERT_COOLDOWN_HOURS, DEFAULT_ALERT_COOLDOWN_HOURS)),
        }

        new_options = {**entry.options, **mapped_options}
        hass.config_entries.async_update_entry(entry, options=new_options)
        hass.data[DOMAIN][entry.entry_id] = {**entry.data, **new_options, CONF_DATA_DIR: data_dir}

    async def _handle_reset_mission(call: ServiceCall) -> None:
        runtime = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})
        current_config = {**entry.data, **entry.options, **runtime}
        await hass.async_add_executor_job(reset_mission, data_dir, current_config)

    async def _handle_test_telegram(call: ServiceCall) -> None:
        payload = dict(call.data or {})
        saved_settings = await hass.async_add_executor_job(read_settings, data_dir)
        runtime = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})
        current_config = {**entry.data, **entry.options, **runtime, **saved_settings}
        telegram_service = str(
            payload.get(CONF_TELEGRAM_SERVICE)
            or current_config.get(CONF_TELEGRAM_SERVICE)
            or DEFAULT_TELEGRAM_SERVICE
        ).strip()

        if not telegram_service or "." not in telegram_service:
            raise ValueError(f"Invalid Telegram notify service: {telegram_service}")

        domain, service = telegram_service.split(".", 1)
        await hass.services.async_call(
            domain,
            service,
            {"message": "Test Telegram Passato"},
            blocking=True,
        )

    if not hass.services.has_service(DOMAIN, "update_settings"):
        hass.services.async_register(DOMAIN, "update_settings", _handle_update_settings)

    if not hass.services.has_service(DOMAIN, "reset_mission"):
        hass.services.async_register(DOMAIN, "reset_mission", _handle_reset_mission)

    if not hass.services.has_service(DOMAIN, "test_telegram"):
        hass.services.async_register(DOMAIN, "test_telegram", _handle_test_telegram)

    async def _scheduled_update_check(now=None) -> None:
        await async_check_update(hass, data_dir)

    entry.async_on_unload(
        async_track_time_interval(hass, _scheduled_update_check, timedelta(minutes=5))
    )
    entry.async_on_unload(async_call_later(hass, 25, lambda _now: hass.async_create_task(_send_startup_telegram())))
    hass.async_create_task(async_check_update(hass, data_dir, force=True))

    entry.async_on_unload(entry.add_update_listener(async_update_options))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
