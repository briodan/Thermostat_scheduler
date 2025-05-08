from datetime import datetime, time
from homeassistant.components.time import TimeEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "t6_program"
DEFAULT_TIME_STRING = "06:00"


def parse_time_string(s: str) -> time:
    """Parse 'HH:MM' string into datetime.time."""
    try:
        return datetime.strptime(s, "%H:%M").time()
    except Exception:
        return time(0, 0)  # fallback if invalid


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entities = []

    for prefix in ("m_f", "s_s"):
        for i in range(1, 5):
            key = f"{prefix}_time_{i}"
            time_str = entry.data.get(key, DEFAULT_TIME_STRING)
            entities.append(
                T6ProgramTimeEntity(
                    name=key.replace("_", " ").title(),
                    unique_id=key,
                    initial_time=parse_time_string(time_str),
                    entry_id=entry.entry_id,
                )
            )

    async_add_entities(entities)


class T6ProgramTimeEntity(TimeEntity, RestoreEntity):
    def __init__(self, name: str, unique_id: str, initial_time: time, entry_id: str):
        self._attr_name = name
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
                self._time = datetime.strptime(state.state, "%H:%M:%S").time()
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
