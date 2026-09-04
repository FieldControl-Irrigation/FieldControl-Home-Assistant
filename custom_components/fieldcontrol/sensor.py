"""Plataforma de Sensores para FieldControl."""

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Configura las entidades de sensor."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    async_add_entities([
        FieldControlSensor(coordinator, entry, "device_id", "Device ID", "mdi:chip"),
        FieldControlSensor(coordinator, entry, "active_valve", "Válvula Activa", "mdi:pipe-valve"),
        FieldControlSensor(coordinator, entry, "remaining_sec", "Tiempo Restante", "mdi:timer-sand", "s", SensorDeviceClass.DURATION),
        FieldControlSensor(coordinator, entry, "rssi", "Señal Wi-Fi", "mdi:wifi", "dBm", SensorDeviceClass.SIGNAL_STRENGTH),
    ])

class FieldControlSensor(CoordinatorEntity, SensorEntity):
    """Representa un sensor de FieldControl."""

    def __init__(self, coordinator, entry, key, name, icon, unit=None, device_class=None):
        super().__init__(coordinator)
        self._entry = entry
        self._key = key
        self._attr_name = f"FieldControl {name}"
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class

    @property
    def native_value(self):
        val = self.coordinator.data.get(self._key)
        if self._key == "active_valve":
            return f"Válvula {val + 1}" if val is not None and val >= 0 else "Inactivo"
        return val
