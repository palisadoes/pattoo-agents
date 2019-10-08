#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

import os.path
import os

# Import project libraries
from pattoo.shared import files
from pattoo.shared import log
from pattoo.shared import configuration
from pattoo.os.pattoo import PATTOO_OS_SPOKED, PATTOO_OS_HUBD


class ConfigSpoked(configuration.ConfigSpoked):
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate the Config parent
        configuration.ConfigSpoked.__init__(self)

        # Update the configuration directory
        config_directory = '{}/etc/pattoo-os.d'.format(
            files.root_directory())

        # Return data
        self._config_pattoo_os = files.read_yaml_files(config_directory)

    def listen_address(self):
        """Get listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_OS_SPOKED
        sub_key = 'listen_address'
        result = configuration.search(
            key, sub_key, self._config_pattoo_os, die=False)

        # Default to 0.0.0.0
        if result is None:
            result = '0.0.0.0'
        return result

    def ip_bind_port(self):
        """Get ip_bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_OS_SPOKED
        sub_key = 'ip_bind_port'
        intermediate = configuration.search(
            key, sub_key, self._config_pattoo_os, die=False)

        # Default to 6000
        if intermediate is None:
            result = 5000
        else:
            result = int(intermediate)
        return result


class ConfigHubd(configuration.ConfigHubd):
    """Class for PATTOO_OS_HUBD configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate the Config parent
        configuration.ConfigHubd.__init__(self)

        # Update the configuration directory
        config_directory = '{}/etc/pattoo-os.d'.format(
            files.root_directory())

        # Return data
        self._config_pattoo_os = files.read_yaml_files(config_directory)

    def ip_devices(self):
        """Get devices.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_OS_HUBD
        sub_key = 'ip_devices'
        result = configuration.search(
            key, sub_key, self._config_pattoo_os, die=True)
        return result
