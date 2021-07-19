
"""Whistle Tracker Platform"""

import logging
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from homeassistant.helpers import entity_platform
from homeassistant.components.device_tracker.const import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=120)

_LOGGER = logging.getLogger(__name__)

"""Attributes"""

ATTR_BATTERY_STATUS = "battery_status"
ATTR_BATTERY_DAYS_LEFT = "battery_days_left"
ATTR_PENDING_LOCATE = "pending_locate"
ATTR_ACTIVITY_STREAK = "activity_streak"
ATTR_ACTIVITY_MINUTES_ACTIVE = "activity_minutes_active"
ATTR_ACTIVITY_MINUTES_REST = "activity_minutes_rest"
ATTR_ACTIVITY_GOAL = "activity_goal"
ATTR_ACTIVITY_DISTANCE = "activity_distance"
ATTR_ACTIVITY_CALORIES = "activity_calories"
ATTR_24H_BATTERY_WIFI_USAGE = "24h_battery_wifi_usage"
ATTR_24H_BATTERY_CELLULAR_USAGE = "24h_battery_cellular_usage"
ATTR_LAST_CHECK_IN = "last_check_in"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Whistle tracker devices."""
    whistle = hass.data[DOMAIN]

    await whistle.async_init()
    get_pets = await whistle.get_pets()

    pets = []

    for pet in get_pets:
        pets.append(WhistleTracker(pet, whistle))

    async_add_entities(pets, True)

class WhistleTracker(TrackerEntity):
    """Representation of Whistle Device Tracker"""

    def __init__(self, pet, whistle):
        self._pet = pet
        self._whistle = whistle
        self._available = True

    @property
    def should_poll(self):
        return True

    @property
    def unique_id(self):
        """Set ID to serial number of the Whistle Device"""
        return self._device_id

    @property
    def name(self):
        """Device tracker entity name"""
        return "whistle_" + self._name

    @property
    def icon(self):
        """Determine what icon to use"""
        if self._species == 'dog':
            return 'mdi:dog'
        if self._species == 'cat':
            return 'mdi:cat'

    @property
    def source_type(self):
        """Return GPS as the source"""
        return SOURCE_TYPE_GPS

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def location_accuracy(self):
        return self._location_accuracy

    @property
    def location_name(self):
        PLACES_LIST = self._places
        COMBINED_PLACES = {}
        for index in range(len(PLACES_LIST)):
            place_id = PLACES_LIST[index].get('id')
            place_name = PLACES_LIST[index].get('name')
            COMBINED_PLACES.update({place_id:place_name})
        if self._current_place_id in COMBINED_PLACES:
            return COMBINED_PLACES.get(self._current_place_id)
        else:
            return "Away"

    @property
    def battery_level(self):
        return self._battery_level

    @property
    def battery_status(self):
        return self._battery_status

    @property
    def battery_days_left(self):
        return self._battery_days_left

    @property
    def pending_locate(self) -> bool:
        return self._pending_locate

    @property
    def activity_streak(self):
        return self._activity_streak

    @property
    def activity_minutes_active(self):
        return self._activity_minutes_active

    @property
    def activity_minutes_rest(self):
        return self._activity_minutes_rest

    @property
    def activity_goal(self):
        return self._activity_goal

    @property
    def activity_distance(self):
        return self._activity_distance

    @property
    def activity_calories(self):
        return self._activity_calories

    @property
    def battery_wifi_usage(self):
        return self._24h_battery_wifi_usage

    @property
    def battery_cellular_usage(self):
        return self._24h_battery_cellular_usage

    @property
    def last_check_in(self):
        return self._last_check_in

    @property
    def available(self):
        return self._available

    @property
    def device_state_attributes(self) -> dict:
        """Return attributes."""
        return {
            ATTR_BATTERY_STATUS: self.battery_status,
            ATTR_BATTERY_DAYS_LEFT: self.battery_days_left,
            ATTR_PENDING_LOCATE: self.pending_locate,
            ATTR_ACTIVITY_STREAK: self.activity_streak,
            ATTR_ACTIVITY_MINUTES_ACTIVE: self.activity_minutes_active,
            ATTR_ACTIVITY_MINUTES_REST: self.activity_minutes_rest,
            ATTR_ACTIVITY_GOAL: self.activity_goal,
            ATTR_ACTIVITY_DISTANCE: self.activity_distance,
            ATTR_ACTIVITY_CALORIES: self.activity_calories,
            ATTR_24H_BATTERY_WIFI_USAGE: self.battery_wifi_usage,
            ATTR_24H_BATTERY_CELLULAR_USAGE: self.battery_cellular_usage,
            ATTR_LAST_CHECK_IN: self.last_check_in,
        }

    async def async_update(self):
        _LOGGER.info('Updating Whistle data')
        try:
            await self._whistle.async_init()
            pets = await self._whistle.get_pets()
        except Exception as e:
            _LOGGER.error("There was an error while updating: %s", e)
        _LOGGER.debug("Retrieved data:")
        _LOGGER.debug(pets)
        if not pets:
            _LOGGER.warning("No Pets found")
            return
        for animal in pets['pets']:
            dailies = await self._whistle.get_dailies(animal['id'])
            device = await self._whistle.get_device(animal['device']['serial_number'])
            self._places = await self._whistle.get_places()
            try:
                self._current_place_id = animal['last_location']['place']['id']
            except Exception as e:
                self._current_place_id = 0
            self._latitude = animal['last_location']['latitude']
            self._longitude = animal['last_location']['longitude']
            self._location_accuracy = animal['last_location']['uncertainty_meters']
            self._location_address = animal['last_location']['description']['address']
            self._device_id = animal['device']['serial_number']
            time_zone = animal['profile']['time_zone_name']
            self._last_check_in = datetime.fromisoformat(animal['device']['last_check_in'].replace(' ' + time_zone, '')).replace(tzinfo=ZoneInfo(time_zone)).astimezone()
            self._name = animal['name']
            self._species = animal['profile']['species']
            self._battery_level = animal['device']['battery_level']
            self._battery_status = animal['device']['battery_status']
            self._battery_days_left = device['device']['battery_stats']['battery_days_left']
            self._pending_locate = animal['device']['pending_locate']
            self._activity_streak = animal['activity_summary']['current_streak']
            self._activity_minutes_active = animal['activity_summary']['current_minutes_active']
            self._activity_minutes_rest = animal['activity_summary']['current_minutes_rest']
            self._activity_goal = animal['activity_summary']['current_activity_goal']['minutes']
            self._activity_distance = round(dailies['dailies'][0]['distance'], 1)
            self._activity_calories = round(dailies['dailies'][0]['calories'], 1)
            self._24h_battery_wifi_usage = round(((float(device['device']['battery_stats']['prior_usage_minutes']['24h']['power_save_mode']) / 1440) * 100), 0)
            self._24h_battery_cellular_usage = round(((float(device['device']['battery_stats']['prior_usage_minutes']['24h']['cellular']) / 1440) * 100), 0)
