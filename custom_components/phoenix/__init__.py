from __future__ import annotations

import logging
from datetime import timedelta
from pathlib import Path

from homeassistant.components import frontend
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.event import async_track_time_interval

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
    DEFAULT_TELEGRAM_ENABLED,
    DEFAULT_TELEGRAM_SERVICE,
    DOMAIN,
    PLATFORMS,
)
from .storage import ensure_data_files
from .update_notifier import async_check_update

_LOGGER = logging.getLogger(__name__)


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
                    "module_url": "/phoenix_ai_trader/phoenix-panel.js?v=052",
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
    data.setdefault(CONF_ALERT_THRESHOLD_EUR, DEFAULT_ALERT_THRESHOLD_EUR)
    data.setdefault(CONF_ALERT_THRESHOLD_PERCENT, DEFAULT_ALERT_THRESHOLD_PERCENT)
    data.setdefault(CONF_ALERT_COOLDOWN_HOURS, DEFAULT_ALERT_COOLDOWN_HOURS)

    hass.config_entries.async_update_entry(
        entry,
        data=data,
        options=options,
        version=8,
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
        float(config.get(CONF_ALERT_THRESHOLD_EUR, DEFAULT_ALERT_THRESHOLD_EUR)),
        float(config.get(CONF_ALERT_THRESHOLD_PERCENT, DEFAULT_ALERT_THRESHOLD_PERCENT)),
        int(config.get(CONF_ALERT_COOLDOWN_HOURS, DEFAULT_ALERT_COOLDOWN_HOURS)),
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {**config, CONF_DATA_DIR: data_dir}

    async def _handle_update_settings(call: ServiceCall) -> None:
        payload = dict(call.data or {})
        await hass.async_add_executor_job(update_phoenix_settings, data_dir, payload)

        mapped_options = {
            CONF_START_CAPITAL: float(payload.get(CONF_START_CAPITAL, config.get(CONF_START_CAPITAL, DEFAULT_START_CAPITAL))),
            CONF_TARGET_CAPITAL: float(payload.get(CONF_TARGET_CAPITAL, config.get(CONF_TARGET_CAPITAL, DEFAULT_TARGET_CAPITAL))),
            CONF_DURATION_VALUE: int(payload.get(CONF_DURATION_VALUE, config.get(CONF_DURATION_VALUE, DEFAULT_DURATION_VALUE))),
            CONF_DURATION_UNIT: payload.get(CONF_DURATION_UNIT, config.get(CONF_DURATION_UNIT, DEFAULT_DURATION_UNIT)),
            CONF_EMAIL: payload.get(CONF_EMAIL, config.get(CONF_EMAIL, DEFAULT_EMAIL)),
            CONF_LICENSE_KEY: payload.get(CONF_LICENSE_KEY, config.get(CONF_LICENSE_KEY, DEFAULT_ACTIVATION_CODE)),
            CONF_TELEGRAM_ENABLED: bool(payload.get(CONF_TELEGRAM_ENABLED, config.get(CONF_TELEGRAM_ENABLED, DEFAULT_TELEGRAM_ENABLED))),
            CONF_TELEGRAM_SERVICE: payload.get(CONF_TELEGRAM_SERVICE, config.get(CONF_TELEGRAM_SERVICE, DEFAULT_TELEGRAM_SERVICE)),
            CONF_ALERT_THRESHOLD_EUR: float(payload.get(CONF_ALERT_THRESHOLD_EUR, config.get(CONF_ALERT_THRESHOLD_EUR, DEFAULT_ALERT_THRESHOLD_EUR))),
            CONF_ALERT_THRESHOLD_PERCENT: float(payload.get(CONF_ALERT_THRESHOLD_PERCENT, config.get(CONF_ALERT_THRESHOLD_PERCENT, DEFAULT_ALERT_THRESHOLD_PERCENT))),
            CONF_ALERT_COOLDOWN_HOURS: int(payload.get(CONF_ALERT_COOLDOWN_HOURS, config.get(CONF_ALERT_COOLDOWN_HOURS, DEFAULT_ALERT_COOLDOWN_HOURS))),
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
        runtime = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})
        current_config = {**entry.data, **entry.options, **runtime}
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
