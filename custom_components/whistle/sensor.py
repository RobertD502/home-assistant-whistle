""" Sensor platform for Whistle integration."""
from __future__ import annotations

from typing import Any

from datetime import datetime
from zoneinfo import ZoneInfo

from whistleaio.model import Pet

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import(
    LENGTH_MILES,
    PERCENTAGE,
    TIME_DAYS,
    TIME_MINUTES,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, WHISTLE_COORDINATOR
from .coordinator import WhistleDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """ Set Up Whistle Sensor Entities. """

    coordinator: WhistleDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][WHISTLE_COORDINATOR]

    sensors = []


    for pet_id, pet_data in coordinator.data.pets.items():
            """ Pet """
            if pet_data.data['device']:
                """ Only get 24h usage if GPS device. """
                if pet_data.data['device']['has_gps']:
                    sensors.extend((
                        WifiUsage(coordinator, pet_id),
                        CellUsage(coordinator, pet_id),
                    ))
                sensors.extend((
                    Battery(coordinator, pet_id),
                    BatteryDaysLeft(coordinator, pet_id),
                    MinutesActive(coordinator, pet_id),
                    MinutesRest(coordinator, pet_id),
                    Streak(coordinator, pet_id),
                    ActivityGoal(coordinator, pet_id),
                    Distance(coordinator, pet_id),
                    Calories(coordinator, pet_id),
                    LastCheckIn(coordinator, pet_id),
                    Event(coordinator, pet_id),
                    EventStart(coordinator, pet_id),
                    EventEnd(coordinator, pet_id),
                    EventDistance(coordinator, pet_id),
                    EventCalories(coordinator, pet_id),
                    EventDuration(coordinator, pet_id),
                ))

    async_add_entities(sensors)

class Battery(CoordinatorEntity, SensorEntity):
    """ Representation of Whistle Device Battery. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_battery'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Battery"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def native_value(self) -> int:
        """ Return battery percentage. """

        return self.pet_data.data['device']['battery_level']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return percentage as the native unit. """

        return PERCENTAGE

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.BATTERY

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.MEASUREMENT

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

class BatteryDaysLeft(CoordinatorEntity, SensorEntity):
    """ Representation of estimated battery life left in days. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_data(self) -> dict[str, Any]:
        """ Handle coordinator device data. """

        return self.coordinator.data.pets[self.pet_id].device

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_battery_days_left'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Battery days left"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:timer-sand'

    @property
    def native_value(self) -> float:
        """ Return estimated days left. """

        return self.device_data['device']['battery_stats']['battery_days_left']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return days as the native unit. """

        return TIME_DAYS

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.DURATION

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.MEASUREMENT

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

class WifiUsage(CoordinatorEntity, SensorEntity):
    """ Representation of Whistle Device Battery 24h WiFi usage. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_data(self) -> dict[str, Any]:
        """ Handle coordinator device data. """

        return self.coordinator.data.pets[self.pet_id].device

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_24h_wifi_usage'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "24H WiFi battery usage"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set entity icon. """

        return 'mdi:wifi'

    @property
    def native_value(self) -> int:
        """ Return 24h WiFi battery usage as percentage. """

        return int(round(((float(self.device_data['device']['battery_stats']['prior_usage_minutes']['24h']['power_save_mode']) / 1440) * 100), 0))

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return percentage as the native unit. """

        return PERCENTAGE

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.MEASUREMENT

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

class CellUsage(CoordinatorEntity, SensorEntity):
    """ Representation of Whistle Device Battery 24h cellular usage. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_data(self) -> dict[str, Any]:
        """ Handle coordinator device data. """

        return self.coordinator.data.pets[self.pet_id].device

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_24h_cell_usage'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "24H cellular battery usage"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set entity icon. """

        return 'mdi:signal-cellular-outline'

    @property
    def native_value(self) -> int:
        """ Return 24h cellular battery usage as percentage. """

        return int(round(((float(self.device_data['device']['battery_stats']['prior_usage_minutes']['24h']['cellular']) / 1440) * 100), 0))

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return percentage as the native unit. """

        return PERCENTAGE

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.MEASUREMENT

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

class MinutesActive(CoordinatorEntity, SensorEntity):
    """ Representation of today's active minutes. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_minutes_active'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Minutes active"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:run-fast'

    @property
    def native_value(self) -> int:
        """ Return today's active minutes. """

        return self.pet_data.data['activity_summary']['current_minutes_active']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return minutes as the native unit. """

        return TIME_MINUTES

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.DURATION

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.TOTAL_INCREASING

class MinutesRest(CoordinatorEntity, SensorEntity):
    """ Representation of today's resting minutes. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_minutes_rest'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Minutes rest"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:bed-clock'

    @property
    def native_value(self) -> int:
        """ Return today's rest minutes. """

        return self.pet_data.data['activity_summary']['current_minutes_rest']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return minutes as the native unit. """

        return TIME_MINUTES

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.DURATION

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.TOTAL_INCREASING

class Streak(CoordinatorEntity, SensorEntity):
    """ Representation of activity streak. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_activity_streak'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Activity streak"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:chart-timeline-variant-shimmer'

    @property
    def native_value(self) -> int:
        """ Return current activity streak. """

        return self.pet_data.data['activity_summary']['current_streak']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return days as the native unit. """

        return TIME_DAYS

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.DURATION

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.TOTAL_INCREASING

class ActivityGoal(CoordinatorEntity, SensorEntity):
    """ Representation of daily activity goal in minutes. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_activity_goal'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Activity goal"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:flag-checkered'

    @property
    def native_value(self) -> int:
        """ Return today's active minutes. """

        return self.pet_data.data['activity_summary']['current_activity_goal']['minutes']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return minutes as the native unit. """

        return TIME_MINUTES

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.DURATION

class Distance(CoordinatorEntity, SensorEntity):
    """ Representation of today's distance in miles. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_distance'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Distance"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:map-marker-distance'

    @property
    def native_value(self) -> float:
        """ Return today's distance in miles. """

        return self.pet_data.dailies['dailies'][00]['distance']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return miles as the native unit. """

        return LENGTH_MILES

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.TOTAL_INCREASING

class Calories(CoordinatorEntity, SensorEntity):
    """ Representation of today's calories. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_calories'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Calories"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:fire'

    @property
    def native_value(self) -> int:
        """ Return today's calories burned. """

        return int(self.pet_data.dailies['dailies'][00]['calories'])

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return calories as the native unit. """

        return 'cal'

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.TOTAL_INCREASING

class LastCheckIn(CoordinatorEntity, SensorEntity):
    """ Representation of last time device sent data to Whistle servers. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_last_check_in'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Last check-in"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:server-network'

    @property
    def native_value(self) -> datetime:
        """ Return last check-in as datetime. """
        current_tz = self.pet_data.data['profile']['time_zone_name']
        return datetime.fromisoformat(self.pet_data.data['device']['last_check_in'].replace(' ' + current_tz, '')).replace(tzinfo=ZoneInfo(current_tz)).astimezone()

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.TIMESTAMP

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

class Event(CoordinatorEntity, SensorEntity):
    """ Representation of latest event. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_event'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Latest event"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        if self.pet_data.data['profile']['species'] == 'dog':
            return 'mdi:dog'
        if self.pet_data.data['profile']['species'] == 'cat':
            return 'mdi:cat'

    @property
    def native_value(self) -> str:
        """ Return latest event. """

        return self.pet_data.events['daily_items'][00]['title']

    @property
    def available(self) -> bool:
        """ Only return True if an event exists for today. """

        if self.pet_data.events['daily_items']:
            return True
        else:
            return False

class EventStart(CoordinatorEntity, SensorEntity):
    """ Representation of when last event started. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_event_start'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Event start"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:timer-play-outline'

    @property
    def native_value(self) -> datetime:
        """ Return event start time. """

        return datetime.fromisoformat(self.pet_data.events['daily_items'][00]['start_time'].replace('Z', '+00:00')).astimezone()

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.TIMESTAMP

    @property
    def available(self) -> bool:
        """ Only return True if an event exists for today. """

        if self.pet_data.events['daily_items']:
            return True
        else:
            return False

class EventEnd(CoordinatorEntity, SensorEntity):
    """ Representation of when last event ended. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_event_end'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Event end"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:timer-pause-outline'

    @property
    def native_value(self) -> datetime:
        """ Return event end time. """

        return datetime.fromisoformat(self.pet_data.events['daily_items'][00]['end_time'].replace('Z', '+00:00')).astimezone()

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.TIMESTAMP

    @property
    def available(self) -> bool:
        """ Only return True if an event exists for today. """

        if self.pet_data.events['daily_items']:
            return True
        else:
            return False

class EventDistance(CoordinatorEntity, SensorEntity):
    """ Representation of distance covered during latest event. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_event_distance'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Event distance"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:map-marker-distance'

    @property
    def native_value(self) -> float:
        """ Return event distance in miles. """

        return self.pet_data.events['daily_items'][00]['data']['distance']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return miles as the native unit. """

        return LENGTH_MILES

    @property
    def available(self) -> bool:
        """ Only return True if an event exists for today. """

        if self.pet_data.events['daily_items']:
            return True
        else:
            return False

class EventCalories(CoordinatorEntity, SensorEntity):
    """ Representation of calories burned during latest event. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_event_calories'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Event calories"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:fire'

    @property
    def native_value(self) -> int:
        """ Return today's calories burned. """

        return self.pet_data.events['daily_items'][00]['data']['calories']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return calories as the native unit. """

        return 'cal'

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class. """

        return SensorStateClass.TOTAL

    @property
    def available(self) -> bool:
        """ Only return True if an event exists for today. """

        if self.pet_data.events['daily_items']:
            return True
        else:
            return False

class EventDuration(CoordinatorEntity, SensorEntity):
    """ Representation of latest event duration in minutes. """

    def __init__(self, coordinator, pet_id):
        super().__init__(coordinator)
        self.pet_id = pet_id


    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.pet_data.id)},
            "name": self.pet_data.data['name'],
            "manufacturer": "Whistle",
            "model": self.pet_data.data['device']['model_id'],
            "configuration_url": "https://www.whistle.com/",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.pet_data.id) + '_event_duration'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Event duration"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self) -> str:
        """ Set icon for entity. """

        return 'mdi:timer-outline'

    @property
    def native_value(self) -> float:
        """ Return latest event duration in minutes. """

        return self.pet_data.events['daily_items'][00]['data']['duration']

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return minutes as the native unit. """

        return TIME_MINUTES

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class. """

        return SensorDeviceClass.DURATION

    @property
    def available(self) -> bool:
        """ Only return True if an event exists for today. """

        if self.pet_data.events['daily_items']:
            return True
        else:
            return False
