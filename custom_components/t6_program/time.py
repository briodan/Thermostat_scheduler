from datetime import time
from homeassistant.components.time import TimeEntity
from homeassistant.helpers.restore_state import RestoreEntity

DOMAIN = "t6_program"

DEFAULT_TIMES = {
    "m_f_time_1": time(6, 0),
    "m_f_time_2": time(8, 0),
    "m_f_time_3": time(15, 0),
    "m_f_time_4": time(21, 0),
    "s_s_time_1": time(6, 0),
    "s_s_time_2": time(8, 0),
    "s_s_time_3": time(15, 0),
    "s_s_time_4": time(21, 0),
}


async def async_setup_entry(hass, entry, async_add_entities):
    entities = []
    for entity_id, default_time in DEFAULT_TIMES.items():
        value = entry.data.get(entity_id)
        if isinstance(value, str):
            try:
                parsed = time.fromisoformat(value)
            except ValueError:
                parsed = default_time
        else:
            parsed = default_time
        entities.append(ScheduleTimeEntity(name=entity_id, unique_id=entity_id, initial_time=parsed, entry_id=entry.entry_id))
    async_add_entities(entities)


class ScheduleTimeEntity(TimeEntity, RestoreEntity):
    def __init__(self, name: str, unique_id: str, initial_time: time, entry_id: str):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = unique_id
        self._attr_has_entity_name = True
        self._time = initial_time
        self._entry_id = entry_id

    @property
    def native_value(self) -> time:
        return self._time

    async def async_set_value(self, value: time) -> None:
        self._time = value
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if (state := await self.async_get_last_state()) and state.state != "unknown":
            try:
                self._time = time.fromisoformat(state.state)
            except ValueError:
                pass

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "T6 Program",
            "manufacturer": "Custom",
            "model": "T6 Scheduler",
            "entry_type": "service",
        }
