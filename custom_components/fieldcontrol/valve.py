"""Plataforma de Válvulas para FieldControl."""

import aiohttp
from homeassistant.components.valve import ValveEntity, ValveEntityFeature
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

VALVE_COUNT = 6

async def async_setup_entry(hass, entry, async_add_entities):
    """Configura las 6 válvulas de riego como entidades nativas de Home Assistant."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    host = data["host"]

    valves = [
        FieldControlValve(coordinator, entry, host, i)
        for i in range(VALVE_COUNT)
    ]
    async_add_entities(valves)

class FieldControlValve(CoordinatorEntity, ValveEntity):
    """Representa una válvula individual de riego FieldControl."""

    _attr_reports_position = False
    _attr_supported_features = ValveEntityFeature.OPEN | ValveEntityFeature.CLOSE

    def __init__(self, coordinator, entry, host, valve_index):
        super().__init__(coordinator)
        self._entry = entry
        self._host = host
        self._valve_index = valve_index
        self._attr_name = f"FieldControl Válvula {valve_index + 1}"
        self._attr_unique_id = f"{entry.entry_id}_valve_{valve_index + 1}"
        self._attr_icon = "mdi:pipe-valve"

    @property
    def is_closed(self) -> bool:
        """Determina si la válvula está cerrada."""
        active_valve = self.coordinator.data.get("active_valve", -1)
        irrigation_active = self.coordinator.data.get("irrigation_active", False)
        return not (irrigation_active and active_valve == self._valve_index)

    async def async_open_valve(self, **kwargs) -> None:
        """Abre la válvula por la duración enviada."""
        minutes = kwargs.get("duration", 10)
        async with aiohttp.ClientSession() as session:
            await session.get(f"{self._host}/api/manual/start?v={self._valve_index}&t={minutes}")
        await self.coordinator.async_request_refresh()

    async def async_close_valve(self, **kwargs) -> None:
        """Cierra la válvula (Stop All)."""
        async with aiohttp.ClientSession() as session:
            await session.get(f"{self._host}/api/stop")
        await self.coordinator.async_request_refresh()
