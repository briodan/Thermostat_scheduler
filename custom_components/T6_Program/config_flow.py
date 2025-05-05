from datetime import time
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from homeassistant.helpers import entity_registry
from homeassistant.helpers.entity_registry import async_entries_for_domain

from .const import DOMAIN

SENSOR_DOMAIN = "sensor"

DEFAULT_TIMES = ["07:00", "11:00", "15:00", "21:00"]
DEFAULT_TEMP = 20.0
DEFAULT_TOLERANCE = 1.0


def get_temp_sensor_options(hass):
    registry = entity_registry.async_get(hass)
    sensors = async_entries_for_domain(registry, SENSOR_DOMAIN)
    return {
        e.entity_id: f"{e.name or e.entity_id}"
        for e in sensors
        if "temperature" in (e.original_device_class or "").lower()
        or "temperature" in e.entity_id.lower()
    }


class T6ProgramConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        sensors = get_temp_sensor_options(self.hass)
        sensor_selector = vol.In(sensors) if sensors else str

        default_time = lambda i: DEFAULT_TIMES[i]

        schema = {
            vol.Required("cool_tolerance", default=DEFAULT_TOLERANCE):
                vol.All(vol.Coerce(float), vol.Range(min=0.5, max=5.0)),
            vol.Required("heat_tolerance", default=DEFAULT_TOLERANCE):
                vol.All(vol.Coerce(float), vol.Range(min=0.5, max=5.0)),
        }

        for i in range(1, 5):
            schema[vol.Required(f"m_f_time_{i}", default=default_time(i - 1))] = str
            schema[vol.Required(f"s_s_time_{i}", default=default_time(i - 1))] = str
            schema[vol.Required(f"m_f_temperature_{i}", default=DEFAULT_TEMP)] = float
            schema[vol.Required(f"s_s_temperature_{i}", default=DEFAULT_TEMP)] = float
            schema[vol.Optional(f"mf_sensor_{i}", default="")] = sensor_selector
            schema[vol.Optional(f"ss_sensor_{i}", default="")] = sensor_selector

        if user_input is not None:
            return self.async_create_entry(title="T6_Program", data=user_input)

        return self.async_show_form(step_id="user", data_schema=vol.Schema(schema))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        from .options import T6ProgramOptionsFlowHandler
        return T6ProgramOptionsFlowHandler(config_entry)
