""" Whistle Component """
from __future__ import annotations

from whistleaio.exceptions import WhistleAuthError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant

from .const import DOMAIN, LOGGER, PLATFORMS
from .coordinator import WhistleDataUpdateCoordinator
from .util import async_validate_api, NoPetsError


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Set up Whistle from a config entry. """

    coordinator = WhistleDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Unload Whistle config entry. """

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        del hass.data[DOMAIN][entry.entry_id]
        if not hass.data[DOMAIN]:
            del hass.data[DOMAIN]
    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Migrate old entry. """

    if entry.version == 1:
        email = entry.data[CONF_USERNAME]
        password = entry.data[CONF_PASSWORD]

        try:
            await async_validate_api(hass, email, password)
        except (WhistleAuthError, ConnectionError, NoPetsError):
            return False

        entry.version = 2

        LOGGER.debug(f'Migrate Whistle config entry unique id to {email}')
        hass.config_entries.async_update_entry(
            entry,
            data={
                CONF_EMAIL: email,
                CONF_PASSWORD: password,

            },
            unique_id=email,
        )

    return True
