""" Constants for Whistle """

import asyncio
import logging

from aiohttp.client_exceptions import ClientConnectionError

from homeassistant.const import Platform

from whistleaio.exceptions import WhistleAuthError

LOGGER = logging.getLogger(__package__)

DEFAULT_SCAN_INTERVAL = 60
DOMAIN = "whistle"
PLATFORMS = [
    Platform.DEVICE_TRACKER,
    Platform.SENSOR,
]

DEFAULT_NAME = "Whistle"
TIMEOUT = 20

WHISTLE_ERRORS = (
    asyncio.TimeoutError,
    ClientConnectionError,
    WhistleAuthError,
)
