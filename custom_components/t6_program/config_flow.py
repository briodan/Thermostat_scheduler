import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.entity_registry import async_get
from .const import DOMAIN

DEFAULT_SENSOR = "sensor.none_found"
DEFAULT_TIME = "06:00"
TOLERANCE_MIN = 0.5

class T6ProgramConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._data = {}

    async def async_step_user(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        default_sensor = list(sensors.keys())[0]

        if user_input:
            temp_min = user_input["temp_min"]
            temp_max = user_input["temp_max"]

            if not (temp_min <= user_input["temp_default"] <= temp_max):
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._build_user_schema(sensors),
                    errors={"temp_default": "default_out_of_range"}
                )

            # Store user selections
            self._data.update(user_input)

            # Automatically assign other fields
            self._data["current_temperature"] = user_input["temp_default"]
            self._data["current_target_temperature"] = user_input["temp_default"]
            self._data["adjusted_cool_temperature"] = user_input["temp_default"]
            self._data["adjusted_heat_temperature"] = user_input["temp_default"]
            self._data["thermostat_state"] = "idle"
            tolerance_max = 10.0 if user_input["temperature_unit"] == "°F" else 5.0
            self._data["tolerance_cool"] = 1.0
            self._data["tolerance_heat"] = 1.0
            self._data["tolerance_max"] = tolerance_max

            self._data["current_sensor"] = user_input["current_sensor"]

            return await self.async_step_mf_config()

        return self.async_show_form(step_id="user", data_schema=self._build_user_schema(sensors))

    def _build_user_schema(self, sensors):
        default_sensor = list(sensors.keys())[0]
        return vol.Schema({
            vol.Required("temperature_unit", default="°C"): vol.In(["°C", "°F"]),
            vol.Required("temp_min"): vol.Coerce(float),
            vol.Required("temp_max"): vol.Coerce(float),
            vol.Required("temp_default"): vol.Coerce(float),
            vol.Required("current_sensor", default=default_sensor): vol.In(sensors),
        })

    async def async_step_mf_config(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        default_sensor = list(sensors.keys())[0]

        temp_min = self._data["temp_min"]
        temp_max = self._data["temp_max"]
        temp_default = self._data["temp_default"]

        if user_input:
            self._data.update(user_input)
            return await self.async_step_ss_config()

        schema = {}
        for i in range(1, 5):
            schema[vol.Required(f"m_f_time_{i}", default=DEFAULT_TIME)] = str
            schema[vol.Required(f"m_f_temperature_{i}", default=temp_default)] = vol.All(
                vol.Coerce(float), vol.Range(min=temp_min, max=temp_max)
            )
            schema[vol.Required(f"m_f_sensor_{i}", default=default_sensor)] = vol.In(sensors)

        return self.async_show_form(step_id="mf_config", data_schema=vol.Schema(schema))

    async def async_step_ss_config(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        default_sensor = list(sensors.keys())[0]

        temp_min = self._data["temp_min"]
        temp_max = self._data["temp_max"]
        temp_default = self._data["temp_default"]

        if user_input:
            self._data.update(user_input)
            return self.async_create_entry(title="T6 Program", data=self._data)

        schema = {}
        for i in range(1, 5):
            schema[vol.Required(f"s_s_time_{i}", default=DEFAULT_TIME)] = str
            schema[vol.Required(f"s_s_temperature_{i}", default=temp_default)] = vol.All(
                vol.Coerce(float), vol.Range(min=temp_min, max=temp_max)
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
