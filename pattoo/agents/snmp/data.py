#!/usr/bin/env python3
"""Pattoo helper for the Linux _data.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
import socket
from pprint import pprint
import multiprocessing


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
    datavariables = []

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
    dv_list_per_device = _snmpwalks(ip_devices, oids4devices)
    for datavariable in dv_list_per_device:
        datavariables.extend(datavariable)
    #print('\n\n\n{}\n\n\n\n'.format(datavariables[0]))
    #print('\n\n\n{}\n\n\n\n'.format(datavariables[1]))
    _data.extend(datavariables)

    # Return data
    process = data.Data(agent_program, _data)
    result = process.data()
    return result


def _snmpwalks(ip_devices, oids4devices):
    """Get PATOO_SNMP agent data.

    Update the DataVariableList with DataVariables

    Args:
        ip_devices: Dict of type SNMPVariable keyed by ip_device
        oids4devices: Dict of OID lists keyed by ip_device

    Returns:
        datavariables: List of type DataVariable

    """
    # Initialize key variables
    arguments = []
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())

    # Poll all devices in sequence
    for ip_device, snmpvariable in sorted(ip_devices.items()):
        if ip_device in oids4devices:
            oids = oids4devices[ip_device]
            arguments.append((snmpvariable, oids))

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        datavariables = pool.starmap(_walker, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Return
    return datavariables


def _walker(snmpvariable, oids):
    """Poll each spoke in parallel.

    Args:
        snmpvariable: SNMPVariable to poll
        oids: OIDs to poll

    Returns:
        datavariables: list of type DataVariable

    """
    # Get data and return
    result = []
    for oid in oids:
        query = snmp.SNMP(snmpvariable)
        query_datavariables = query.walk(oid)
        result.extend(query_datavariables)
    return result
