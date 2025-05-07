# config_flow.py (enhanced with descriptive pages)

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.entity_registry import async_get
from .const import DOMAIN

TIME_OPTIONS = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]
DEFAULT_TEMP = 20.0
DEFAULT_TOLERANCE = 1.0
DEFAULT_SENSOR = "sensor.none_found"

class T6ProgramConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self.data = {}

    async def async_step_user(self, user_input=None):
        sensors = await self._get_temp_sensor_options()

        if user_input:
            self.data.update(user_input)
            return await self.async_step_mf_config()

        schema = vol.Schema({
            vol.Required("tolerance_cool", default=DEFAULT_TOLERANCE): vol.All(vol.Coerce(float), vol.Range(min=0.5, max=5.0)),
            vol.Required("tolerance_heat", default=DEFAULT_TOLERANCE): vol.All(vol.Coerce(float), vol.Range(min=0.5, max=5.0)),
            vol.Required("current_sensor", default=next(iter(sensors))): vol.In(sensors),
            vol.Required("current_temperature", default=DEFAULT_TEMP): vol.All(vol.Coerce(float), vol.Range(min=10, max=30)),
            vol.Required("current_target_temperature", default=DEFAULT_TEMP): vol.All(vol.Coerce(float), vol.Range(min=10, max=30)),
            vol.Required("adjusted_cool_temperature", default=DEFAULT_TEMP): vol.All(vol.Coerce(float), vol.Range(min=10, max=30)),
            vol.Required("adjusted_heat_temperature", default=DEFAULT_TEMP): vol.All(vol.Coerce(float), vol.Range(min=10, max=30)),
            vol.Required("thermostat_state", default="idle" ): vol.In(["idle", "heat", "cool"]),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={
                "intro": "Initial configuration of the T6 program",
                "cool": "Cool Tolerance (adjusts when cooling triggers)",
                "heat": "Heat Tolerance (adjusts when heating triggers)",
                "sensor": "Sensor to use for current temperature monitoring",
                "temp": "Current room temperature",
                "target": "Desired temperature to maintain",
                "adj_cool": "Modified target temperature used for cooling decisions",
                "adj_heat": "Modified target temperature used for heating decisions",
                "state": "Thermostat operational state"
            }
        )

    async def _get_temp_sensor_options(self):
        registry = async_get(self.hass)
        return {
            e.entity_id: e.name or e.entity_id
            for e in registry.entities.values()
            if e.domain == "sensor" and (e.device_class == "temperature" or "temperature" in e.entity_id)
        } or {DEFAULT_SENSOR: "No temperature sensors found"}

    async def async_step_mf_config(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        if user_input:
            self.data.update(user_input)
            return await self.async_step_ss_config()

        schema = {}
        for i in range(1, 5):
            schema[vol.Required(f"m_f_time_{i}", default=TIME_OPTIONS[i - 1])] = vol.In(TIME_OPTIONS)
            schema[vol.Required(f"m_f_temperature_{i}", default=DEFAULT_TEMP)] = vol.All(vol.Coerce(float), vol.Range(min=10, max=30))
            schema[vol.Required(f"m_f_sensor_{i}", default=next(iter(sensors)))] = vol.In(sensors)

        return self.async_show_form(
            step_id="mf_config",
            data_schema=vol.Schema(schema),
            description_placeholders={
                "intro": "Configure Monday–Friday schedule",
                "time": "Each time defines a daily schedule trigger",
                "temp": "Target temperature to apply at that time",
                "sensor": "Sensor used for evaluating that schedule period"
            }
        )

    async def async_step_ss_config(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        if user_input:
            self.data.update(user_input)
            return self.async_create_entry(title="T6 Program", data=self.data)

        schema = {}
        for i in range(1, 5):
            schema[vol.Required(f"s_s_time_{i}", default=TIME_OPTIONS[i - 1])] = vol.In(TIME_OPTIONS)
            schema[vol.Required(f"s_s_temperature_{i}", default=DEFAULT_TEMP)] = vol.All(vol.Coerce(float), vol.Range(min=10, max=30))
            schema[vol.Required(f"s_s_sensor_{i}", default=next(iter(sensors)))] = vol.In(sensors)

        return self.async_show_form(
            step_id="ss_config",
            data_schema=vol.Schema(schema),
            description_placeholders={
                "intro": "Configure Saturday–Sunday schedule",
                "time": "Each time defines a weekend schedule trigger",
                "temp": "Target temperature to apply at that time",
                "sensor": "Sensor used for evaluating that schedule period"
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return T6ProgramOptionsFlowHandler(config_entry)

class T6ProgramOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
