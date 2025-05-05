from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

# If you want to add options during setup later, adjust this schema
STEP_USER_DATA_SCHEMA = vol.Schema({})

class MySchedulerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Scheduler."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="My Scheduler", data={})

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

    async def async_step_import(self, user_input):
        """Handle import from configuration.yaml (if needed)."""
        return await self.async_step_user(user_input)

    async def async_step_reauth(self, user_input=None):
        """Handle re-authentication if needed."""
        return self.async_abort(reason="not_implemented")
