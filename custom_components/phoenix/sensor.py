from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DATA_DIR, DOMAIN
from .coordinator import PhoenixDataUpdateCoordinator


ESSENTIAL_WHEN_LOCKED = {
    "license_status",
    "demo_remaining_seconds",
    "last_update",
}


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
    PhoenixSensorDescription("max_profit", "Massimo Guadagno", "€", "mdi:trophy"),
    PhoenixSensorDescription("max_loss", "Massima Perdita", "€", "mdi:chart-line-variant"),
    PhoenixSensorDescription("target_capital", "Target Capitale", "€", "mdi:flag-checkered"),
    PhoenixSensorDescription("target_distance", "Distanza Target", "€", "mdi:map-marker-distance"),
    PhoenixSensorDescription("target_progress_percent", "Progresso Target", "%", "mdi:progress-check"),
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
    config = hass.data[DOMAIN][entry.entry_id]
    data_dir = config[CONF_DATA_DIR]
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

    def _is_locked(self) -> bool:
        data = self.coordinator.data or {}
        return bool(data.get("locked") or data.get("demo_expired"))

    def _is_essential_when_locked(self) -> bool:
        return self.description.key in ESSENTIAL_WHEN_LOCKED

    @property
    def available(self) -> bool:
        if self._is_locked() and not self._is_essential_when_locked():
            return False
        return super().available

    @property
    def native_value(self):
        if self._is_locked() and not self._is_essential_when_locked():
            return None
        return (self.coordinator.data or {}).get(self.description.key)

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        base = {
            "paper_trading": data.get("paper_trading", True),
            "online": data.get("online"),
            "version": data.get("version"),
            "license_status": data.get("license_status"),
            "licensed": data.get("licensed"),
            "trial_mode": data.get("trial_mode"),
            "locked": data.get("locked"),
            "demo_expired": data.get("demo_expired"),
            "demo_expires_at": data.get("demo_expires_at"),
            "demo_remaining_seconds": data.get("demo_remaining_seconds"),
        }

        if self._is_locked():
            base["phoenix_disabled_reason"] = "demo_expired"
            return base

        return {
            **base,
            "accounting_model": data.get("accounting_model"),
            "accounting_note": data.get("accounting_note"),
            "positions": data.get("positions"),
            "top20": data.get("top20"),
            "mission": data.get("mission"),
            "metrics": data.get("metrics"),
            "raw_accounting": data.get("raw_accounting"),
            "best_trade": data.get("best_trade"),
            "worst_trade": data.get("worst_trade"),
            "max_profit": data.get("max_profit"),
            "max_loss": data.get("max_loss"),
        }
