import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.entity_registry import async_get
from homeassistant.helpers import config_validation as cv

import logging
_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    DEFAULT_SENSOR,
    DEFAULT_TIME_STRING,
    DEFAULT_TOLERANCE_MAX_C, 
    DEFAULT_TOLERANCE_MAX_F,
    UNIT_CELSIUS,
    UNIT_FARENHEIT,
)

class T6ProgramConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._data = {}

    async def async_step_user(self, user_input=None):
        sensors = await self._get_temp_sensor_options()
        _LOGGER.debug("Available sensors: %s", sensors)
        default_sensor = list(sensors.keys())[0]

        if user_input:
            _LOGGER.debug("User input received in user step: %s", user_input)
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
            tolerance_max = DEFAULT_TOLERANCE_MAX_F if user_input["temperature_unit"] == UNIT_FARENHEIT else DEFAULT_TOLERANCE_MAX_C
            self._data["tolerance_max"] = tolerance_max
            #self._data["current_sensor"] = user_input["current_sensor"]
            sensor_list = user_input["sensor_filter"]
            self._data["current_sensor"] = sensor_list[0] if sensor_list else DEFAULT_SENSOR
            self._data["sensor_filter"] = user_input["sensor_filter"]
            _LOGGER.debug("User input received in user step: %s", user_input)

            return await self.async_step_mf_config()

        return self.async_show_form(step_id="user", data_schema=self._build_user_schema(sensors))

    def _build_user_schema(self, sensors):
        default_sensor = list(sensors.keys())[0]
        return vol.Schema({
            vol.Required("temperature_unit", default= UNIT_CELSIUS): vol.In([UNIT_CELSIUS, UNIT_FARENHEIT]),
            vol.Required("temp_min"): vol.Coerce(float),
            vol.Required("temp_max"): vol.Coerce(float),
            vol.Required("temp_default"): vol.Coerce(float),
            #vol.Required("current_sensor", default=default_sensor): vol.In(sensors),
            vol.Required("sensor_filter", default=[default_sensor]): cv.multi_select(sensors)
        })

    async def async_step_mf_config(self, user_input=None):
        sensor_list = self._data.get("sensor_filter", [DEFAULT_SENSOR])
        sensors = sensor_list
        default_sensor = sensor_list[0]

        temp_min = self._data["temp_min"]
        temp_max = self._data["temp_max"]
        temp_default = self._data["temp_default"]

        if user_input:
            self._data.update(user_input)
            return await self.async_step_ss_config()

        schema = {}
        for i in range(1, 5):
            schema[vol.Required(f"m_f_time_{i}", default=DEFAULT_TIME_STRING)] = str
            schema[vol.Required(f"m_f_temperature_{i}", default=temp_default)] = vol.All(
                vol.Coerce(float), vol.Range(min=temp_min, max=temp_max)
            )
            schema[vol.Required(f"m_f_sensor_{i}", default=default_sensor)] = vol.In(sensors)

        return self.async_show_form(step_id="mf_config", data_schema=vol.Schema(schema))

    async def async_step_ss_config(self, user_input=None):
        sensor_list = self._data.get("sensor_filter", [DEFAULT_SENSOR])
        sensors = sensor_list
        default_sensor = sensor_list[0]

        temp_min = self._data["temp_min"]
        temp_max = self._data["temp_max"]
        temp_default = self._data["temp_default"]

        if user_input:
            self._data.update(user_input)
            return self.async_create_entry(title="T6 Program", data=self._data)

        schema = {}
        for i in range(1, 5):
            schema[vol.Required(f"s_s_time_{i}", default=DEFAULT_TIME_STRING)] = str
            schema[vol.Required(f"s_s_temperature_{i}", default=temp_default)] = vol.All(
                vol.Coerce(float), vol.Range(min=temp_min, max=temp_max)
            )
            schema[vol.Required(f"s_s_sensor_{i}", default=default_sensor)] = vol.In(sensors)

        return self.async_show_form(step_id="ss_config", data_schema=vol.Schema(schema))

    async def _get_temp_sensor_options(self):
        try:
            registry = async_get(self.hass)
            sensors = {
                e.entity_id: e.name or e.entity_id
                for e in registry.entities.values()
                if e.domain == "sensor" and ("temperature" in (e.device_class or "") or "temperature" in e.entity_id)
            }
            if not sensors:
                sensors = {DEFAULT_SENSOR: "No temperature sensors found"}
            return sensors
        except Exception as e:
            _LOGGER.exception("Failed to get temperature sensors: %s", e)
            return {DEFAULT_SENSOR: "Error retrieving sensors"}

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return T6ProgramOptionsFlowHandler(config_entry)


class T6ProgramOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry
        self._data = dict(config_entry.data)

    async def async_step_init(self, user_input=None):
        registry = async_get(self.hass)
        all_sensors = {
            e.entity_id: e.entity_id
            for e in registry.entities.values()
            if e.domain == "sensor" and ("temperature" in (e.device_class or "") or "temperature" in e.entity_id)
        }

        if user_input:
            self._data["sensor_filter"] = user_input["sensor_filter"]
            self._data["current_sensor"] = user_input["sensor_filter"][0] if user_input["sensor_filter"] else DEFAULT_SENSOR
            return self.async_create_entry(title="", data=self._data)

        selected = self._data.get("sensor_filter", list(all_sensors.keys())[:1])
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("sensor_filter", default=selected): cv.multi_select(all_sensors),
            })
        )
