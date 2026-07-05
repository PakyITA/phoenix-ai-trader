from __future__ import annotations

import os
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_STATUS_PATH, DEFAULT_STATUS_PATH


class PhoenixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            status_path = user_input[CONF_STATUS_PATH]

            if not os.path.exists(status_path):
                errors["base"] = "file_not_found"
            else:
                await self.async_set_unique_id(status_path)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title="Phoenix AI Trader",
                    data={CONF_STATUS_PATH: status_path},
                )

        schema = vol.Schema({
            vol.Required(CONF_STATUS_PATH, default=DEFAULT_STATUS_PATH): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
