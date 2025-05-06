from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import async_get
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "t6_program"

TIME_OPTIONS = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 30)]


class T6ProgramTimeSelect(SelectEntity):
    def __init__(self, config_entry, name: str, unique_id: str, current_option: str):
        self._config_entry = config_entry
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_options = TIME_OPTIONS
        self._attr_current_option = current_option

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "T6 Program",
            "manufacturer": "Custom",
            "model": "T6 Scheduler",
            "entry_type": "service"
        }

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self.async_write_ha_state()


class T6ProgramSensorSelect(SelectEntity):
    def __init__(self, config_entry, name: str, unique_id: str, options: list[str], selected: str):
        self._config_entry = config_entry
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_options = options
        self._attr_current_option = selected

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "T6 Program",
            "manufacturer": "Custom",
            "model": "T6 Scheduler",
            "entry_type": "service"
        }

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    entities = []

    # Create time selectors
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            eid = f"{prefix}_time_{i}"
            name = eid.replace("_", " ").title()
            entities.append(T6ProgramTimeSelect(entry, name, eid, "07:00"))

    # Get temperature sensors from entity registry
    registry = async_get(hass)
    all_entities = registry.entities.values()
    temp_sensors = sorted([
        e.entity_id for e in all_entities
        if e.domain == "sensor" and (
            (e.device_class == "temperature") or "temperature" in e.entity_id
        )
    ])

    if not temp_sensors:
        temp_sensors = ["sensor.none_found"]

    default_sensor = temp_sensors[0]

    # Create sensor selectors
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            eid = f"{prefix}_sensor_{i}"
            name = eid.replace("_", " ").title()
            entities.append(T6ProgramSensorSelect(entry, name, eid, temp_sensors, default_sensor))

    async_add_entities(entities)
