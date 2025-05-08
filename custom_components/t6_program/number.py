from homeassistant.components.number import NumberEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "t6_program"


class BaseT6Number(NumberEntity, RestoreEntity):
    def __init__(self, name: str, unique_id: str, default: float, min_v: float, max_v: float, entry_id: str):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = unique_id
        self._attr_native_value = default
        self._default = default
        self._attr_native_unit_of_measurement = "°C"
        self._attr_native_min_value = min_v
        self._attr_native_max_value = max_v
        self._attr_native_step = 0.5
        self._attr_has_entity_name = True
        self._entry_id = entry_id

    @property
    def native_value(self):
        return self._attr_native_value

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        if (last_state := await self.async_get_last_state()) is not None:
            try:
                self._attr_native_value = float(last_state.state)
            except ValueError:
                self._attr_native_value = self._default

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "T6 Program",
            "manufacturer": "Custom",
            "model": "T6 Scheduler",
            "entry_type": "service"
        }


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    entities = []

    # Temperature schedule slots
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            key = f"{prefix}_temperature_{i}"
            name = key.replace("_", " ").title()
            val = entry.data.get(key, 20.0)
            entities.append(
                BaseT6Number(name=name, unique_id=key, default=val, min_v=10.0, max_v=30.0, entry_id=entry.entry_id)
            )

    # Global number entities
    fixed_ranges = {
        "tolerance_cool": (1.0, 0.5, 5.0),
        "tolerance_heat": (1.0, 0.5, 5.0),
        "current_temperature": (20.0, 10, 30),
        "current_target_temperature": (20.0, 10, 30),
        "adjusted_cool_temperature": (20.0, 10, 30),
        "adjusted_heat_temperature": (20.0, 10, 30),
    }

    for key, (default, min_v, max_v) in fixed_ranges.items():
        val = entry.data.get(key, default)
        name = key.replace("_", " ").title()
        entities.append(
            BaseT6Number(name=name, unique_id=key, default=val, min_v=min_v, max_v=max_v, entry_id=entry.entry_id)
        )

    async_add_entities(entities, update_before_add=True)
