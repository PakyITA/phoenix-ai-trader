from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DATA_DIR, DOMAIN
from .coordinator import PhoenixDataUpdateCoordinator


@dataclass(frozen=True)
class PhoenixBinarySensorDescription:
    key: str
    name: str
    icon_on: str
    icon_off: str
    value_fn: Callable[[dict], bool]


BINARY_SENSORS = [
    PhoenixBinarySensorDescription(
        key="licensed",
        name="Licenza Attiva",
        icon_on="mdi:shield-check",
        icon_off="mdi:shield-alert-outline",
        value_fn=lambda data: bool(data.get("licensed")),
    ),
    PhoenixBinarySensorDescription(
        key="trial_mode",
        name="Demo Attiva",
        icon_on="mdi:timer-sand",
        icon_off="mdi:timer-sand-complete",
        value_fn=lambda data: bool(data.get("trial_mode")) and not bool(data.get("demo_expired")),
    ),
    PhoenixBinarySensorDescription(
        key="locked",
        name="Bloccato",
        icon_on="mdi:lock-alert",
        icon_off="mdi:lock-open-check",
        value_fn=lambda data: bool(data.get("locked") or data.get("demo_expired")),
    ),
    PhoenixBinarySensorDescription(
        key="telegram_enabled",
        name="Telegram Attivo",
        icon_on="mdi:telegram",
        icon_off="mdi:telegram",
        value_fn=lambda data: bool(data.get("telegram_enabled")),
    ),
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
        [PhoenixBinarySensor(coordinator, description) for description in BINARY_SENSORS]
    )


class PhoenixBinarySensor(CoordinatorEntity[PhoenixDataUpdateCoordinator], BinarySensorEntity):
    def __init__(self, coordinator: PhoenixDataUpdateCoordinator, description: PhoenixBinarySensorDescription):
        super().__init__(coordinator)
        self.description = description
        self._attr_name = f"Phoenix {description.name}"
        self._attr_unique_id = f"phoenix_{description.key}_binary"

    @property
    def is_on(self) -> bool:
        return self.description.value_fn(self.coordinator.data or {})

    @property
    def icon(self) -> str:
        return self.description.icon_on if self.is_on else self.description.icon_off

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        return {
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
            "telegram_service": data.get("telegram_service"),
        }
