"""Plataforma de Switches (Interruptores) para FieldControl."""

import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Configura los switches de FieldControl."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    host = data["host"]

    async_add_entities([
        FieldControlAutoSwitch(coordinator, entry, host),
        FieldControlAccessorySwitch(coordinator, entry, host),
    ])

class FieldControlAutoSwitch(CoordinatorEntity, SwitchEntity):
    """Switch para activar/desactivar el modo automático."""

    def __init__(self, coordinator, entry, host):
        super().__init__(coordinator)
        self._entry = entry
        self._host = host
        self._attr_name = "FieldControl Modo Automático"
        self._attr_unique_id = f"{entry.entry_id}_auto_mode"
        self._attr_icon = "mdi:robot-industrial"

    @property
    def is_on(self):
        return bool(self.coordinator.data.get("auto_enabled", False))

    async def async_turn_on(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"{self._host}/api/auto/play")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"{self._host}/api/auto/stop")
        await self.coordinator.async_request_refresh()

class FieldControlAccessorySwitch(CoordinatorEntity, SwitchEntity):
    """Switch para el relé accesorio / bomba."""

    def __init__(self, coordinator, entry, host):
        super().__init__(coordinator)
        self._entry = entry
        self._host = host
        self._attr_name = "FieldControl Relé Accesorio"
        self._attr_unique_id = f"{entry.entry_id}_accessory"
        self._attr_icon = "mdi:lightning-bolt-circle"

    @property
    def is_on(self):
        return bool(self.coordinator.data.get("accessory_active", False))

    async def async_turn_on(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"{self._host}/api/acc/set?s=1")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        async with aiohttp.ClientSession() as session:
            await session.get(f"{self._host}/api/acc/set?s=0")
        await self.coordinator.async_request_refresh()
