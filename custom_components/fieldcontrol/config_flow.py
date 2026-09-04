"""Config Flow para la integración de FieldControl en la interfaz gráfica de Home Assistant."""

import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
import aiohttp
from .const import DOMAIN, CONF_HOST

class FieldControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Maneja el formulario de configuración inicial en Home Assistant."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip().rstrip('/')
            if not host.startswith('http://') and not host.startswith('https://'):
                host = f"http://{host}"

            # Validar conexión intentando consultar /api/status
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{host}/api/status", timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            device_id = data.get("device_id", "FieldControl")
                            return self.async_create_entry(
                                title=f"FieldControl ({device_id})",
                                data={"host": host, "device_id": device_id}
                            )
                        else:
                            errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default="192.168.1.50"): cv.string,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={"docs": "Ingresa la IP local del controlador FieldControl"}
        )
