from homeassistant.components.number import NumberEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "t6_program"


class T6ProgramTemperatureNumber(NumberEntity, RestoreEntity):
    def __init__(self, config_entry, name: str, unique_id: str, default: float = 20.0):
        self._config_entry = config_entry
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_native_unit_of_measurement = "°C"
        self._attr_min_value = 10
        self._attr_max_value = 30
        self._attr_step = 0.5
        self._default = default
        self._attr_native_value = None

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        if (last_state := await self.async_get_last_state()) is not None:
            self._attr_native_value = float(last_state.state)
        else:
            self._attr_native_value = self._default

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
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            eid = f"{prefix}_temperature_{i}"
            name = eid.replace("_", " ").title()
            entities.append(T6ProgramTemperatureNumber(entry, name, eid, default=20.0))
    async_add_entities(entities)
