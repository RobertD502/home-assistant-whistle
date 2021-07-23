"""Whistle Sensor Platform"""
import logging
import aiohttp
from datetime import timedelta, datetime
from homeassistant.exceptions import PlatformNotReady
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=120)

_LOGGER = logging.getLogger(__name__)

"""Attributes"""

ATTR_START_TIME = "start_time"
ATTR_END_TIME = "end_time"
ATTR_DURATION = "duration"
ATTR_DISTANCE = "distance"
ATTR_CALORIES = "calories"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Whistle event sensor."""
    whistle = hass.data[DOMAIN]
    pets = []
    try:
        await whistle.async_init()
        get_pets = await whistle.get_pets()
    except Exception as e:
        _LOGGER.error("Failed to get pets from Whistle servers")
        raise PlatformNotReady from e

    for pet in get_pets["pets"]:
        pets.append(WhistleEventSensor(pet, whistle))

    async_add_entities(pets, True)

class WhistleEventSensor(SensorEntity):
    """Representation of Whistle Event Sensor"""

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

    def _daily_items_update(self, daily_items):
        self._event_title = daily_items['daily_items'][0]['title']
        self._start_time = datetime.fromisoformat(daily_items['daily_items'][0]['start_time'].replace('Z', '+00:00')).astimezone()
        self._end_time = datetime.fromisoformat(daily_items['daily_items'][0]['end_time'].replace('Z', '+00:00')).astimezone()
        self._duration = daily_items['daily_items'][0]['data']['duration']
        self._distance = daily_items['daily_items'][0]['data']['distance']
        self._calories = daily_items['daily_items'][0]['data']['calories']

    @property
    def should_poll(self):
        return True

    @property
    def unique_id(self):
        """Set ID to serial number of the Whistle Device"""
        return self._device_id

    @property
    def name(self):
        """Sensor entity name"""
        return "whistle_" + self._name + "_event"

    @property
    def icon(self):
        """Determine what icon to use"""
        if self._species == 'dog':
            return 'mdi:dog'
        if self._species == 'cat':
            return 'mdi:cat'

    @property
    def state(self):
        return self._event_title

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def duration(self):
        return self._duration

    @property
    def distance(self):
        return self._distance

    @property
    def calories(self):
        return self._calories

    @property
    def available(self):
        return self._available

    @property
    def device_state_attributes(self) -> dict:
        """Return attributes."""
        return {
            ATTR_START_TIME: self.start_time,
            ATTR_END_TIME: self.end_time,
            ATTR_DURATION: self.duration,
            ATTR_DISTANCE: self.distance,
            ATTR_CALORIES: self.calories,
        }

    async def async_update(self):
        """ Retrieve latest data from Whistle Servers """
        _LOGGER.info('Updating Whistle event data')
        try:
            await self._whistle.async_init()
            dailies = await self._whistle.get_dailies(self._pet_id)
            daily_items = await self._whistle.get_dailies_daily_items(self._pet_id, dailies['dailies'][0]['day_number'])
        except Exception as e:
            if self._failed_update:
                _LOGGER.warning(
                    "Failed to update event data for device '%s' from Whistle servers",
                    self.name,
                )
                self._available = False
                self.async_write_ha_state()
                return

            _LOGGER.debug("First failed event data update for device '%s'", self.name)
            self._failed_update = True
            return
        if len(daily_items['daily_items']) > 0:
            self._daily_items_update(daily_items)
            self._available = True
            self._failed_update = False
        else:
            _LOGGER.info("No event found to report. This occurs at midnight. '%s' sensor will become available once an event has been reported to the Whistle servers.", self.name)
            self._available = False
        
