"""The Fitness Push component."""
__version__ = '0.0.1'

import logging

_LOGGER = logging.getLogger(__name__)

from fitbit import Fitbit
from homeassistant.components.fitbit import
    FITBIT_CONFIG_FILE,
    ATTR_ACCESS_TOKEN as FITBIT_ATTR_ACCESS_TOKEN,
    ATTR_REFRESH_TOKEN as FITBIT_ATTR_REFRESH_TOKEN,
    ATTR_CLIENT_ID as FITBIT_ATTR_CLIENT_ID,
    ATTR_CLIENT_SECRET as FITBIT_ATTR_CLIENT_SECRET,
    ATTR_LAST_SAVED_AT as FITBIT_ATTR_LAST_SAVED_AT

FITBIT_DOMAIN = 'fitbit'

POLAR_DOMAIN = 'polar'
ATTR_DATA = 'data'

def setup(hass, config):

    fitbit = setup_fitbit(hass)

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

    def handle_polar_log_weight(call):
        data = call.data.get(ATTR_DATA, None)
        # _LOGGER.log(...)

    hass.services.register(POLAR_DOMAIN, 'log_weight', handle_polar_log_weight)

    # Return boolean to indicate that initialization was successfully.
    return True

def setup_fitbit(hass):
    config_path = hass.config.path(FITBIT_CONFIG_FILE)

    if os.path.isfile(config_path):
        config_file = load_json(config_path)
    else
        _LOGGER.error("No Fitbit config file found")
        return None

    access_token = config_file.get(FITBIT_ATTR_ACCESS_TOKEN)
    refresh_token = config_file.get(FITBIT_ATTR_REFRESH_TOKEN)
    expires_at = config_file.get(FITBIT_ATTR_LAST_SAVED_AT)

    if None in (access_token, refresh_token):
        _LOGGER.error("Fitbit config file is not initialized")
        return None

    
    return Fitbit(
        config_file.get(FITBIT_ATTR_CLIENT_ID),
        config_file.get(FITBIT_ATTR_CLIENT_SECRET),
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        refresh_cb=lambda x: None,
    )