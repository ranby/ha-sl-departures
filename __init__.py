from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

# List the platforms you want to support (in your case, just sensor)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SL Departure Sensor from a config entry."""
    # This stores your configuration data so the sensor.py can find it
    hass.data.setdefault(DOMAIN, {})
    
    # This "forwards" the setup to your sensor.py file
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This handles removing the integration if you delete it from the UI
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)