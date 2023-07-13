""" DataUpdateCoordinator for the Whistle integration. """
from __future__ import annotations

from datetime import timedelta

from whistleaio import WhistleClient
from whistleaio.exceptions import WhistleAuthError, WhistleError
from whistleaio.model import WhistleData


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER, TIMEOUT

class WhistleDataUpdateCoordinator(DataUpdateCoordinator):
    """ Whistle Data Update Coordinator. """

    data: WhistleData

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """ Initialize the Whistle coordinator. """

        self.client = WhistleClient(
            entry.data[CONF_EMAIL],
            entry.data[CONF_PASSWORD],
            session=async_get_clientsession(hass),
            timeout=TIMEOUT,
        )
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> WhistleData:
        """ Fetch data from Whistle. """

        try:
            data = await self.client.get_whistle_data()
        except WhistleAuthError as error:
            raise ConfigEntryAuthFailed from error
        except WhistleError as error:
            raise UpdateFailed(error) from error
        except Exception as error:
            raise UpdateFailed(error) from error
        if not data.pets:
            raise UpdateFailed("No Pets found")
        return data
