from __future__ import annotations

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .actions import reset_mission
from .const import CONF_DATA_DIR, DOMAIN


class PhoenixResetMissionView(HomeAssistantView):
    url = "/api/phoenix/reset_mission"
    name = "api:phoenix:reset_mission"
    requires_auth = True

    async def post(self, request):
        hass: HomeAssistant = request.app["hass"]
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            return self.json({"ok": False, "error": "no_entry"}, status_code=404)

        entry = entries[0]
        runtime = hass.data.get(DOMAIN, {}).get(entry.entry_id, {})
        data_dir = runtime.get(CONF_DATA_DIR) or entry.data.get(CONF_DATA_DIR)
        if not data_dir:
            return self.json({"ok": False, "error": "no_data_dir"}, status_code=400)

        status = await hass.async_add_executor_job(reset_mission, data_dir)
        return self.json({"ok": True, "status": status})
