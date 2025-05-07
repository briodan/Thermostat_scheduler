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
        self._attr_entity_id = f"select.t6_program_{unique_id}"
        self._attr_options = TIME_OPTIONS
        self._attr_current_option = current_option

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "T6 Program",
            "manufacturer": "Custom",
            "model": "T6 Scheduler",
            "entry_type": "service"
        }


class T6ProgramSensorSelect(SelectEntity):
    def __init__(self, config_entry, name: str, unique_id: str, options: list[str], selected: str):
        self._config_entry = config_entry
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_entity_id = f"select.t6_program_{unique_id}"
        self._attr_options = options
        self._attr_current_option = selected

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "T6 Program",
            "manufacturer": "Custom",
            "model": "T6 Scheduler",
            "entry_type": "service"
        }


class T6ProgramFixedSelect(SelectEntity):
    def __init__(self, config_entry, name: str, unique_id: str, options: list[str], default: str):
        self._config_entry = config_entry
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_entity_id = f"select.t6_program_{unique_id}"
        self._attr_options = options
        self._attr_current_option = default

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "T6 Program",
            "manufacturer": "Custom",
            "model": "T6 Scheduler",
            "entry_type": "service"
        }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    entities = []

    # Time slot selects
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            eid = f"{prefix}_time_{i}"
            name = eid.replace("_", " ").title()
            selected = entry.data.get(eid, "07:00")
            entities.append(T6ProgramTimeSelect(entry, name, eid, selected))

    # Get temperature sensors
    registry = async_get(hass)
    all_entities = registry.entities.values()
    temp_sensors = sorted([
        e.entity_id for e in all_entities
        if e.domain == "sensor" and (
            (e.device_class == "temperature") or "temperature" in e.entity_id
        )
    ]) or ["sensor.none_found"]
    default_sensor = temp_sensors[0]

    # Sensor slot selects
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            eid = f"{prefix}_sensor_{i}"
            name = eid.replace("_", " ").title()
            selected = entry.data.get(eid, default_sensor)
            entities.append(T6ProgramSensorSelect(entry, name, eid, temp_sensors, selected))

    # Current sensor
    selected = entry.data.get("current_sensor", default_sensor)
    entities.append(T6ProgramSensorSelect(entry, "Current Sensor", "current_sensor", temp_sensors, selected))

    # Thermostat state
    selected = entry.data.get("thermostat_state", "idle")
    entities.append(
        T6ProgramFixedSelect(entry, "Thermostat State", "thermostat_state", ["idle", "heat", "cool"], selected)
    )

    async_add_entities(entities)
