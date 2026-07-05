from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DATA_DIR,
    CONF_DURATION_UNIT,
    CONF_DURATION_VALUE,
    CONF_EMAIL,
    CONF_LICENSE_KEY,
    CONF_START_CAPITAL,
    CONF_TARGET_CAPITAL,
    DEFAULT_ACTIVATION_CODE,
    DEFAULT_DATA_DIR,
    DEFAULT_DURATION_UNIT,
    DEFAULT_DURATION_VALUE,
    DEFAULT_EMAIL,
    DEFAULT_START_CAPITAL,
    DEFAULT_TARGET_CAPITAL,
    DOMAIN,
)
from .storage import ensure_data_files

_LOGGER = logging.getLogger(__name__)

DURATION_UNITS = {
    "hours": "Ore",
    "days": "Giorni",
    "weeks": "Settimane",
    "months": "Mesi",
    "years": "Anni",
}


class PhoenixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 3

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            data_dir = user_input[CONF_DATA_DIR].strip()
            start_capital = float(user_input[CONF_START_CAPITAL])
            target_capital = float(user_input[CONF_TARGET_CAPITAL])
            duration_value = int(user_input[CONF_DURATION_VALUE])
            duration_unit = user_input[CONF_DURATION_UNIT]
            email = user_input.get(CONF_EMAIL, "").strip()
            activation_code = user_input.get(CONF_LICENSE_KEY, "").strip()

            try:
                await self.hass.async_add_executor_job(
                    ensure_data_files,
                    data_dir,
                    start_capital,
                    target_capital,
                    duration_value,
                    duration_unit,
                    email,
                    activation_code,
                )
            except Exception:
                _LOGGER.exception("Unable to create Phoenix AI Trader data files")
                errors["base"] = "cannot_create_files"
            else:
                await self.async_set_unique_id(data_dir)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Phoenix AI Trader",
                    data={
                        CONF_DATA_DIR: data_dir,
                        CONF_START_CAPITAL: start_capital,
                        CONF_TARGET_CAPITAL: target_capital,
                        CONF_DURATION_VALUE: duration_value,
                        CONF_DURATION_UNIT: duration_unit,
                        CONF_EMAIL: email,
                        CONF_LICENSE_KEY: activation_code,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_DATA_DIR, default=DEFAULT_DATA_DIR): str,
                vol.Required(CONF_START_CAPITAL, default=DEFAULT_START_CAPITAL): vol.Coerce(float),
                vol.Required(CONF_TARGET_CAPITAL, default=DEFAULT_TARGET_CAPITAL): vol.Coerce(float),
                vol.Required(CONF_DURATION_VALUE, default=DEFAULT_DURATION_VALUE): vol.Coerce(int),
                vol.Required(CONF_DURATION_UNIT, default=DEFAULT_DURATION_UNIT): vol.In(DURATION_UNITS),
                vol.Optional(CONF_EMAIL, default=DEFAULT_EMAIL): str,
                vol.Optional(CONF_LICENSE_KEY, default=DEFAULT_ACTIVATION_CODE): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
