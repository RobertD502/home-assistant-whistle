""" Config Flow for Whistle integration. """
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from whistleaio.exceptions import WhistleAuthError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_ZONE_METHOD,
    DEFAULT_NAME,
    DEFAULT_ZONE_METHOD,
    DOMAIN,
    ZONE_METHODS,
)

from .util import async_validate_api, NoPetsError

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


class WhistleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ Handle a config flow for Whistle integration. """

    VERSION = 3

    entry: config_entries.ConfigEntry | None

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> WhistleOptionsFlowHandler:
        """Get the options flow for this handler."""
        return WhistleOptionsFlowHandler(config_entry)

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:
        """ Handle re-authentication with Whistle. """

        self.entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """ Confirm re-authentication with Whistle. """

        errors: dict[str, str] = {}

        if user_input:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]
            try:
                await async_validate_api(self.hass, email, password)
            except WhistleAuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except NoPetsError:
                errors["base"] = "no_pets"
            else:
                assert self.entry is not None

                self.hass.config_entries.async_update_entry(
                    self.entry,
                    data={
                        CONF_EMAIL: email,
                        CONF_PASSWORD: password,

                    },
                )
                await self.hass.config_entries.async_reload(self.entry.entry_id)
                return self.async_abort(reason="reauth_successful")
                errors["base"] = "incorrect_email_pass"

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """ Handle the initial step. """

        errors: dict[str, str] = {}

        if user_input:

            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]
            try:
                await async_validate_api(self.hass, email, password)
            except WhistleAuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except NoPetsError:
                errors["base"] = "no_pets"
            else:
                await self.async_set_unique_id(email)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data={CONF_EMAIL: email, CONF_PASSWORD: password},
                    options={CONF_ZONE_METHOD: DEFAULT_ZONE_METHOD},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

class WhistleOptionsFlowHandler(config_entries.OptionsFlow):
    """ Handle Whistle zone options. """

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """ Manage options. """
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Optional(
                CONF_ZONE_METHOD,
                default=self.config_entry.options.get(
                    CONF_ZONE_METHOD, DEFAULT_ZONE_METHOD
                ),
            ): vol.In(ZONE_METHODS)
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
