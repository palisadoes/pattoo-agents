#!/usr/bin/env python3
"""switchmap.classes that manage various configurations."""

# Standard imports
from copy import deepcopy

# Import project libraries
from pattoo.configuration import Config
from pattoo import configuration
from pattoo.variables import SNMPAuth, SNMPVariableList, OIDVariable
from pattoo.constants import PATTOO_SNMPD


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

    def snmpvariables(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of SNMPVariable items

        """
        # Initialize key variables
        result = []

        # Get configuration snippet
        key = PATTOO_SNMPD
        sub_key = 'snmp_groups'
        sub_config = configuration.search(
            key, sub_key, self._configuration, die=True)

        # Create snmp objects
        groups = _validate_snmp(sub_config)
        for group in groups:
            # Save the authentication parameters
            snmpauth = SNMPAuth(
                version=group['snmp_version'],
                community=group['snmp_community'],
                port=group['snmp_port'],
                secname=group['snmp_secname'],
                authprotocol=group['snmp_authprotocol'],
                authpassword=group['snmp_authpassword'],
                privprotocol=group['snmp_privprotocol'],
                privpassword=group['snmp_privpassword']
            )

            # Create the SNMPVariableList
            snmpvariablelist = SNMPVariableList(snmpauth, group['ip_devices'])
            snmpvariables = snmpvariablelist.snmpvariables
            result.extend(snmpvariables)

        # Return
        return result

    def oidvariables(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of OIDVariable items

        """
        # Initialize key variables
        result = []

        # Get configuration snippet
        key = PATTOO_SNMPD
        sub_key = 'oid_groups'
        sub_config = configuration.search(
            key, sub_key, self._configuration, die=True)

        # Create snmp objects
        groups = _validate_oids(sub_config)
        for group in groups:
            oidvariable = OIDVariable(
                oids=group['oids'],
                ip_devices=group['ip_devices']
            )
            result.append(oidvariable)
        return result


def _validate_snmp(config_dict):
    """Get list of dicts of SNMP information in configuration file.

    Args:
        config_dict: Configuration dict

    Returns:
        data: List of SNMP data dicts found in configuration file.

    """
    # Initialize key variables
    seed_dict = {}
    seed_dict['snmp_version'] = 2
    seed_dict['snmp_secname'] = None
    seed_dict['snmp_community'] = 'public'
    seed_dict['snmp_authprotocol'] = None
    seed_dict['snmp_authpassword'] = None
    seed_dict['snmp_privprotocol'] = None
    seed_dict['snmp_privpassword'] = None
    seed_dict['snmp_port'] = 161
    seed_dict['ip_devices'] = []

    # Start populating information
    data = []
    for read_dict in config_dict:
        # Next entry if this is not a dict
        if isinstance(read_dict, dict) is False:
            continue

        # Assign data
        new_dict = deepcopy(seed_dict)
        for key in read_dict.keys():
            new_dict[key] = read_dict[key]

        # Verify the correct version keys
        if new_dict['snmp_version'] not in [2, 3]:
            continue

        # Validate IP addresses and OIDs
        if isinstance(new_dict['ip_devices'], list) is False:
            continue

        # Append data to list
        data.append(new_dict)

    # Return
    return data


def _validate_oids(config_dict):
    """Get list of dicts of SNMP information in configuration file.

    Args:
        config_dict: Configuration dict

    Returns:
        snmp_data: List of SNMP data dicts found in configuration file.

    """
    # Initialize key variables
    nothing = []
    seed_dict = {}
    seed_dict['ip_devices'] = []
    seed_dict['oids'] = []

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
        if isinstance(new_dict['oids'], list) is False:
            continue

        # Append data to list
        data.append(new_dict)

    # Return
    return data
