from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .storage import read_status

_LOGGER = logging.getLogger(__name__)


class PhoenixDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, data_dir: str):
        super().__init__(
            hass,
            _LOGGER,
            name="Phoenix AI Trader",
            update_interval=timedelta(seconds=30),
        )
        self.data_dir = data_dir

    async def _async_update_data(self) -> dict[str, Any]:
        return await self.hass.async_add_executor_job(read_status, self.data_dir)
