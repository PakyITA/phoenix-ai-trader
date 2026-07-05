from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_DATA_DIR,
    CONF_DURATION_UNIT,
    CONF_DURATION_VALUE,
    CONF_START_CAPITAL,
    CONF_TARGET_CAPITAL,
    DEFAULT_DURATION_UNIT,
    DEFAULT_DURATION_VALUE,
    DEFAULT_START_CAPITAL,
    DEFAULT_TARGET_CAPITAL,
    DOMAIN,
    PLATFORMS,
)
from .storage import ensure_data_files


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
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
