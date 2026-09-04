"""Plataforma de Sensores Binarios para FieldControl."""

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Configura las entidades de sensor binario."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    async_add_entities([
        FieldControlBinarySensor(coordinator, entry, "online", "Online", "mdi:wifi-check", BinarySensorDeviceClass.CONNECTIVITY),
        FieldControlBinarySensor(coordinator, entry, "rain_sensor", "Sensor de Lluvia", "mdi:weather-pouring", BinarySensorDeviceClass.MOISTURE),
        FieldControlBinarySensor(coordinator, entry, "irrigation_active", "Riego Activo", "mdi:water-pump", None),
    ])

class FieldControlBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representa un sensor binario de FieldControl."""

    def __init__(self, coordinator, entry, key, name, icon, device_class=None):
        super().__init__(coordinator)
        self._entry = entry
        self._key = key
        self._attr_name = f"FieldControl {name}"
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_icon = icon
        self._attr_device_class = device_class

    @property
    def is_on(self):
        return bool(self.coordinator.data.get(self._key, False))
