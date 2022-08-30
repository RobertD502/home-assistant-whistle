""" Utilities for Whistle Integration """
from __future__ import annotations



import async_timeout
from whistleaio import WhistleClient
from whistleaio.exceptions import WhistleAuthError
from whistleaio.model import Pet, WhistleData

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import LOGGER, WHISTLE_ERRORS, TIMEOUT

async def async_validate_api(hass: HomeAssistant, email: str, password: str) -> bool:
    """ Get data from API. """

    client = WhistleClient(
        email,
        password,
        session=async_get_clientsession(hass),
        timeout=TIMEOUT,
    )

    try:
        async with async_timeout.timeout(TIMEOUT):
            whistle_query = await client.get_whistle_data()
    except WhistleAuthError as err:
        LOGGER.error(f'Could not authenticate on Whistle servers: {err}')
        raise WhistleAuthError from err
    except WHISTLE_ERRORS as err:
        LOGGER.error(f'Failed to get information from Whistle servers: {err}')
        raise ConnectionError from err

    pets: dict[str, Pet] = whistle_query.pets
    if not pets:
        LOGGER.error("Could not retrieve any pets from Whistle servers")
        raise NoPetsError
    else:
        return True


class NoPetsError(Exception):
    """ No Pets from Whistle API. """
