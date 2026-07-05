from __future__ import annotations

import json
import os
from datetime import datetime

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_DATA_DIR,
    CONF_START_CAPITAL,
    CONF_TARGET_CAPITAL,
    CONF_DURATION_VALUE,
    CONF_DURATION_UNIT,
    DEFAULT_DATA_DIR,
    DEFAULT_START_CAPITAL,
    DEFAULT_TARGET_CAPITAL,
    DEFAULT_DURATION_VALUE,
    DEFAULT_DURATION_UNIT,
    STATUS_FILENAME,
    SETTINGS_FILENAME,
    HISTORY_FILENAME,
    TRADES_FILENAME,
)


DURATION_UNITS = {
    "hours": "Ore",
    "days": "Giorni",
    "weeks": "Settimane",
    "months": "Mesi",
    "years": "Anni",
}


def create_default_files(
    data_dir: str,
    start_capital: float,
    target_capital: float,
    duration_value: int,
    duration_unit: str,
) -> None:
    os.makedirs(data_dir, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    settings = {
        "paper_trading": True,
        "start_capital": start_capital,
        "target_capital": target_capital,
        "duration_value": duration_value,
        "duration_unit": duration_unit,
        "created_at": now,
        "currency": "€",
    }

    status = {
        "online": False,
        "version": "0.2.0",
        "paper_trading": True,
        "last_update": now,
        "scanned_count": 0,
        "start_balance": start_capital,
        "balance": start_capital,
        "invested_amount": 0.0,
        "open_value": 0.0,
        "unrealized_pnl": 0.0,
        "unrealized_pnl_percent": 0.0,
        "equity": start_capital,
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
        "mission": {
            "start_capital": start_capital,
            "target_capital": target_capital,
            "duration_value": duration_value,
            "duration_unit": duration_unit,
            "start_date": now,
        },
        "positions": [],
        "top20": [],
    }

    files = {
        SETTINGS_FILENAME: settings,
        STATUS_FILENAME: status,
        HISTORY_FILENAME: [],
        TRADES_FILENAME: [],
    }

    for filename, content in files.items():
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                json.dump(content, file, indent=2, ensure_ascii=False)


class PhoenixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        if user_input is not None:
            data_dir = user_input[CONF_DATA_DIR].strip()
            start_capital = float(user_input[CONF_START_CAPITAL])
            target_capital = float(user_input[CONF_TARGET_CAPITAL])
            duration_value = int(user_input[CONF_DURATION_VALUE])
            duration_unit = user_input[CONF_DURATION_UNIT]

            try:
                await self.hass.async_add_executor_job(
                    create_default_files,
                    data_dir,
                    start_capital,
                    target_capital,
                    duration_value,
                    duration_unit,
                )
            except OSError:
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
                    },
                )

        schema = vol.Schema({
            vol.Required(CONF_DATA_DIR, default=DEFAULT_DATA_DIR): str,
            vol.Required(CONF_START_CAPITAL, default=DEFAULT_START_CAPITAL): vol.Coerce(float),
            vol.Required(CONF_TARGET_CAPITAL, default=DEFAULT_TARGET_CAPITAL): vol.Coerce(float),
            vol.Required(CONF_DURATION_VALUE, default=DEFAULT_DURATION_VALUE): vol.Coerce(int),
            vol.Required(CONF_DURATION_UNIT, default=DEFAULT_DURATION_UNIT): vol.In(DURATION_UNITS),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
