from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components import frontend
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    frontend.async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title="Phoenix AI Trader",
        sidebar_icon="mdi:chart-line",
        frontend_url_path="phoenix-ai-trader",
        config={
            "_panel_custom": {
                "name": "phoenix-ai-trader-panel",
                "module_url": "/phoenix_ai_trader/phoenix-panel.js",
                "embed_iframe": False,
                "trust_external_script": False,
            }
        },
        require_admin=False,
    )

    local_path = Path(__file__).parent / "www"
    hass.http.register_static_path(
        "/phoenix_ai_trader",
        str(local_path),
        cache_headers=False,
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
