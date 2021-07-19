"""Whistle Component Setup"""
import asyncio
import logging
import voluptuous as vol
from pywhistle import Client

from homeassistant.helpers import aiohttp_client, config_validation as cv
from homeassistant import config_entries
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME
)
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Setup of the component"""
    return True


async def async_setup_entry(hass, config_entry):
    """Set up Whistle integration from a config entry."""
    username = config_entry.data.get(CONF_USERNAME)
    password = config_entry.data.get(CONF_PASSWORD)

    _LOGGER.info("Initializing the Whistle API")
    websession = aiohttp_client.async_get_clientsession(hass)
    whistle = Client(username, password, websession)
    _LOGGER.info("Connected to Whistle API")

    hass.data[DOMAIN] = whistle

    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(config_entry, "device_tracker")
    )

    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )

    return True
