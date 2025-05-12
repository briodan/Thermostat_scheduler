from homeassistant.components.number import NumberEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

DOMAIN = "t6_program"

# Step values (fixed as per your requirement)
STEP_TEMP = 0.01
STEP_TOLERANCE = 0.5

# Tolerance configuration (still hardcoded)
DEFAULT_TOLERANCE = 1.0
TOLERANCE_MIN = 0.5
TOLERANCE_MAX = 5.0


class BaseT6Number(NumberEntity, RestoreEntity):
    def __init__(
        self,
        name: str,
        unique_id: str,
        default: float,
        min_v: float,
        max_v: float,
        step: float,
        entry_id: str,
        unit: str
    ):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = unique_id
        self._attr_native_value = default
        self._default = default
        self._attr_native_unit_of_measurement = unit
        self._attr_native_min_value = min_v
        self._attr_native_max_value = max_v
        self._attr_native_step = step
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

    # User-defined temperature configuration
    temp_min = entry.data["temp_min"]
    temp_max = entry.data["temp_max"]
    temp_default = entry.data["temp_default"]
    unit = entry.data.get("temperature_unit", "°C")

    # Scheduled temperature slots
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            key = f"{prefix}_temperature_{i}"
            val = entry.data[key]
            entities.append(
                BaseT6Number(
                    name=key.replace("_", " ").title(),
                    unique_id=key,
                    default=val,
                    min_v=temp_min,
                    max_v=temp_max,
                    step=STEP_TEMP,
                    entry_id=entry.entry_id,
                    unit=unit
                )
            )

    # Global numeric configuration entities
    fixed_ranges = {
        # Tolerances: hardcoded ranges
        "tolerance_cool": (entry.data["tolerance_cool"], TOLERANCE_MIN, entry.data.get("tolerance_max", 5.0), STEP_TOLERANCE),
        "tolerance_heat": (entry.data["tolerance_heat"], TOLERANCE_MIN, entry.data.get("tolerance_max", 5.0), STEP_TOLERANCE),

        # Temperatures: user-defined limits
        "current_temperature": (entry.data["current_temperature"], temp_min, temp_max, STEP_TEMP),
        "current_target_temperature": (entry.data["current_target_temperature"], temp_min, temp_max, STEP_TEMP),
        "adjusted_cool_temperature": (entry.data["adjusted_cool_temperature"], temp_min, temp_max, STEP_TEMP),
        "adjusted_heat_temperature": (entry.data["adjusted_heat_temperature"], temp_min, temp_max, STEP_TEMP),
    }

    for key, (default, min_v, max_v, step) in fixed_ranges.items():
        name = key.replace("_", " ").title()
        entities.append(
            BaseT6Number(
                name=name,
                unique_id=key,
                default=default,
                min_v=min_v,
                max_v=max_v,
                step=step,
                entry_id=entry.entry_id,
                unit=unit
            )
        )

    async_add_entities(entities, update_before_add=True)
