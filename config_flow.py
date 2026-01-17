import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_SITE_ID, CONF_LINE

class SLConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SL Departures."""
    VERSION = 1

async def async_step_user(self, user_input=None):
    """Handle the initial step where the user enters data."""
    if user_input is not None:
        # Create the entry!
        return self.async_create_entry(
            title=f"Bus {user_input[CONF_LINE]} at {user_input[CONF_SITE_ID]}",
            data=user_input
        )

    # Form schema for the UI
    data_schema = vol.Schema({
        vol.Required(CONF_SITE_ID): str,
        vol.Required(CONF_LINE): str,
    })

    return self.async_show_form(step_id="user", data_schema=data_schema)