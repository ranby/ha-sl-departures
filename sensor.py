import logging
import requests
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Bridge between UI and the Sensor Class."""
    site_id = config_entry.data.get("site_id")
    line = config_entry.data.get("line")
    async_add_entities([SLDepartureSensor(site_id, line)], update_before_add=True)

class SLDepartureSensor(SensorEntity):
    def __init__(self, site_id, line):
        self._site_id = site_id
        self._line = line
        self._attr_name = f"Bus {line} at {site_id}"
        self._attr_unique_id = f"sl_{site_id}_{line}"
        self._state = "Initializing..."
        self._attributes = {"upcoming": [], "line": line, "stop_name": "Loading..."}

    @property
    def native_value(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        """Fetch and update upcoming departures for the configured bus line and stop."""
        url = f"https://transport.integration.sl.se/v1/sites/{self._site_id}/departures"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            departures = []
            stop_name = None
            for dep in data.get("departures", []):
                # Only include departures for the configured line (designation)
                if str(dep.get("line", {}).get("designation")) == str(self._line):
                    if not stop_name:
                        stop_name = dep.get("stop_area", {}).get("name", "Unknown")
                    departures.append({
                        "scheduled": dep.get("scheduled"),
                        "expected": dep.get("expected"),
                        "display": dep.get("display"),
                        "direction": dep.get("direction"),
                        "destination": dep.get("destination"),
                        "line": dep.get("line", {}).get("designation"),
                    })
            self._attributes["upcoming"] = departures
            self._attributes["stop_name"] = stop_name or "Unknown"
            if departures:
                self._state = departures[0]["display"]
            else:
                self._state = "No departures"
        except Exception as e:
            _LOGGER.error(f"Failed to update departures: {e}")
            self._state = "Error"
            self._attributes["upcoming"] = []