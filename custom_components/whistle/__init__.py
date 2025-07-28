""" Whistle Component """
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir

from .const import (
    CONF_ZONE_METHOD,
    DEFAULT_ZONE_METHOD,
    DOMAIN,
    LOGGER,
    PLATFORMS,
    UPDATE_LISTENER,
    WHISTLE_COORDINATOR,
)
from .coordinator import WhistleDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Set up Whistle from a config entry. """

    # Create deprecation notification
    ir.async_create_issue(
        hass,
        DOMAIN,
        "whistle_platform_decommission",
        is_fixable=False,
        severity=ir.IssueSeverity.WARNING,
        translation_key="whistle_platform_decommission",
    )

    coordinator = WhistleDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        WHISTLE_COORDINATOR: coordinator
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    update_listener = entry.add_update_listener(async_update_options)
    hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER] = update_listener

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Unload Whistle config entry. """

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        update_listener = hass.data[DOMAIN][entry.entry_id][UPDATE_LISTENER]
        update_listener()
        del hass.data[DOMAIN][entry.entry_id]
        if not hass.data[DOMAIN]:
            del hass.data[DOMAIN]
    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Migrate old entry. """

    if entry.version in [1,2]:
        if entry.version == 1:
            email = entry.data[CONF_USERNAME]
        else:
            email = entry.data[CONF_EMAIL]
        password = entry.data[CONF_PASSWORD]

        LOGGER.debug(f'Migrate Whistle config entry unique id to {email}')
        entry.version = 3

        hass.config_entries.async_update_entry(
            entry,
            data={
                CONF_EMAIL: email,
                CONF_PASSWORD: password,
            },
            options={CONF_ZONE_METHOD: DEFAULT_ZONE_METHOD},
            unique_id=email,
        )
    return True

async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """ Update options. """
    
    await hass.config_entries.async_reload(entry.entry_id)
