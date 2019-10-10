#!/usr/bin/env python3
"""Pattoo classes that manage various configurations."""

import os.path
import os
import yaml

# Import project libraries
from pattoo import files
from pattoo import log
from pattoo import configuration
from pattoo.configuration import Config 
from pattoo import files
from pattoo.agents.os.pattoo import PATTOO_OS_SPOKED, PATTOO_OS_HUBD


class ConfigSpoked(Config):
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate the Config parent
        Config.__init__(self)

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

    def translations(self, agent_program):
        """Get translations.

        Args:
            agent_program: Agent program

        Returns:
            result: result

        """
        # Intialize key variables
        result = {}
        language = self.language()
        filepath = (
            '{0}{1}metadata{1}language{1}agents{1}{2}{1}{3}.yaml'
            ''.format(
                files.root_directory(), os.sep, language, agent_program))

        # Read data
        if os.path.isfile(filepath) is False:
            log_message = (
                'Translation file {} for language {} does not exist.'
                ''.format(filepath, language))
            log.log2die(1022, log_message)

        # Load yaml file
        with open(filepath, 'r') as stream:
            try:
                data_dict = yaml.safe_load(stream)
            except:
                log_message = 'Unable to read file {}.'.format(filepath)
                log.log2die(1022, log_message)

        # Get data
        if 'agent_source_descriptions' in data_dict:
            result = data_dict['agent_source_descriptions']

        # Return
        return result


class ConfigHubd(Config):
    """Class for PATTOO_OS_HUBD configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate the Config parent
        Config.__init__(self)

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
