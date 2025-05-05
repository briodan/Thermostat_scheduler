from datetime import time
from .const import *
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components.input_datetime import InputDatetime
from homeassistant.components.input_number import InputNumber

DOMAIN = "t6_program"  # Required for Home Assistant to recognize the integration

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    data = entry.data

    # InputDatetime
    dt_component = EntityComponent(hass, "input_datetime", hass.config)
    dt_entities = []

    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            eid = f"{prefix}_time_{i}"
            val = data[eid]
            hour, minute = map(int, val.split(":"))
            dt_entities.append(InputDatetime(
                name=eid.replace("_", " ").title(),
                has_time=True,
                has_date=False,
                initial=time(hour, minute)
            ))

    await dt_component.async_add_entities(dt_entities)

    # InputNumber
    num_component = EntityComponent(hass, "input_number", hass.config)
    num_entities = []

    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            eid = f"{prefix}_temperature_{i}"
            val = float(data[eid])
            num_entities.append(InputNumber(
                name=eid.replace("_", " ").title(),
                min_value=10,
                max_value=30,
                step=0.5,
                unit_of_measurement="°C",
                initial=val
            ))

    # Tolerances
    for tol_key in ("cool_tolerance", "heat_tolerance"):
        val = float(data.get(tol_key, DEFAULT_TOLERANCE))
        num_entities.append(InputNumber(
            name=tol_key.replace("_", " ").title(),
            min_value=0.5,
            max_value=5.0,
            step=0.5,
            unit_of_measurement="°C",
            initial=val
        ))

    await num_component.async_add_entities(num_entities)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return True
