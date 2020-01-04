#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

# Standard imports
import os

# Import project libraries
from pattoo_shared import configuration
from pattoo_shared.configuration import Config
from pattoo_shared import files, log
from .constants import (
    PATTOO_AGENT_OS_SPOKED, PATTOO_AGENT_OS_HUBD, PATTOO_AGENT_OS_AUTONOMOUSD)


class ConfigSpoked(Config):
    """Class gathers all configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_AGENT_OS_SPOKED constant

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

    def ip_listen_address(self):
        """Get ip_listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_OS_SPOKED
        sub_key = 'ip_listen_address'
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
        key = PATTOO_AGENT_OS_SPOKED
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
    """Class for PATTOO_AGENT_OS_HUBD configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_AGENT_OS_HUBD constant

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

    def ip_targets(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_OS_HUBD
        sub_key = 'ip_targets'
        result = configuration.search(
            key, sub_key, self._configuration, die=True)
        return result


class ConfigAutonomousd(object):
    """Class for PATTOO_AGENT_OS_AUTONOMOUSD configuration information.

    Only processes the following YAML keys in the configuration file:

        The value of the PATTOO_AGENT_OS_AUTONOMOUSD constant

    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Get the configuration directory
        # Expand linux ~ notation for home directories if provided.
        _config_directory = log.check_environment()
        config_directory = os.path.expanduser(_config_directory)
        config_file = '{}{}{}.yaml'.format(
            config_directory, os.sep, PATTOO_AGENT_OS_AUTONOMOUSD)
        self._configuration = files.read_yaml_file(config_file)

    def polling_interval(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_OS_AUTONOMOUSD
        sub_key = 'polling_interval'
        intermediate = configuration.search(
            key, sub_key, self._configuration, die=False)

        # Default to 300
        if bool(intermediate) is False:
            result = 300
        else:
            result = abs(int(intermediate))
        return result
