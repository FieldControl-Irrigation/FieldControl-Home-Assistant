"""Plataforma de Sensores para FieldControl."""

import aiohttp
import async_timeout
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=5)

async def async_setup_entry(hass, entry, async_add_entities):
    """Configura las entidades de sensor."""
    host = entry.data["host"]

    async def async_update_data():
        async with async_timeout.timeout(4):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{host}/api/status") as response:
                    return await response.json()

    coordinator = DataUpdateCoordinator(
        hass,
        logger=hass.components.sensor._LOGGER,
        name="fieldcontrol_sensor_coordinator",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        FieldControlSensor(coordinator, "device_id", "FieldControl Device ID", "mdi:chip"),
        FieldControlSensor(coordinator, "active_valve", "FieldControl Válvula Activa", "mdi:pipe-valve"),
        FieldControlSensor(coordinator, "remaining_sec", "FieldControl Tiempo Restante", "mdi:timer-sand", "s"),
        FieldControlSensor(coordinator, "rssi", "FieldControl Señal Wi-Fi", "mdi:wifi", "dBm"),
    ])

class FieldControlSensor(CoordinatorEntity, SensorEntity):
    """Representa un sensor de FieldControl."""

    def __init__(self, coordinator, key, name, icon, unit=None):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self):
        val = self.coordinator.data.get(self._key)
        if self._key == "active_valve":
            return f"Válvula {val + 1}" if val is not None and val >= 0 else "Inactivo"
        return val
