#!/usr/bin/env python3
"""Classe to manage SNMP agent configurations."""
# Import project libraries
from pattoo_shared import configuration
from pattoo_shared.configuration import Config
from pattoo_shared.constants import PATTOO_AGENT_MODBUSTCPD
from pattoo_agents.agents.modbus.variables import (
    InputRegisterVariable, HoldingRegisterVariable, DeviceRegisterVariables)


class ConfigModbusTCP(Config):
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
        groups = configuration.search(
            key, sub_key, self._configuration, die=True)

        # Create Tuple instance to populate
        result = []

        # Create snmp objects
        for group in groups:
            for register in ['input_registers', 'holding_registers']:
                if register in group:
                    result.extend(_create_drv(group, register))
        return result


def _create_drv(data, register_type):
    """Create a list of DeviceRegisterVariables for polling.

    Args:
        data: Configuration dict

    Returns:
        result: list of DeviceRegisterVariables

    """
    # Initialize key variables
    result = []

    # Only return valid value
    if isinstance(data, dict) is True:
        # Screen data for keys and correct type
        if (register_type not in 'input_registers') and (
                register_type not in 'holding_registers'):
            return []
        if isinstance(data['ip_devices'], list) is False and isinstance(
                data[register_type], list) is False:
            return []

        # Process
        for ip_device in data['ip_devices']:
            variables = []
            for register in data[register_type]:
                if register_type == 'holding_registers':
                    variables.append(HoldingRegisterVariable(register))
                else:
                    variables.append(InputRegisterVariable(register))
            drv = DeviceRegisterVariables(ip_device)
            drv.add(variables)
            result.append(drv)

    # Return
    return result
