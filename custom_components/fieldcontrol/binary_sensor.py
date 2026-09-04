"""Plataforma de Sensores Binarios para FieldControl."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Configura las entidades de sensor binario."""
    coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    # Usar el coordinator del sensor
    if not coordinator:
        # Reutilizamos el coordinator que se registra
        pass

    # Los binarios se registran vía el coordinator de hass
