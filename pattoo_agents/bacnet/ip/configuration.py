#!/usr/bin/env python3
"""Classe to manage SNMP agent configurations."""

# Standard imports
import itertools

# Import project libraries
from pattoo_shared import configuration
from pattoo_shared import data as lib_data
from pattoo_shared.variables import DevicePollingTargets
from pattoo_shared.configuration import Config
from pattoo_shared.constants import PATTOO_AGENT_BACNETIPD
from pattoo_agents.modbus.variables import (
    InputRegisterVariable, HoldingRegisterVariable, DeviceRegisterVariables)


class ConfigBACnetIP(Config):
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

    def agent_ip_address(self):
        """Get list polling target information in configuration file..

        Args:
            None

        Returns:
            result: IP address

        """
        # Initialize key variables
        result = []

        # Get configuration snippet
        key = PATTOO_AGENT_BACNETIPD
        sub_key = 'agent_ip_address'
        result = configuration.search(
            key, sub_key, self._configuration, die=True)
        return result

    def device_polling_targets(self):
        """Get list polling target information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of DevicePollingTargets objects

        """
        # Initialize key variables
        result = []
        datapoint_key = 'points'

        # Get configuration snippet
        key = PATTOO_AGENT_BACNETIPD
        sub_key = 'polling_groups'
        groups = configuration.search(
            key, sub_key, self._configuration, die=True)

        # Create snmp objects
        for group in groups:
            # Ignore bad values
            if isinstance(group, dict) is False:
                continue

            # Process data
            if 'ip_devices' and datapoint_key in group:
                for ip_device in group['ip_devices']:
                    poll_targets = self._polling_targets(group[datapoint_key])
                    dpt = DevicePollingTargets(ip_device)
                    dpt.add(poll_targets)
                    result.append(dpt)
        return result
