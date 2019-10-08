#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

import os.path
import os

# Import project libraries
from pattoo.shared import general
from pattoo.shared import log
from pattoo.shared import configuration
from pattoo.os.pattoo import API_EXECUTABLE


class ConfigAPI(configuration.ConfigAPI):
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate the Config parent
        configuration.ConfigAPI.__init__(self)

        # Update the configuration directory
        config_directory = '{}/etc/pattoo-os.d'.format(
            general.root_directory())

        # Return data
        self._config_pattoo_os = general.read_yaml_files(config_directory)

    def listen_address(self):
        """Get listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = API_EXECUTABLE
        sub_key = 'listen_address'
        result = configuration.search(
            key, sub_key, self._config_pattoo_os, die=False)

        # Default to 0.0.0.0
        if result is None:
            result = '0.0.0.0'
        return result

    def bind_port(self):
        """Get bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = API_EXECUTABLE
        sub_key = 'bind_port'
        intermediate = configuration.search(
            key, sub_key, self._config_pattoo_os, die=False)

        # Default to 6000
        if intermediate is None:
            result = 5000
        else:
            result = int(intermediate)
        return result
