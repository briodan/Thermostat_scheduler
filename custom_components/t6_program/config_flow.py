import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.entity_registry import async_get
from .const import DOMAIN

# Default values
DEFAULT_TEMP = 20.0
DEFAULT_SENSOR = "sensor.none_found"
DEFAULT_TIME = "06:00"

# Ranges
TOLERANCE_MIN = 0.5
TOLERANCE_MAX = 5.0
M_F_TEMPERATURE_MIN = 10
M_F_TEMPERATURE_MAX = 30


class T6ProgramConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._data = {}

    async def async_step_user(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        default_sensor = list(sensors.keys())[0]

        if user_input:
            self._data.update(user_input)
            return await self.async_step_mf_config()

        schema = vol.Schema({
            vol.Required("tolerance_cool", default=1.0): vol.All(vol.Coerce(float), vol.Range(min=TOLERANCE_MIN, max=TOLERANCE_MAX)),
            vol.Required("tolerance_heat", default=1.0): vol.All(vol.Coerce(float), vol.Range(min=TOLERANCE_MIN, max=TOLERANCE_MAX)),
            vol.Required("current_sensor", default=default_sensor): vol.In(sensors),
            vol.Required("current_temperature", default=DEFAULT_TEMP): vol.All(vol.Coerce(float), vol.Range(min=M_F_TEMPERATURE_MIN, max=M_F_TEMPERATURE_MAX)),
            vol.Required("current_target_temperature", default=DEFAULT_TEMP): vol.All(vol.Coerce(float), vol.Range(min=M_F_TEMPERATURE_MIN, max=M_F_TEMPERATURE_MAX)),
            vol.Required("adjusted_cool_temperature", default=DEFAULT_TEMP): vol.All(vol.Coerce(float), vol.Range(min=M_F_TEMPERATURE_MIN, max=M_F_TEMPERATURE_MAX)),
            vol.Required("adjusted_heat_temperature", default=DEFAULT_TEMP): vol.All(vol.Coerce(float), vol.Range(min=M_F_TEMPERATURE_MIN, max=M_F_TEMPERATURE_MAX)),
            vol.Required("thermostat_state", default="idle"): vol.In(["idle", "heat", "cool"]),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_mf_config(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        default_sensor = list(sensors.keys())[0]

        if user_input:
            self._data.update(user_input)
            return await self.async_step_ss_config()

        schema = {}
        for i in range(1, 5):
            schema[vol.Required(f"m_f_time_{i}", default=DEFAULT_TIME)] = str
            schema[vol.Required(f"m_f_temperature_{i}", default=DEFAULT_TEMP)] = vol.All(
                vol.Coerce(float), vol.Range(min=M_F_TEMPERATURE_MIN, max=M_F_TEMPERATURE_MAX)
            )
            schema[vol.Required(f"m_f_sensor_{i}", default=default_sensor)] = vol.In(sensors)

        return self.async_show_form(step_id="mf_config", data_schema=vol.Schema(schema))

    async def async_step_ss_config(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        default_sensor = list(sensors.keys())[0]

        if user_input:
            self._data.update(user_input)
            return self.async_create_entry(title="T6 Program", data=self._data)

        schema = {}
        for i in range(1, 5):
            schema[vol.Required(f"s_s_time_{i}", default=DEFAULT_TIME)] = str
            schema[vol.Required(f"s_s_temperature_{i}", default=DEFAULT_TEMP)] = vol.All(
                vol.Coerce(float), vol.Range(min=M_F_TEMPERATURE_MIN, max=M_F_TEMPERATURE_MAX)
            )
            schema[vol.Required(f"s_s_sensor_{i}", default=default_sensor)] = vol.In(sensors)

        return self.async_show_form(step_id="ss_config", data_schema=vol.Schema(schema))

    async def _get_temp_sensor_options(self):
        registry = async_get(self.hass)
        sensors = {
            e.entity_id: e.name or e.entity_id
            for e in registry.entities.values()
            if e.domain == "sensor" and ("temperature" in (e.device_class or "") or "temperature" in e.entity_id)
        }
        if not sensors:
            sensors = {DEFAULT_SENSOR: "No temperature sensors found"}
        return sensors

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return T6ProgramOptionsFlowHandler(config_entry)


class T6ProgramOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
