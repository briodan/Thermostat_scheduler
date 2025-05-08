from homeassistant.components.select import SelectEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import async_get
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "t6_program"


def sanitize_instance_name(name: str) -> str:
    return name.lower().replace(" ", "_")


class BaseT6Select(SelectEntity, RestoreEntity):
    def __init__(self, name: str, unique_id: str, options: list[str], initial_option: str, entry_id: str):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = unique_id
        self._attr_options = options
        self._attr_current_option = initial_option
        self._attr_has_entity_name = True
        self._entry_id = entry_id

    @property
    def native_value(self) -> str:
        return self._attr_current_option

    async def async_select_option(self, option: str) -> None:
        self._attr_current_option = option
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if (state := await self.async_get_last_state()) and state.state in self._attr_options:
            self._attr_current_option = state.state

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "T6 Program",
            "manufacturer": "Custom",
            "model": "T6 Scheduler",
            "entry_type": "service",
        }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    entities = []

    registry = async_get(hass)
    all_entities = registry.entities.values()
    temp_sensors = sorted([
        e.entity_id for e in all_entities
        if e.domain == "sensor" and (
            e.device_class == "temperature" or "temperature" in e.entity_id
        )
    ]) or ["sensor.none_found"]
    default_sensor = temp_sensors[0]

    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            key = f"{prefix}_sensor_{i}"
            name = key.replace("_", " ").title()
            selected = entry.data.get(key, default_sensor)
            entities.append(
                BaseT6Select(name=name, unique_id=key, options=temp_sensors, initial_option=selected, entry_id=entry.entry_id)
            )

    selected = entry.data.get("current_sensor", default_sensor)
    entities.append(
        BaseT6Select(name="Current Sensor", unique_id="current_sensor", options=temp_sensors, initial_option=selected, entry_id=entry.entry_id)
    )

    state_options = ["idle", "heat", "cool"]
    selected = entry.data.get("thermostat_state", "idle")
    entities.append(
        BaseT6Select(name="Thermostat State", unique_id="thermostat_state", options=state_options, initial_option=selected, entry_id=entry.entry_id)
    )

    async_add_entities(entities, update_before_add=True)
