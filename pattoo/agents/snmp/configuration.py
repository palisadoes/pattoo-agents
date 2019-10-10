#!/usr/bin/env python3
"""switchmap.classes that manage various configurations."""

import os.path
import os
import multiprocessing

# Import project libraries
from pattoo import log
from pattoo import files
from pattoo.configuration import Config


class ConfigSNMP(Config):
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
        config_directory = '{}/etc/pattoo-snmp.d'.format(
            files.root_directory())

        # Return
        self.config_dict = files.read_yaml_files(config_directory)

    def hostnames(self):
        """Get hostnames.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        result = []

        # Get config
        key = 'main'
        sub_key = 'hostnames'
        agent_config = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Get result
        if isinstance(agent_config, list) is True:
            agent_config = list(set(agent_config))
            result = sorted(agent_config)

        # Return
        return result


class _ConfigSNMP(object):
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        hosts:
        snmp_auth:
    """

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.none = None
        self.root_directory = files.root_directory()
        # Update the configuration directory
        # 'SWITCHMAP_CONFIGDIR' is used for unittesting
        if 'SWITCHMAP_CONFIGDIR' in os.environ:
            config_directory = os.environ['SWITCHMAP_CONFIGDIR']
        else:
            config_directory = '{}/etc'.format(self.root_directory)
        directories = [config_directory]

        # Return
        self.config_dict = files.read_yaml_files(directories)

    def snmp_auth(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            snmp_data: List of SNMP data dicts found in configuration file.

        """
        # Initialize key variables
        seed_dict = {}
        seed_dict['snmp_version'] = 2
        seed_dict['snmp_secname'] = None
        seed_dict['snmp_community'] = None
        seed_dict['snmp_authprotocol'] = None
        seed_dict['snmp_authpassword'] = None
        seed_dict['snmp_privprotocol'] = None
        seed_dict['snmp_privpassword'] = None
        seed_dict['snmp_port'] = 161
        seed_dict['group_name'] = None
        seed_dict['enabled'] = True

        # Read configuration's SNMP information. Return 'None' if none found
        if 'snmp_groups' in self.config_dict:
            if isinstance(self.config_dict['snmp_groups'], list) is True:
                if len(self.config_dict['snmp_groups']) < 1:
                    return None
            else:
                return None

        # Start populating information
        snmp_data = []
        for read_dict in self.config_dict['snmp_groups']:
            # Next entry if this is not a dict
            if isinstance(read_dict, dict) is False:
                continue

            # Assign good data
            new_dict = {}
            for key, _ in seed_dict.items():
                if key in read_dict:
                    new_dict[key] = read_dict[key]
                else:
                    new_dict[key] = seed_dict[key]

            # Convert relevant strings to integers
            new_dict['snmp_version'] = int(new_dict['snmp_version'])
            new_dict['snmp_port'] = int(new_dict['snmp_port'])

            # Append data to list
            snmp_data.append(new_dict)

        # Return
        return snmp_data

    def dont_use(self):
        """Dummy method to pass linter.

        Args:
            None

        Returns:
            none: Nothing

        """
        # Initialize key variables
        none = self.none
        return none


def _agent_config(agent_name, config_dict):
    """Get agent config parameter from YAML.

    Args:
        agent_name: Agent Name
        config_dict: Dictionary to explore
        die: Die if true and the result encountered is None

    Returns:
        result: result

    """
    # Get result
    key = 'agents'
    result = None

    # Get new result
    if key in config_dict:
        configurations = config_dict[key]
        for configuration in configurations:
            if 'agent_name' in configuration:
                if configuration['agent_name'] == agent_name:
                    result = configuration
                    break

    # Error if not configured
    if result is None:
        log_message = (
            'Agent {} not defined in configuration in '
            'agents:{} section'.format(key, key))
        log.log2die(1094, log_message)

    # Return
    return result


def _key_sub_key(key, sub_key, config_dict, die=True):
    """Get config parameter from YAML.

    Args:
        key: Primary key
        sub_key: Secondary key
        config_dict: Dictionary to explore
        die: Die if true and the result encountered is None

    Returns:
        result: result

    """
    # Get result
    result = None

    # Verify config_dict is indeed a dict.
    # Die safely as log_directory is not defined
    if isinstance(config_dict, dict) is False:
        log.log2die_safe(1021, 'Invalid configuration file. YAML not found')

    # Get new result
    if key in config_dict:
        # Make sure we don't have a None value
        if config_dict[key] is None:
            log_message = (
                'Configuration value {}: is blank. Please fix.'
                ''.format(key))
            log.log2die_safe(1037, log_message)

        # Get value we need
        if sub_key in config_dict[key]:
            result = config_dict[key][sub_key]

    # Error if not configured
    if result is None and die is True:
        log_message = (
            '{}:{} not defined in configuration'.format(key, sub_key))
        log.log2die_safe(1016, log_message)

    # Return
    return result
