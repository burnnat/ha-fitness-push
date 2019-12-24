"""The Fitness Push component."""
__version__ = '0.0.1'

import logging

_LOGGER = logging.getLogger(__name__)

FITBIT_DOMAIN = 'fitbit'
POLAR_DOMAIN = 'polar'

ATTR_DATA = 'data'

def setup(hass, config):

    def handle_fitbit_push(call):
        data = call.data.get(ATTR_DATA, None)
        # _LOGGER.log(...)

    hass.services.register(FITBIT_DOMAIN, 'push_data', handle_fitbit_push)

    def handle_polar_push(call):
        data = call.data.get(ATTR_DATA, None)
        # _LOGGER.log(...)

    hass.services.register(POLAR_DOMAIN, 'push_data', handle_polar_push)

    # Return boolean to indicate that initialization was successfully.
    return True