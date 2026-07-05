from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components import frontend
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_DATA_DIR,
    CONF_DURATION_UNIT,
    CONF_DURATION_VALUE,
    CONF_EMAIL,
    CONF_LICENSE_KEY,
    CONF_START_CAPITAL,
    CONF_TARGET_CAPITAL,
    DEFAULT_ACTIVATION_CODE,
    DEFAULT_DURATION_UNIT,
    DEFAULT_DURATION_VALUE,
    DEFAULT_EMAIL,
    DEFAULT_START_CAPITAL,
    DEFAULT_TARGET_CAPITAL,
    DOMAIN,
    PLATFORMS,
)
from .storage import ensure_data_files

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    try:
        local_path = Path(__file__).parent / "www"

        try:
            from homeassistant.components.http import StaticPathConfig

            await hass.http.async_register_static_paths(
                [
                    StaticPathConfig(
                        "/phoenix_ai_trader",
                        str(local_path),
                        False,
                    )
                ]
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
                    "module_url": "/phoenix_ai_trader/phoenix-panel.js?v=030",
                    "embed_iframe": False,
                    "trust_external_script": True,
                }
            },
            require_admin=False,
        )

    except Exception:
        _LOGGER.exception("Unable to register Phoenix AI Trader sidebar panel")

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data_dir = entry.data[CONF_DATA_DIR]

    await hass.async_add_executor_job(
        ensure_data_files,
        data_dir,
        float(entry.data.get(CONF_START_CAPITAL, DEFAULT_START_CAPITAL)),
        float(entry.data.get(CONF_TARGET_CAPITAL, DEFAULT_TARGET_CAPITAL)),
        int(entry.data.get(CONF_DURATION_VALUE, DEFAULT_DURATION_VALUE)),
        entry.data.get(CONF_DURATION_UNIT, DEFAULT_DURATION_UNIT),
        entry.data.get(CONF_EMAIL, DEFAULT_EMAIL),
        entry.data.get(CONF_LICENSE_KEY, DEFAULT_ACTIVATION_CODE),
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
