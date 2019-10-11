#!/usr/bin/env python3
"""Pattoo helper for the Linux _data.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
import socket
from pprint import pprint

# Pattoo libraries
from pattoo.agents.snmp import configuration
from pattoo.agents.snmp import snmp
from pattoo import data
from pattoo.variables import DataVariableList
from pattoo.constants import PATTOO_SNMPD


def poll():
    """Get PATOO_SNMP agent data.

    Performance data from SNMP enabled devices.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    agent_program = PATTOO_SNMPD
    device = socket.getfqdn()
    config = configuration.ConfigSNMP()
    translations = {}
    ip_devices = {}
    oids4devices = {}

    # Intialize data gathering
    _data = DataVariableList(device, translations)

    # Get SNMP OIDs to be polled (Along with authorizations and ip_devices)
    snmpvariables = config.snmpvariables()
    oidvariables = config.oidvariables()

    # Create a dict of snmpvariables keyed by ip_device
    for snmpvariable in snmpvariables:
        ip_devices[snmpvariable.ip_device] = snmpvariable

    # Create a dict of oid lists keyed by ip_device
    for oidvariable in oidvariables:
        for next_device in oidvariable.ip_devices:
            if next_device in oids4devices:
                oids4devices[next_device].extend(oidvariable.oids)
            else:
                oids4devices[next_device] = oidvariable.oids

    # Poll oids for all devices and update the DataVariableList
    _snmpwalks(_data, ip_devices, oids4devices)

    # Return data
    process = data.Data(agent_program, _data)
    result = process.data()
    return result


def _snmpwalks(_data, ip_devices, oids4devices):
    """Get PATOO_SNMP agent data.

    Update the DataVariableList with DataVariables

    Args:
        _data: DataVariableList that holds SNMP polling data
        ip_devices: Dict of SNMPVariables keyed by ip_device
        oids4devices: Dict of OID lists keyed by ip_device

    Returns:
        None

    """
    # Poll all devices in sequence
    for ip_device, snmpvariable in sorted(ip_devices.items()):
        if ip_device in oids4devices:
            # Setup the query
            query = snmp.SNMP(snmpvariable)

            # Poll OIDs
            for oid in oids4devices[ip_device]:
                datavariables = query.walk(oid)
                for datavariable in datavariables:
                    _data.append(datavariable)
