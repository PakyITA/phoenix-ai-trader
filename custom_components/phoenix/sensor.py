from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_STATUS_PATH


@dataclass(frozen=True)
class PhoenixSensorDescription:
    key: str
    name: str
    unit: str | None = None
    icon: str | None = None


SENSORS = [
    PhoenixSensorDescription("equity", "Equity", "€", "mdi:cash"),
    PhoenixSensorDescription("balance", "Liquidità", "€", "mdi:wallet"),
    PhoenixSensorDescription("invested_amount", "Investito", "€", "mdi:briefcase"),
    PhoenixSensorDescription("open_value", "Valore Posizioni", "€", "mdi:package-variant"),
    PhoenixSensorDescription("unrealized_pnl", "P/L Aperto", "€", "mdi:chart-line"),
    PhoenixSensorDescription("total_profit", "Profitto Totale", "€", "mdi:trending-up"),
    PhoenixSensorDescription("total_profit_percent", "Profitto Percentuale", "%", "mdi:percent"),
    PhoenixSensorDescription("win_rate", "Win Rate", "%", "mdi:target"),
    PhoenixSensorDescription("open_positions", "Trade Aperti", None, "mdi:format-list-bulleted"),
    PhoenixSensorDescription("closed_trades", "Trade Chiusi", None, "mdi:check-circle"),
    PhoenixSensorDescription("top_crypto", "Top Crypto", None, "mdi:bitcoin"),
    PhoenixSensorDescription("scanned_count", "Crypto Scansionate", None, "mdi:radar"),
    PhoenixSensorDescription("last_update", "Ultimo Aggiornamento", None, "mdi:clock"),
]


class PhoenixDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, status_path: str):
        super().__init__(
            hass,
            logger=None,
            name="Project Phoenix",
            update_interval=timedelta(seconds=30),
        )
        self.status_path = status_path

    async def _async_update_data(self) -> dict[str, Any]:
        return await self.hass.async_add_executor_job(self._read_status)

    def _read_status(self) -> dict[str, Any]:
        if not os.path.exists(self.status_path):
            return {"online": False, "error": "status.json not found"}

        with open(self.status_path, "r", encoding="utf-8") as file:
            return json.load(file)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    status_path = entry.data[CONF_STATUS_PATH]
    coordinator = PhoenixDataUpdateCoordinator(hass, status_path)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        PhoenixSensor(coordinator, description)
        for description in SENSORS
    ])


class PhoenixSensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: PhoenixDataUpdateCoordinator,
        description: PhoenixSensorDescription,
    ):
        super().__init__(coordinator)
        self.description = description
        self._attr_name = f"Phoenix {description.name}"
        self._attr_unique_id = f"phoenix_{description.key}"
        self._attr_native_unit_of_measurement = description.unit
        self._attr_icon = description.icon

    @property
    def native_value(self):
        return self.coordinator.data.get(self.description.key)

    @property
    def extra_state_attributes(self):
        return {
            "online": self.coordinator.data.get("online"),
            "version": self.coordinator.data.get("version"),
            "positions": self.coordinator.data.get("positions"),
            "top20": self.coordinator.data.get("top20"),
            "mission": self.coordinator.data.get("mission"),
        }
