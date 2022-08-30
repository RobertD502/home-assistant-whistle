# Whistle Home Assistant Integration
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) ![GitHub manifest version (path)](https://img.shields.io/github/manifest-json/v/RobertD502/home-assistant-whistle?filename=custom_components%2Fwhistle%2Fmanifest.json)

<a href="https://www.buymeacoffee.com/RobertD502" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="100" width="424"></a>

### A lot of work has been put into creating the backend and this integration. If you enjoy this integration, consider donating by clicking on the logo above.

***All proceeds go towards helping a local animal rescue.**


This integration was made for the `Whistle Go Explore` and `Whistle Fit`. It should also work with the new `Whistle Switch`- testers needed!

**Prior To Installation**

You will need credentials consisting of your Whistle `email` and `password`.

## Installation

### With HACS
1. Open HACS Settings and add this repository (https://github.com/RobertD502/home-assistant-whistle)
as a Custom Repository (use **Integration** as the category).
2. The `Whistle` page should automatically load (or find it in the HACS Store)
3. Click `Install`

### Manual
Copy the `whistle` directory from `custom_components` in this repository,
and place inside your Home Assistant Core installation's `custom_components` directory.


## Setup
1. Install this integration.
2. Navigate to the Home Assistant Integrations page (Settings --> Devices & Services)
3. Click the `+ ADD INTEGRATION` button in the lower right-hand corner
4. Search for `Whistle`

# Devices

A device is created for each pet. See below for the entities available and special notes.

# Entities

| Entity            | Entity Type | Notes                                                                                                                                                                                                                                                   |
|-------------------| --- |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Activity goal`   | `Sensor` | Current daily goal as set up in the Whistle app. `Note`: The state is in `minutes` but the Home Assistant UI displays this sensor in `HH:MM:SS`                                                                                                         |
| `Activity streak` | `Sensor` | Current amount of days in a row pet has hit daily goal. `Note`: The state is in `days` but the Home Assistant UI displays this sensor in `HH:MM:SS`                                                                                                     |
| `Calories`        | `Sensor` | Number of calories burned today.                                                                                                                                                                                                                        |
| `Distance`        | `Sensor` | Distance covered in miles today.                                                                                                                                                                                                                        |
| `Event calories`  | `Sensor` | Calories burned during the most recent event reported. `Note`: As there is no event at midnight, this entity will show as unavailable. As soon as an event is reported by Whistle servers for the current day, this entity will become available again. |
| `Event distance` | `Sensor` | Amount of miles covered during the latest event. `Note`: As there is no event at midnight, this entity will show as unavailable. As soon as an event is reported by Whistle servers for the current day, this entity will become available again. |
| `Event duration` | `Sensor` | How long the last event lasted. The state of this entity is in `minutes` but the Home Assistant UI displays this sensor in `HH:MM:SS`. `Note`: As there is no event at midnight, this entity will show as unavailable. As soon as an event is reported by Whistle servers for the current day, this entity will become available again. |
| `Event end` | `Sensor` | When the event ended as represented in datetime format. `Note`: As there is no event at midnight, this entity will show as unavailable. As soon as an event is reported by Whistle servers for the current day, this entity will become available again. |
| `Event start` | `Sensor` | When the event started as represented in datetime format. `Note`: As there is no event at midnight, this entity will show as unavailable. As soon as an event is reported by Whistle servers for the current day, this entity will become available again. |
| `Last event` | `Sensor` | Most recent event reported by Whistle servers. `Note`: As there is no event at midnight, this entity will show as unavailable. As soon as an event is reported by Whistle servers for the current day, this entity will become available again. |
| `Minutes active` | `Sensor` | Minutes your pet has been active today. `Note`: The state of this sensor is in `minutes` but the Home Assistant UI displays this sensor in `HH:MM:SS` |
| `Minutes rest` | `Sensor` | Minutes your pet has spent resting today. `Note`: The state of this sensor is in `minutes` but the Home Assistant UI displays this sensor in `HH:MM:SS` |
| `24H WiFi battery usage` | `Sensor` | `This entity is only available for GPS Whistle devices`. Displays the percent of time, during last 24 hours, that Whistle device used WiFi. |
| `24H cellular battery usage` | `Sensor` | `This entity is only available for GPS Whistle devices`. Displays the percent of time, during last 24 hours, that Whistle device used cellular connection. |
| `Battery` | `Sensor` | Current Whistle device battery percentage. |
| `Battery days left` | `Sensor` | Estimated battery life left. `Note`: This sensor's state is in `days` but the Home Assitant UI displays the sensor in `HH:MM:SS` |
| `Last check-in` | `Sensor` | Last time whistle device contacted Whistle servers. Represented as datetime. |
| `Whistle tracker` | `Device Tracker` | `This entity is only available for GPS Whistle devices.` Shows the most recent reported location using predefined places created within the Whistle app. If pet is not located in a predefined Whistle place, the device tracker has a state of `Away`. |

