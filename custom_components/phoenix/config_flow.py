from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

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
    DEFAULT_DATA_DIR,
    DEFAULT_DURATION_UNIT,
    DEFAULT_DURATION_VALUE,
    DEFAULT_EMAIL,
    DEFAULT_START_CAPITAL,
    DEFAULT_TARGET_CAPITAL,
    DEFAULT_TELEGRAM_ENABLED,
    DEFAULT_TELEGRAM_SERVICE,
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


def _build_schema(defaults: dict[str, Any], *, include_data_dir: bool = True) -> vol.Schema:
    fields: dict[Any, Any] = {}

    if include_data_dir:
        fields[vol.Required(CONF_DATA_DIR, default=defaults.get(CONF_DATA_DIR, DEFAULT_DATA_DIR))] = str

    fields.update(
        {
            vol.Required(CONF_START_CAPITAL, default=defaults.get(CONF_START_CAPITAL, DEFAULT_START_CAPITAL)): vol.Coerce(float),
            vol.Required(CONF_TARGET_CAPITAL, default=defaults.get(CONF_TARGET_CAPITAL, DEFAULT_TARGET_CAPITAL)): vol.Coerce(float),
            vol.Required(CONF_DURATION_VALUE, default=defaults.get(CONF_DURATION_VALUE, DEFAULT_DURATION_VALUE)): vol.Coerce(int),
            vol.Required(CONF_DURATION_UNIT, default=defaults.get(CONF_DURATION_UNIT, DEFAULT_DURATION_UNIT)): vol.In(DURATION_UNITS),
            vol.Optional(CONF_EMAIL, default=defaults.get(CONF_EMAIL, DEFAULT_EMAIL)): str,
            vol.Optional(CONF_LICENSE_KEY, default=defaults.get(CONF_LICENSE_KEY, DEFAULT_ACTIVATION_CODE)): str,
            vol.Optional(CONF_TELEGRAM_ENABLED, default=defaults.get(CONF_TELEGRAM_ENABLED, DEFAULT_TELEGRAM_ENABLED)): bool,
            vol.Optional(CONF_TELEGRAM_SERVICE, default=defaults.get(CONF_TELEGRAM_SERVICE, DEFAULT_TELEGRAM_SERVICE)): str,
            vol.Optional(CONF_ALERT_THRESHOLD_EUR, default=defaults.get(CONF_ALERT_THRESHOLD_EUR, DEFAULT_ALERT_THRESHOLD_EUR)): vol.Coerce(float),
            vol.Optional(CONF_ALERT_THRESHOLD_PERCENT, default=defaults.get(CONF_ALERT_THRESHOLD_PERCENT, DEFAULT_ALERT_THRESHOLD_PERCENT)): vol.Coerce(float),
            vol.Optional(CONF_ALERT_COOLDOWN_HOURS, default=defaults.get(CONF_ALERT_COOLDOWN_HOURS, DEFAULT_ALERT_COOLDOWN_HOURS)): vol.Coerce(int),
        }
    )

    return vol.Schema(fields)


def _normalize_input(user_input: dict[str, Any], *, data_dir: str | None = None) -> dict[str, Any]:
    normalized = dict(user_input)

    if data_dir is not None:
        normalized[CONF_DATA_DIR] = data_dir
    else:
        normalized[CONF_DATA_DIR] = str(normalized[CONF_DATA_DIR]).strip()

    normalized[CONF_START_CAPITAL] = float(normalized[CONF_START_CAPITAL])
    normalized[CONF_TARGET_CAPITAL] = float(normalized[CONF_TARGET_CAPITAL])
    normalized[CONF_DURATION_VALUE] = int(normalized[CONF_DURATION_VALUE])
    normalized[CONF_EMAIL] = str(normalized.get(CONF_EMAIL, DEFAULT_EMAIL)).strip()
    normalized[CONF_LICENSE_KEY] = str(normalized.get(CONF_LICENSE_KEY, DEFAULT_ACTIVATION_CODE)).strip()
    normalized[CONF_TELEGRAM_ENABLED] = bool(normalized.get(CONF_TELEGRAM_ENABLED, DEFAULT_TELEGRAM_ENABLED))
    normalized[CONF_TELEGRAM_SERVICE] = str(normalized.get(CONF_TELEGRAM_SERVICE, DEFAULT_TELEGRAM_SERVICE)).strip()
    normalized[CONF_ALERT_THRESHOLD_EUR] = float(normalized.get(CONF_ALERT_THRESHOLD_EUR, DEFAULT_ALERT_THRESHOLD_EUR))
    normalized[CONF_ALERT_THRESHOLD_PERCENT] = float(normalized.get(CONF_ALERT_THRESHOLD_PERCENT, DEFAULT_ALERT_THRESHOLD_PERCENT))
    normalized[CONF_ALERT_COOLDOWN_HOURS] = int(normalized.get(CONF_ALERT_COOLDOWN_HOURS, DEFAULT_ALERT_COOLDOWN_HOURS))

    return normalized


def _validate_input(data: dict[str, Any]) -> dict[str, str]:
    errors: dict[str, str] = {}

    if not data[CONF_DATA_DIR]:
        errors[CONF_DATA_DIR] = "invalid_data_dir"

    if data[CONF_START_CAPITAL] <= 0:
        errors[CONF_START_CAPITAL] = "invalid_start_capital"

    if data[CONF_TARGET_CAPITAL] <= data[CONF_START_CAPITAL]:
        errors[CONF_TARGET_CAPITAL] = "invalid_target_capital"

    if data[CONF_DURATION_VALUE] <= 0:
        errors[CONF_DURATION_VALUE] = "invalid_duration"

    if data[CONF_TELEGRAM_ENABLED] and "." not in data[CONF_TELEGRAM_SERVICE]:
        errors[CONF_TELEGRAM_SERVICE] = "invalid_telegram_service"

    if data[CONF_ALERT_THRESHOLD_EUR] < 0:
        errors[CONF_ALERT_THRESHOLD_EUR] = "invalid_alert_threshold"

    if data[CONF_ALERT_THRESHOLD_PERCENT] < 0:
        errors[CONF_ALERT_THRESHOLD_PERCENT] = "invalid_alert_threshold"

    if data[CONF_ALERT_COOLDOWN_HOURS] < 1:
        errors[CONF_ALERT_COOLDOWN_HOURS] = "invalid_alert_cooldown"

    return errors


async def _ensure_files(hass, data: dict[str, Any]) -> None:
    await hass.async_add_executor_job(
        ensure_data_files,
        data[CONF_DATA_DIR],
        data[CONF_START_CAPITAL],
        data[CONF_TARGET_CAPITAL],
        data[CONF_DURATION_VALUE],
        data[CONF_DURATION_UNIT],
        data[CONF_EMAIL],
        data[CONF_LICENSE_KEY],
        data[CONF_TELEGRAM_ENABLED],
        data[CONF_TELEGRAM_SERVICE],
        data[CONF_ALERT_THRESHOLD_EUR],
        data[CONF_ALERT_THRESHOLD_PERCENT],
        data[CONF_ALERT_COOLDOWN_HOURS],
    )


class PhoenixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 5

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        return PhoenixOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            data = _normalize_input(user_input)
            errors = _validate_input(data)

            if not errors:
                try:
                    await _ensure_files(self.hass, data)
                except Exception:
                    _LOGGER.exception("Unable to create Phoenix AI Trader data files")
                    errors["base"] = "cannot_create_files"
                else:
                    await self.async_set_unique_id(data[CONF_DATA_DIR])
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(title="Phoenix AI Trader", data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema({}, include_data_dir=True),
            errors=errors,
        )


class PhoenixOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        errors: dict[str, str] = {}
        data_dir = self.config_entry.data[CONF_DATA_DIR]
        defaults = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            data = _normalize_input(user_input, data_dir=data_dir)
            errors = _validate_input(data)

            if not errors:
                try:
                    await _ensure_files(self.hass, data)
                except Exception:
                    _LOGGER.exception("Unable to update Phoenix AI Trader options")
                    errors["base"] = "cannot_create_files"
                else:
                    options = {key: value for key, value in data.items() if key != CONF_DATA_DIR}
                    return self.async_create_entry(title="", data=options)

        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(defaults, include_data_dir=False),
            errors=errors,
        )
