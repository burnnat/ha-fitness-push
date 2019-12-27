"""The Fitness Push component."""
__version__ = '0.0.1'

import logging
import os
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util.json import load_json

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'fitness_push'

FITBIT_DOMAIN = 'fitbit'

POLAR_DOMAIN = 'polar'
POLAR_CONF_EMAIL = 'email'
POLAR_CONF_PASSWORD = 'password'

ATTR_DATA = 'data'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            FITBIT_DOMAIN: {},
            POLAR_DOMAIN: {
                POLAR_CONF_EMAIL: cv.string,
                POLAR_CONF_PASSWORD: cv.string
            }
        }
    },
    extra=vol.ALLOW_EXTRA
)

async def async_setup(hass, config):
    _LOGGER.debug('Initializing fitness push services')
    data = config.get(DOMAIN)

    if FITBIT_DOMAIN in data:
        fitbit = await setup_fitbit(hass, config)

        if fitbit is not None:
            def handle_fitbit_log_weight(call):
                data = call.data.get(ATTR_DATA, None)
                # _LOGGER.log(...)
                """
                https://dev.fitbit.com/build/reference/web-api/body/#log-weight
                """
                url = "{0}/{1}/user/-/body/log/weight.json".format(*fitbit._get_common_args())
                return fitbit.make_request(url, data=data)

            hass.services.register(FITBIT_DOMAIN, 'log_weight', handle_fitbit_log_weight)

    if POLAR_DOMAIN in data:
        polar = await setup_polar(hass, config)

        if polar is not None:
            def handle_polar_log_weight(call):
                data = call.data.get(ATTR_DATA, None)
                # _LOGGER.log(...)
                entry = hass.config_entries.async_entries(POLAR_DOMAIN)[0]
                user_id = entry.data.get(POLAR_CONF_USER_ID)

                await polar.log_weight(user_id, datetime.date(2019, 12, 24), 163.0)

            hass.services.register(POLAR_DOMAIN, 'log_weight', handle_polar_log_weight)

    return True

async def setup_fitbit(hass, config):
    _LOGGER.debug('Initializing Fitbit fitness push services')

    from fitbit import Fitbit
    from homeassistant.components.fitbit.sensor import (
        FITBIT_CONFIG_FILE,
        ATTR_ACCESS_TOKEN as FITBIT_ATTR_ACCESS_TOKEN,
        ATTR_REFRESH_TOKEN as FITBIT_ATTR_REFRESH_TOKEN,
        ATTR_CLIENT_ID as FITBIT_ATTR_CLIENT_ID,
        ATTR_CLIENT_SECRET as FITBIT_ATTR_CLIENT_SECRET,
        ATTR_LAST_SAVED_AT as FITBIT_ATTR_LAST_SAVED_AT)
        
    config_path = hass.config.path(FITBIT_CONFIG_FILE)

    if os.path.isfile(config_path):
        config_file = load_json(config_path)
    else:
        _LOGGER.warn("No Fitbit config file found")
        return None

    access_token = config_file.get(FITBIT_ATTR_ACCESS_TOKEN)
    refresh_token = config_file.get(FITBIT_ATTR_REFRESH_TOKEN)
    expires_at = config_file.get(FITBIT_ATTR_LAST_SAVED_AT)

    if None in (access_token, refresh_token):
        _LOGGER.warn("Fitbit config file is not initialized")
        return None

    return Fitbit(
        config_file.get(FITBIT_ATTR_CLIENT_ID),
        config_file.get(FITBIT_ATTR_CLIENT_SECRET),
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        refresh_cb=lambda x: None,
    )

async def setup_polar(hass, config):
    _LOGGER.debug('Initializing Polar fitness push services')

    from polarweb import PolarWeb

    # TODO: some way to import this constant directly?
    POLAR_CONF_USER_ID = 'user_id'

    data = config.get(DOMAIN).get(POLAR_DOMAIN)
    email = data.get(POLAR_CONF_EMAIL)
    password = data.get(POLAR_CONF_PASSWORD)

    entries = hass.config_entries.async_entries(POLAR_DOMAIN)

    if not entries:
        _LOGGER.warn('Polar integration is not configured')
        return None

    _LOGGER.debug('Setting up Polar web connection with user account: %s', email)

    return PolarWeb(
        async_get_clientsession(hass),
        email,
        password
    )
