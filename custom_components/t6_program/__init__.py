from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "t6_program"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the T6 Program component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up T6 Program from a config entry."""
    # Properly await platform setups
    await hass.config_entries.async_forward_entry_setups(entry, ["select", "number", "time"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload T6 Program entry."""
    unloads = await hass.config_entries.async_forward_entry_unloads(entry, ["select", "number", "time"])
    return all(unloads)