import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

DEFAULT_TOLERANCE = 1.0

class T6ProgramConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for T6 Program."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="T6 Program", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("cool_tolerance", default=DEFAULT_TOLERANCE): vol.All(
                    vol.Coerce(float), vol.Range(min=0.5, max=5.0)
                ),
                vol.Required("heat_tolerance", default=DEFAULT_TOLERANCE): vol.All(
                    vol.Coerce(float), vol.Range(min=0.5, max=5.0)
                ),
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return T6ProgramOptionsFlowHandler(config_entry)


class T6ProgramOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for T6 Program."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        # For future enhancements (e.g., sensor selection, schedule count)
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
