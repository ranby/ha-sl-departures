{% set departures = state_attr('sensor.bus_444446446c_471_at_4120', 'upcoming') %}
## 🚌 {{ state_attr('sensor.bus_444446446c_471_at_4120', 'stop_name') }}

| Line | Destination &nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Time |
| :--- | :--- | :--- |
{% if departures -%}
{% for bus in departures -%}
| **{{ bus.line }}** | {{ bus.destination }} | `{{ bus.display }}` |
{% endfor -%}
{% else -%}
| | No departures | |
{% endif %}

***
**Last Updated:** {{ states.sensor.bus_444446446c_471_at_4120.last_updated.strftime('%H:%M:%S') }}