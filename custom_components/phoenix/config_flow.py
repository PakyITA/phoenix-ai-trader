from __future__ import annotations

import json
import os

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_STATUS_PATH, DEFAULT_STATUS_PATH


DEFAULT_STATUS_DATA = {
    "online": False,
    "version": "0.1.0",
    "last_update": "not available",
    "scanned_count": 0,
    "start_balance": 100.0,
    "balance": 100.0,
    "invested_amount": 0.0,
    "open_value": 0.0,
    "unrealized_pnl": 0.0,
    "unrealized_pnl_percent": 0.0,
    "equity": 100.0,
    "total_profit": 0.0,
    "total_profit_percent": 0.0,
    "closed_profit": 0.0,
    "open_positions": 0,
    "closed_trades": 0,
    "wins": 0,
    "losses": 0,
    "win_rate": 0.0,
    "top_crypto": "N/D",
    "top_score": 0,
    "top_confidence": "N/D",
    "top_quality": "N/D",
    "market_risk": "N/D",
    "last_trade": "N/D",
    "best_trade": "N/D",
    "worst_trade": "N/D",
    "positions": [],
    "top20": [],
}


def ensure_status_file(status_path: str) -> None:
    folder = os.path.dirname(status_path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(status_path):
        with open(status_path, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_STATUS_DATA, file, indent=2, ensure_ascii=False)


class PhoenixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            status_path = user_input[CONF_STATUS_PATH].strip()

            try:
                await self.hass.async_add_executor_job(
                    ensure_status_file,
                    status_path,
                )
            except OSError:
                errors["base"] = "cannot_create_file"
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
