# Whistle Home Assistant Integration
<a href="https://www.buymeacoffee.com/RobertD502" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) ![GitHub manifest version (path)](https://img.shields.io/github/manifest-json/v/RobertD502/home-assistant-whistle?filename=custom_components%2Fwhistle%2Fmanifest.json)

Custom component for Home Assistant Core for Whistle GPS pet tracker. This integration was made for the `Whistle Go Explore`, however, it should also work with the new `Whistle Switch`- testers needed!

Donations aren't required, but are always appreciated. If you enjoy this integration, consider buying me a coffee by clicking on the link above.

**Note:** If you previously used the "pywhistle" custom component, you will need to remove your credentials from the configuration.yaml file and any template sensors that you created prior to installing this custom component. In addition, installing this integration should overwrite the whistle folder which was created by pywhistle and located within the custom_components folder. However, it is best to manually delete the whistle folder prior to installing this custom component.

**Prior To Installation**

You will need credentials consisting of your whistle `username(e-mail)` and `password`.

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
2. Use Config Flow to configure the integration with your Whistle username(e-mail) and password.
    * Initiate Config Flow by navigating to Configuration > Integrations > click the "+" button > find "Whistle" (restart Home Assistant and / or clear browser cache if you can't find it)

## Features

### Whistle GPS Tracker
Whistle devices are exposed as `device_tracker` entities and have a `state` that displays `place name` as defined in the Whistle app. For example, if you've set up two places in the Whistle app, `Home` and `Vet`, if the whistle tracker is located at `Home` then the `state` of the device_tracker will be `Home`. If the whistle tracker is found to be at the `Vet`, then the `state` of the device_tracker will be `Vet`. If the device tracker is not located in any of the predefined places, the `state` of the device_tracker will be `Away`.  

Icon: the icon of the device_tracker will either be a cat or a dog depending on the pet associated with the Whistle device.

Available attributes:

| Attribute | Description |
| --- | --- |
| `battery_level` | Current battery charge level in `percent` |
| `latitude` | Last known latitude coordinate |
| `longitude` | Last Known longitude coordinate |
| `gps_accuracy` | GPS uncertainty in `meters` |
| `battery_status` | Displays if the battery is `on` or `off` |
| `battery_days_left` | Estimated number of `days` left before battery is empty |
| `pending_locate` | If locating pet is pending. Can be either `true` or `false` |
| `activity_streak` | Number of `days` in a row your pet has reached its activity goal |
| `activity_minutes_active` | Number of `minutes` your pet has been active today |
| `active_minutes_rest` | Number of minutes your pet has been resting today |
| `activity_goal` | Current activity goal, in `minutes`, for today as set up from the app |
| `activity_distance` | Distance covered, in `miles`, by your pet today |
| `activity_calories` | Number of calories burned by your pet today |
| `24h_battery_wifi_usage` | Amount of time in the last 24 hours, in `percent`, the Whistle used Wi-Fi (also known as Power Save Mode) |
| `24h_battery_cellular_usage` | Amount of time in the last 24 hours, in `percent`, the Whistle used the cellular network (this occurs when the tracker is not connected to Wi-Fi) |
| `last_check_in` | Last date and time the Whistle device contacted the Whistle servers |
