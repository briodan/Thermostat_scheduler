from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "t6_program"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the T6 Program component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up T6 Program from a config entry."""
    # Forward the config entry to the select platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "select")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload T6 Program entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "select")
