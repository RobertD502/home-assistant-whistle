
"""Whistle Tracker Platform"""

import logging
import aiohttp
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from homeassistant.helpers import entity_platform
from homeassistant.exceptions import PlatformNotReady
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
    pets = []
    try:
        await whistle.async_init()
        get_pets = await whistle.get_pets()
    except Exception as e:
        _LOGGER.error("Failed to get pets from Whistle servers")
        raise PlatformNotReady from e

    for pet in get_pets["pets"]:
        if pet['device']['has_gps']:
            pets.append(WhistleTracker(pet, whistle))

    async_add_entities(pets, True)

class WhistleTracker(TrackerEntity):
    """Representation of Whistle Device Tracker"""

    def __init__(self, pet, whistle):
        """ Build WhistleTracker
            whistle = aiohttp session
            pet = initially-fetched pet data
        """
        self._whistle = whistle
        self._pet_id = pet['id']
        self._device_id = pet['device']['serial_number']
        self._available = False
        self._pet_update(pet)
        self._failed_update = False

    def _pet_update(self, pet):
        self._available = True
        self._name = pet['name']
        self._species = pet['profile']['species']
        self._latitude = pet['last_location']['latitude']
        self._longitude = pet['last_location']['longitude']
        self._location_accuracy = pet['last_location']['uncertainty_meters']
        self._location_address = pet['last_location']['description']['address']
        self._device_id = pet['device']['serial_number']
        time_zone = pet['profile']['time_zone_name']
        self._last_check_in = datetime.fromisoformat(pet['device']['last_check_in'].replace(' ' + time_zone, '')).replace(tzinfo=ZoneInfo(time_zone)).astimezone()
        self._battery_level = pet['device']['battery_level']
        self._battery_status = pet['device']['battery_status']
        self._pending_locate = pet['device']['pending_locate']
        self._activity_streak = pet['activity_summary']['current_streak']
        self._activity_minutes_active = pet['activity_summary']['current_minutes_active']
        self._activity_minutes_rest = pet['activity_summary']['current_minutes_rest']
        self._activity_goal = pet['activity_summary']['current_activity_goal']['minutes']
        self._current_place_id = pet['last_location']['place']['id']

    def _device_dailies_places_update(self, device, dailies, places):
        self._battery_days_left = device['device']['battery_stats']['battery_days_left']
        self._24h_battery_wifi_usage = round(((float(device['device']['battery_stats']['prior_usage_minutes']['24h']['power_save_mode']) / 1440) * 100), 0)
        self._24h_battery_cellular_usage = round(((float(device['device']['battery_stats']['prior_usage_minutes']['24h']['cellular']) / 1440) * 100), 0)
        self._activity_distance = round(dailies['dailies'][0]['distance'], 1)
        self._activity_calories = round(dailies['dailies'][0]['calories'], 1)
        self._places = places


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
    def extra_state_attributes(self) -> dict:
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
        """ Retrieve latest data from Whistle Servers """
        _LOGGER.info('Updating Whistle data')
        try:
            await self._whistle.async_init()
            get_pet = await self._whistle.get_pet(self._pet_id)
            device = await self._whistle.get_device(self._device_id)
            dailies = await self._whistle.get_dailies(self._pet_id)
            places = await self._whistle.get_places()
        except Exception as e:
            if self._failed_update:
                _LOGGER.warning(
                    "Failed to update data for device '%s' from Whistle servers",
                    self.name,
                )
                self._available = False
                self.async_write_ha_state()
                return

            _LOGGER.debug("First failed data update for device '%s'", self.name)
            self._failed_update = True
            return
        pet = get_pet['pet']
        self._failed_update = False
        self._pet_update(pet)
        self._device_dailies_places_update(device, dailies, places)
