from homeassistant.components.number import NumberEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "t6_program"

class T6ProgramNumber(NumberEntity, RestoreEntity):
    def __init__(self, config_entry, name: str, unique_key: str, default: float, min_v: float, max_v: float):
        self._config_entry = config_entry
        instance_name = config_entry.data.get("instance_name", "t6_program")
        safe_instance = instance_name.lower().replace(" ", "_")

        # Correctly assign unique_id for use in entity_id
        self._attr_unique_id = f"{safe_instance}_{unique_key}"
        self._attr_name = name  # UI name (no prefix)
        self._attr_native_unit_of_measurement = "°C"
        self._attr_min_value = min_v
        self._attr_max_value = max_v
        self._attr_step = 0.5
        self._default = default
        self._attr_native_value = default  # Will be overwritten if restored

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
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
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
            eid = f"{prefix}_temperature_{i}"
            name = eid.replace("_", " ").title()
            val = entry.data.get(eid, 20.0)
            entities.append(T6ProgramNumber(entry, name, eid, val, 10, 30))

    # Global numbers
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
        entities.append(T6ProgramNumber(entry, name, key, val, min_v, max_v))

    async_add_entities(entities, update_before_add=True)
