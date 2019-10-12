#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

import os
import yaml

# Import project libraries
from pattoo import configuration
from pattoo.configuration import Config
from pattoo.constants import PATTOO_OS_SPOKED, PATTOO_OS_HUBD


class ConfigSpoked(Config):
    """Class gathers all configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_OS_SPOKED constant

    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate the Config parent
        Config.__init__(self)

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
            key, sub_key, self._configuration, die=False)

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
            key, sub_key, self._configuration, die=False)

        # Default to 6000
        if intermediate is None:
            result = 5000
        else:
            result = int(intermediate)
        return result


class ConfigHubd(Config):
    """Class for PATTOO_OS_HUBD configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_OS_HUBD constant

    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate the Config parent
        Config.__init__(self)

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
            key, sub_key, self._configuration, die=True)
        return result
