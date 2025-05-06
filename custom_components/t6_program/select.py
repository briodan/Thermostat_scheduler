from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "t6_program"

TIME_OPTIONS = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 30)]

class T6ProgramTimeSelect(SelectEntity):
    def __init__(self, name: str, unique_id: str, current_option: str):
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_options = TIME_OPTIONS
        self._attr_current_option = current_option

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self.async_write_ha_state()

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    entities = []
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            eid = f"{prefix}_time_{i}"
            name = eid.replace("_", " ").title()
            entities.append(T6ProgramTimeSelect(name, eid, "07:00"))
    async_add_entities(entities)
