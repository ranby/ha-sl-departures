import logging
import requests
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Bridge between UI and the Sensor Class."""
    site_id = config_entry.data.get("site_id")
    lines = config_entry.data.get("lines")  # Expecting a list now
    if not isinstance(lines, list):
        lines = [lines] if lines is not None else []
    async_add_entities([SLDepartureSensor(site_id, lines)], update_before_add=True)

class SLDepartureSensor(SensorEntity):
    def __init__(self, site_id, lines):
        self._site_id = site_id
        self._lines = [str(l) for l in lines]
        self._attr_name = f"Bus {','.join(self._lines)} at {site_id}"
        self._attr_unique_id = f"sl_{site_id}_{'_'.join(self._lines)}"
        self._state = "Initializing..."
        self._attributes = {"upcoming": [], "lines": self._lines, "stop_name": "Loading..."}

    @property
    def native_value(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        """Fetch and update upcoming departures for the configured bus lines and stop."""
        url = f"https://transport.integration.sl.se/v1/sites/{self._site_id}/departures"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            departures = []
            stop_name = None
            for dep in data.get("departures", []):
                # Only include departures for the configured lines (designation)
                line_designation = str(dep.get("line", {}).get("designation"))
                if line_designation in self._lines:
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