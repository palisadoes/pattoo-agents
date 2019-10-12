#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing


# Pattoo libraries
from pattoo.agents.snmp import configuration
from pattoo.agents.snmp import snmp
from pattoo.variables import DataVariableList


def poll():
    """Get PATOO_SNMP agent data.

    Performance data from SNMP enabled devices.

    Args:
        None

    Returns:
        dv_lists: A list of type DataVariableList

    """
    # Initialize key variables.
    config = configuration.ConfigSNMP()
    ip_devices = {}
    oids4devices = {}

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
    dv_lists = _snmpwalks(ip_devices, oids4devices)

    # Return data
    return dv_lists


def _snmpwalks(ip_devices, oids4devices):
    """Get PATOO_SNMP agent data.

    Update the DataVariableList with DataVariables

    Args:
        ip_devices: Dict of type SNMPVariable keyed by ip_device
        oids4devices: Dict of OID lists keyed by ip_device

    Returns:
        dv_list: List of type DataVariableList

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
        dv_lists = pool.starmap(_walker, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Return
    return dv_lists


def _walker(snmpvariable, oids):
    """Poll each spoke in parallel.

    Args:
        snmpvariable: SNMPVariable to poll
        oids: OIDs to poll

    Returns:
        dv_list: DataVariableList for the SNMPVariable device

    """
    # Intialize data gathering
    dv_list = DataVariableList(snmpvariable.ip_device)

    # Get list of type DataVariable
    datavariables = []
    for oid in oids:
        query = snmp.SNMP(snmpvariable)
        query_datavariables = query.walk(oid)
        datavariables.extend(query_datavariables)
    dv_list.extend(datavariables)

    # Return
    return dv_list
