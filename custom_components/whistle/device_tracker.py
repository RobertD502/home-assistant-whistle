""" Device Tracker platform for Whistle integration."""
from __future__ import annotations

from typing import Any

from whistleaio.model import Pet

from homeassistant.components.device_tracker.const import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_ZONE_METHOD,
    DEFAULT_ZONE_METHOD,
    DOMAIN,
    WHISTLE_COORDINATOR,
)
from .coordinator import WhistleDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """ Set Up Whistle Device Tracker Entities. """

    coordinator: WhistleDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][WHISTLE_COORDINATOR]

    device_trackers = []


    for pet_id, pet_data in coordinator.data.pets.items():

            """ Device Trackers """
            if pet_data.data['device'] and pet_data.data['device']['has_gps']:
                device_trackers.extend((
                        WhistleTracker(coordinator, pet_id, entry),
                    ))
    async_add_entities(device_trackers)

class WhistleTracker(CoordinatorEntity, TrackerEntity):
    """ Representation of Whistle GPS Tracker. """

    def __init__(self, coordinator, pet_id, entry):
        super().__init__(coordinator)
        self.pet_id = pet_id
        self.entry = entry

    @property
    def zone_method(self):
        """ Return the zone method. """
        
        return self.entry.options[CONF_ZONE_METHOD]

    @property
    def pet_data(self) -> Pet:
        """ Handle coordinator pet data. """

        return self.coordinator.data.pets[self.pet_id]

    @property
    def location_dict(self) -> dict[int, str]:
        """ Create a dictionary for all pre-defined Whistle
        locations as a dict of location id: location name.
        """

        locations: dict[int, str] = {}
        for place in self.pet_data.places:
            locations[place['id']] = place['name']

        return locations

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

        return str(self.pet_data.id) + '_tracker'

    @property
    def name(self) -> str:
        """ Return name of the entity. """

        return "Whistle tracker"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined. """

        return True

    @property
    def icon(self):
        """ Determine what icon to use. """

        if self.pet_data.data['profile']['species'] == 'dog':
            return 'mdi:dog'
        if self.pet_data.data['profile']['species'] == 'cat':
            return 'mdi:cat'

    @property
    def source_type(self) -> SourceType:
        """ Return GPS as the source. """

        return SourceType.GPS

    @property
    def latitude(self) -> float:
        """ Return most recent latitude. """

        return self.pet_data.data['last_location']['latitude']

    @property
    def longitude(self) -> float:
        """ Return most recent longitude. """

        return self.pet_data.data['last_location']['longitude']

    @property
    def battery_level(self) -> int:
        """ Return tracker current battery percent. """

        return self.pet_data.data['device']['battery_level']

    @property
    def location_accuracy(self) -> int:
        """ Return last location gps accuracy. """

        return int(self.pet_data.data['last_location']['uncertainty_meters'])

    @property
    def location_name(self) -> str | None:
        """Returns the Whistle location, as defined in the app,
        if zone method is set to Whistle.If the tracker is not in
        a pre-defined location, location of Away is returned.
        If zone method is set to Home Assistant, Home Assistant
        zones will be used instead.
        """
        
        if self.zone_method == DEFAULT_ZONE_METHOD:
            if self.pet_data.data['last_location']['place']['status'] == 'outside_geofence_range':
                return "Away"
            elif self.pet_data.data['last_location']['place']['id']:
                location_id = self.pet_data.data['last_location']['place']['id']
                return self.location_dict.get(location_id)
            else:
                return "Away"
        else:
            return None
