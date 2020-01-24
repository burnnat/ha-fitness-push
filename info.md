## Overview
Custom component exposing Home Assistant services to push fitness data to cloud services.

## Requirements

To push to Fitbit, you must have the [standard Fitbit integration for Home Assistant](https://www.home-assistant.io/integrations/fitbit/) enabled and configured. The existing authentication and configuration information will be reused by this integration.

To push to Polar Flow, no additional requirements are necessary. You may still wish to install the [Polar Flow sensor integration](https://github.com/burnnat/ha-polar), however authorization will be performed separately via web client username and password in place of OAuth.

## Configuration:
```
fitness_push:
    fitbit:
    polar:
        username: user@example.com
        password: !secret polar_password
```
