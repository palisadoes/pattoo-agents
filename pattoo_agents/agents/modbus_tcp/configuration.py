#!/usr/bin/env python3
"""Classe to manage SNMP agent configurations."""

# Standard imports
from copy import deepcopy

# Import project libraries
from pattoo_shared import configuration
from pattoo_shared.configuration import Config
from pattoo_shared.constants import PATTOO_AGENT_MODBUSTCPD
from .variables import RegisterVariable


class ConfigMODBUSTCP(Config):
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

    def registervariables(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of RegisterVariable items

        """
        # Initialize key variables
        result = []

        # Get configuration snippet
        key = PATTOO_AGENT_MODBUSTCPD
        sub_key = 'polling_groups'
        sub_config = configuration.search(
            key, sub_key, self._configuration, die=True)

        # Create snmp objects
        groups = _validate_registers(sub_config)
        for group in groups:
            registervariable = RegisterVariable(
                registers=group['input_registers'],
                ip_devices=group['ip_devices']
            )
            result.append(registervariable)
        return result


def _validate_registers(config_dict):
    """Get list of dicts of SNMP information in configuration file.

    Args:
        config_dict: Configuration dict

    Returns:
        snmp_data: List of SNMP data dicts found in configuration file.

    """
    # Initialize key variables
    seed_dict = {}
    seed_dict['ip_devices'] = []
    seed_dict['input_registers'] = []

    # Start populating information
    data = []
    for read_dict in config_dict:
        # Next entry if this is not a dict
        if isinstance(read_dict, dict) is False:
            continue

        # Assign data
        new_dict = deepcopy(seed_dict)
        for key in read_dict.keys():
            if isinstance(read_dict[key], list) is True:
                new_dict[key] = read_dict[key]

        # Validate IP addresses and OIDs
        if isinstance(new_dict['ip_devices'], list) is False:
            continue
        if isinstance(new_dict['input_registers'], list) is False:
            continue

        # Append data to list
        data.append(new_dict)

    # Return
    return data
