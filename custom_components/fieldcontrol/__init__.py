"""Inicialización de la integración FieldControl en Home Assistant."""

import logging
from datetime import timedelta
import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "binary_sensor", "switch", "button"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura FieldControl desde un Config Entry."""
    host = entry.data["host"]

    async def async_update_data():
        """Obtiene el estado más reciente desde la API del ESP32."""
        try:
            async with async_timeout.timeout(4):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{host}/api/status") as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error HTTP {response.status} al consultar {host}")
                        return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error al comunicar con FieldControl en {host}: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="fieldcontrol_coordinator",
        update_method=async_update_data,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "host": host,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descarga el Config Entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
