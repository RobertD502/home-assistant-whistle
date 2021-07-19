"""Whistle Sensor Platform"""
import logging
from datetime import timedelta, datetime
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

    await whistle.async_init()
    get_pets = await whistle.get_pets()

    pets = []

    for pet in get_pets:
        pets.append(WhistleEventSensor(pet, whistle))

    async_add_entities(pets, True)

class WhistleEventSensor(SensorEntity):
    """Representation of Whistle Event Sensor"""

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
        _LOGGER.info('Updating Whistle Event sensor data')
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
            daily_items = await self._whistle.get_dailies_daily_items(animal['id'], dailies['dailies'][0]['day_number'])
            try:
                self._name = animal['name']
                self._device_id = animal['device']['serial_number']
                self._species = animal['profile']['species']
                self._event_title = daily_items['daily_items'][0]['title']
                self._start_time = datetime.fromisoformat(daily_items['daily_items'][0]['start_time'].replace('Z', '+00:00')).astimezone()
                self._end_time = datetime.fromisoformat(daily_items['daily_items'][0]['end_time'].replace('Z', '+00:00')).astimezone()
                self._duration = daily_items['daily_items'][0]['data']['duration']
                self._distance = daily_items['daily_items'][0]['data']['distance']
                self._calories = daily_items['daily_items'][0]['data']['calories']
            except Exception as e:
                _LOGGER.error("There was an error while updating Whistle Event Sensor: %s", e)
