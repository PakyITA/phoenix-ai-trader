from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DATA_DIR
from .coordinator import PhoenixDataUpdateCoordinator


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
    PhoenixSensorDescription("license_status", "Stato Licenza", None, "mdi:key-chain"),
    PhoenixSensorDescription("demo_remaining_seconds", "Secondi Demo Residui", "s", "mdi:timer-outline"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data_dir = entry.data[CONF_DATA_DIR]
    coordinator = PhoenixDataUpdateCoordinator(hass, data_dir)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [PhoenixSensor(coordinator, description) for description in SENSORS]
    )


class PhoenixSensor(CoordinatorEntity[PhoenixDataUpdateCoordinator], SensorEntity):
    def __init__(self, coordinator: PhoenixDataUpdateCoordinator, description: PhoenixSensorDescription):
        super().__init__(coordinator)
        self.description = description
        self._attr_name = f"Phoenix {description.name}"
        self._attr_unique_id = f"phoenix_{description.key}"
        self._attr_native_unit_of_measurement = description.unit
        self._attr_icon = description.icon

    @property
    def native_value(self):
        if self.coordinator.data.get("locked") and self.description.key not in {
            "license_status",
            "demo_remaining_seconds",
            "last_update",
        }:
            return None
        return self.coordinator.data.get(self.description.key)

    @property
    def extra_state_attributes(self):
        return {
            "paper_trading": self.coordinator.data.get("paper_trading", True),
            "online": self.coordinator.data.get("online"),
            "version": self.coordinator.data.get("version"),
            "commercial_mode": self.coordinator.data.get("commercial_mode"),
            "license_status": self.coordinator.data.get("license_status"),
            "licensed": self.coordinator.data.get("licensed"),
            "trial_mode": self.coordinator.data.get("trial_mode"),
            "locked": self.coordinator.data.get("locked"),
            "demo_expired": self.coordinator.data.get("demo_expired"),
            "demo_expires_at": self.coordinator.data.get("demo_expires_at"),
            "demo_remaining_seconds": self.coordinator.data.get("demo_remaining_seconds"),
            "positions": self.coordinator.data.get("positions"),
            "top20": self.coordinator.data.get("top20"),
            "mission": self.coordinator.data.get("mission"),
            "best_trade": self.coordinator.data.get("best_trade"),
            "worst_trade": self.coordinator.data.get("worst_trade"),
        }
