import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_SITE_ID, CONF_LINES, CONF_DIRECTION_CODE

class SLConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SL Departures."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters data."""
        if user_input is not None:
            # Split lines by comma and strip whitespace
            lines = [l.strip() for l in user_input[CONF_LINES].split(",") if l.strip()]
            direction_code = user_input.get(CONF_DIRECTION_CODE)
            if direction_code == "any":
                direction_code = None
            data = {
                CONF_SITE_ID: user_input[CONF_SITE_ID],
                CONF_LINES: lines,
                CONF_DIRECTION_CODE: direction_code,
            }
            return self.async_create_entry(
                title=f"Bus {','.join(lines)} at {user_input[CONF_SITE_ID]}",
                data=data
            )

        # Form schema for the UI (comma-separated lines, direction dropdown)
        data_schema = vol.Schema({
            vol.Required(CONF_SITE_ID): str,
            vol.Required(CONF_LINES): str,  # User enters comma-separated lines
            vol.Optional(CONF_DIRECTION_CODE, default="any"): vol.In(["any", "1", "2"]),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)