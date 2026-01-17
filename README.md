# ha-sl-departures
Home Assistant integration showing SL departures. Based on [TrafikLab's API](https://www.trafiklab.se/api/our-apis/sl/transport/).

## Installation
Move the files described below into your Home Assistant instance, for example using the "Studio Code Server" integration.
### Sensor
Move the folder `custom_components/sl-departures` into the corresponding folder in your Home Assistance instance.

### Custom Card
Move the file `www/sl-departures-card.js` into the corresponding folder in your Home Assistant instance.

## Configuration

### Sensor
- **site_id:** The id of the stop you want to watch. The id can be found by making [this request](https://www.trafiklab.se/api/our-apis/sl/transport/#/default/Sites) and searching for your stop in the response JSON.
- **lines:** A comma-separated list of the lines you want to watch.
- **direction_code:** Select depending on if you want to display departures going in both directions or only one.

When setting up the integration, enter the bus stop site ID and a comma-separated list of bus lines (e.g., `1,2,3`).

Example:
- **Site ID:** `1234`
- **Lines:** `1,2,3`
