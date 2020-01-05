#!/usr/bin/env python3
"""Classe to manage SNMP agent configurations."""

# Standard imports
from copy import deepcopy
import os

# Import project libraries
from pattoo_shared import configuration, files, log
from pattoo_shared.variables import IPTargetPollingPoints
from .constants import PATTOO_AGENT_SNMPD, PATTOO_AGENT_SNMP_IFMIBD
from .variables import SNMPAuth, SNMPVariableList


class ConfigSNMP(object):
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Get the configuration directory
        config_file = configuration.agent_config_filename(
            PATTOO_AGENT_SNMPD)
        self._configuration = files.read_yaml_file(config_file)

    def snmpvariables(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of SNMPVariable items

        """
        # Get result
        result = _snmpvariables(PATTOO_AGENT_SNMPD, self._configuration)
        return result

    def target_polling_points(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of IPTargetPollingPoints objects

        """
        # Get result
        result = _target_polling_points(
            PATTOO_AGENT_SNMPD, self._configuration)
        return result

    def polling_interval(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = _polling_interval(PATTOO_AGENT_SNMPD, self._configuration)
        return result


class ConfigSNMPIfMIB(object):
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Get the configuration directory
        config_file = configuration.agent_config_filename(
            PATTOO_AGENT_SNMP_IFMIBD)
        self._configuration = files.read_yaml_file(config_file)

    def snmpvariables(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of SNMPVariable items

        """
        # Get result
        result = _snmpvariables(PATTOO_AGENT_SNMP_IFMIBD, self._configuration)
        return result

    def target_polling_points(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of IPTargetPollingPoints objects

        """
        # Get result
        result = _target_polling_points(
            PATTOO_AGENT_SNMP_IFMIBD, self._configuration)
        return result

    def polling_interval(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = _polling_interval(
            PATTOO_AGENT_SNMP_IFMIBD, self._configuration)
        return result


def _target_polling_points(key, _configuration):
    """Get list of dicts of SNMP information in configuration file.

    Args:
        group: Group name to filter results by

    Returns:
        result: List of IPTargetPollingPoints objects

    """
    # Initialize key variables
    result = []
    datapoint_key = 'oids'

    # Get configuration snippet
    sub_key = 'polling_groups'
    sub_config = configuration.search(key, sub_key, _configuration, die=True)

    # Create snmp objects
    groups = _validate_oids(sub_config)
    for group in groups:
        # Ignore bad values
        if isinstance(group, dict) is False:
            continue

        # Process data
        if 'ip_targets' and datapoint_key in group:
            for ip_target in group['ip_targets']:
                poll_targets = configuration.get_polling_points(
                    group[datapoint_key])
                dpt = IPTargetPollingPoints(ip_target)
                dpt.add(poll_targets)
                if dpt.valid is True:
                    result.append(dpt)
    return result


def _polling_interval(key, _configuration):
    """Get targets.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    sub_key = 'polling_interval'
    value = configuration.search(key, sub_key, _configuration, die=False)

    # Default to 300
    if bool(value) is False:
        result = 300
    else:
        result = abs(int(value))
    return result


def _snmpvariables(key, _configuration):
    """Get list of dicts of SNMP information in configuration file.

    Args:
        group: Group name to filter results by

    Returns:
        result: List of SNMPVariable items

    """
    # Initialize key variables
    result = []

    # Get configuration snippet
    sub_key = 'auth_groups'
    sub_config = configuration.search(key, sub_key, _configuration, die=True)

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
        snmpvariablelist = SNMPVariableList(snmpauth, group['ip_targets'])
        snmpvariables = snmpvariablelist.snmpvariables
        result.extend(snmpvariables)

    # Return
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
    seed_dict['ip_targets'] = []

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
        if isinstance(new_dict['ip_targets'], list) is False:
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
    seed_dict = {}
    seed_dict['ip_targets'] = []
    seed_dict['oids'] = []

    # Start populating information
    data = []

    # Ignore incompatible configuration
    if isinstance(config_dict, list) is False:
        return []

    # Process the stuff
    for read_dict in config_dict:
        # Next entry if this is not a dict
        if isinstance(read_dict, dict) is False:
            continue

        # Assign data
        new_dict = deepcopy(seed_dict)
        for key, value in sorted(read_dict.items()):
            if key not in seed_dict.keys():
                continue
            if isinstance(read_dict[key], list) is True:
                new_dict[key] = value

        # Append data to list
        data.append(new_dict)

    # Return
    return data
