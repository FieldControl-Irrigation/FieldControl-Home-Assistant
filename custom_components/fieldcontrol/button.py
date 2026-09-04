"""Plataforma de Botones (Acciones de un toque) para FieldControl."""

import aiohttp
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Configura los botones de FieldControl."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    host = data["host"]

    async_add_entities([
        FieldControlStopButton(coordinator, entry, host),
    ])

class FieldControlStopButton(CoordinatorEntity, ButtonEntity):
    """Botón de Parada de Emergencia (Stop All)."""

    def __init__(self, coordinator, entry, host):
        super().__init__(coordinator)
        self._entry = entry
        self._host = host
        self._attr_name = "FieldControl Parada General"
        self._attr_unique_id = f"{entry.entry_id}_stop_all"
        self._attr_icon = "mdi:stop-circle"

    async def async_press(self) -> None:
        """Ejecuta la parada de emergencia."""
        async with aiohttp.ClientSession() as session:
            await session.get(f"{self._host}/api/stop")
        await self.coordinator.async_request_refresh()
