from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "t6_program"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the T6 Program component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up T6 Program from a config entry."""
    # Properly await platform setups
    await hass.config_entries.async_forward_entry_setup(entry, "select")
    await hass.config_entries.async_forward_entry_setup(entry, "number")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload T6 Program entry."""
    unload_select = await hass.config_entries.async_forward_entry_unload(entry, "select")
    unload_number = await hass.config_entries.async_forward_entry_unload(entry, "number")
    return unload_select and unload_number
