from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components import persistent_notification
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .storage import PHOENIX_VERSION, read_settings, update_settings

_LOGGER = logging.getLogger(__name__)

GITHUB_MANIFEST_URL = "https://raw.githubusercontent.com/PakyITA/phoenix-ai-trader/main/custom_components/phoenix/manifest.json"
CHECK_INTERVAL = timedelta(minutes=5)


def _now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _version_tuple(value: str | None) -> tuple[int, ...]:
    numbers: list[int] = []
    for part in str(value or "0").split("."):
        clean = "".join(ch for ch in part if ch.isdigit())
        numbers.append(int(clean or 0))
    return tuple(numbers)


async def async_check_update(hass: HomeAssistant, data_dir: str, *, force: bool = False) -> None:
    settings = await hass.async_add_executor_job(read_settings, data_dir)

    if not force:
        last_check = _parse_dt(settings.get("update_last_check_at"))
        if last_check and datetime.now() - last_check < CHECK_INTERVAL:
            return

    try:
        session = async_get_clientsession(hass)
        async with session.get(GITHUB_MANIFEST_URL, timeout=10) as response:
            if response.status != 200:
                _LOGGER.debug("Phoenix update check returned HTTP %s", response.status)
                return
            manifest: dict[str, Any] = json.loads(await response.text())
    except Exception:
        _LOGGER.debug("Unable to check Phoenix update", exc_info=True)
        return

    latest_version = str(manifest.get("version") or "").strip()
    current_version = PHOENIX_VERSION
    update_available = bool(latest_version) and _version_tuple(latest_version) > _version_tuple(current_version)

    await hass.async_add_executor_job(
        update_settings,
        data_dir,
        {
            "update_last_check_at": _now_string(),
            "update_latest_version": latest_version,
            "update_current_version": current_version,
            "update_available": update_available,
        },
    )

    if not update_available:
        return

    if settings.get("update_notice_version") == latest_version:
        return

    persistent_notification.async_create(
        hass,
        f"Nuova versione disponibile: {latest_version}. Versione installata: {current_version}. Aggiorna Phoenix da HACS o da GitHub.",
        title="Phoenix AI Trader - Aggiornamento disponibile",
        notification_id="phoenix_update_available",
    )

    await hass.async_add_executor_job(
        update_settings,
        data_dir,
        {
            "update_notice_version": latest_version,
            "update_notice_at": _now_string(),
        },
    )
