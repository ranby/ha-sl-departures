import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

class SLDeparturesCard extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {},
    };
  }

  render() {
    const entityId = this.config.entity;
    const stateObj = this.hass.states[entityId];

    if (!stateObj) {
      return html`
        <ha-card>
          <div class="error">Entity not found: ${entityId}</div>
        </ha-card>
      `;
    }

    const departures = stateObj.attributes.upcoming || [];
    const stopName = stateObj.attributes.stop_name || "Departures";

    return html`
      <ha-card>
        <div class="card-header">
          🚌 ${stopName}
        </div>
        <div class="card-content">
          <table>
            <thead>
              <tr>
                <th>Line</th>
                <th class="grow">Destination</th>
                <th class="time-header">Time</th>
              </tr>
            </thead>
            <tbody>
              ${departures.length > 0
                ? departures.map(
                    (bus) => html`
                      <tr>
                        <td class="line-cell"><strong>${bus.line}</strong></td>
                        <td class="grow">${bus.destination}</td>
                        <td class="time-cell">
                          <span class="time-badge">${bus.display}</span>
                        </td>
                      </tr>
                    `
                  )
                : html`<tr><td colspan="3" class="no-data">No upcoming departures</td></tr>`}
            </tbody>
          </table>
        </div>
      </ha-card>
    `;
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error("Please define an entity");
    }
    this.config = config;
  }

  static get styles() {
    return css`
      :host {
        --accent-color: var(--primary-color);
      }
      .card-header {
        font-size: 1.2em;
        padding: 16px 16px 4px 16px;
        font-weight: bold;
      }
      .error {
        color: var(--error-color);
        padding: 16px;
      }
      table {
        width: 100%;
        border-collapse: collapse;
      }
      th {
        text-align: left;
        color: var(--secondary-text-color);
        font-size: 0.85em;
        text-transform: uppercase;
        padding: 8px 4px;
        border-bottom: 2px solid var(--divider-color);
      }
      td {
        padding: 10px 4px;
        border-bottom: 1px solid var(--divider-color);
      }
      .grow {
        width: 65%; /* This ensures the destination takes most space */
      }
      .line-cell {
        color: var(--accent-color);
        white-space: nowrap;
      }
      .time-header {
        text-align: right;
      }
      .time-cell {
        text-align: right;
        white-space: nowrap;
      }
      .time-badge {
        background: var(--secondary-background-color);
        padding: 4px 8px;
        border-radius: 4px;
        font-family: var(--code-font-family, monospace);
        font-size: 0.9em;
      }
      .no-data {
        text-align: center;
        padding: 20px;
        color: var(--secondary-text-color);
      }
    `;
  }
}

// Ensure the name here matches the YAML type exactly
customElements.define("sl-departures-card", SLDeparturesCard);

// Metadata for the UI Picker
window.customCards = window.customCards || [];
window.customCards.push({
  type: "sl-departures-card",
  name: "SL Departures Card",
  description: "A LitElement card for SL bus departures",
});