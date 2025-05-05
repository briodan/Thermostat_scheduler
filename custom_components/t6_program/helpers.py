from homeassistant.components.input_datetime import (
    DOMAIN as DATETIME_DOMAIN,
    async_set_datetime,
    InputDatetime,
)
from homeassistant.components.input_number import (
    DOMAIN as NUMBER_DOMAIN,
    InputNumber,
)
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.core import callback
from homeassistant.const import ATTR_NAME

from .const import *

async def create_entities(hass: HomeAssistantType):
    # Create InputDatetime component
    datetime_component = EntityComponent(hass, DATETIME_DOMAIN, hass.config)
    number_component = EntityComponent(hass, NUMBER_DOMAIN, hass.config)

    datetime_entities = []
    for entity_id in ALL_INPUT_DATETIMES:
        datetime_entities.append(
            InputDatetime(
                name=entity_id.replace("_", " ").title(),
                has_date=False,
                has_time=True,
                initial=None,
            )
        )

    number_entities = []
    for entity_id in ALL_INPUT_NUMBERS:
        number_entities.append(
            InputNumber(
                name=entity_id.replace("_", " ").title(),
                min_value=10,
                max_value=30,
                step=0.5,
                unit_of_measurement="°C",
                initial=None,
            )
        )

    await datetime_component.async_add_entities(datetime_entities)
    await number_component.async_add_entities(number_entities)
