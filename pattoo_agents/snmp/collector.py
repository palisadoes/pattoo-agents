#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing
import socket


# Pattoo libraries
from pattoo_agents.snmp import configuration
from pattoo_agents.snmp import snmp
from pattoo_shared import agent
from pattoo_shared import data
from pattoo_shared.constants import PATTOO_AGENT_SNMPD
from pattoo_shared.variables import (
    DataVariable, DeviceDataVariables, AgentPolledData, DeviceGateway)


def poll():
    """Get PATOO_SNMP agent data.

    Performance data from SNMP enabled devices.

    Args:
        None

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize key variables.
    config = configuration.ConfigSNMP()
    ip_snmpvariables = {}
    ip_polltargets = {}

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_SNMPD
    agent_hostname = socket.getfqdn()
    agent_id = agent.get_agent_id(agent_program, agent_hostname)
    agentdata = AgentPolledData(agent_id, agent_program, agent_hostname)
    gateway = DeviceGateway(agent_hostname)

    # Get SNMP OIDs to be polled (Along with authorizations and ip_devices)
    cfg_snmpvariables = config.snmpvariables()
    device_poll_targets = config.device_polling_targets()

    # Create a dict of snmpvariables keyed by ip_device
    for snmpvariable in cfg_snmpvariables:
        ip_snmpvariables[snmpvariable.ip_device] = snmpvariable

    # Create a dict of oid lists keyed by ip_device
    for dpt in device_poll_targets:
        # Ignore invalid data
        if dpt.valid is False:
            continue

        # Process
        next_device = dpt.device
        if next_device in ip_polltargets:
            ip_polltargets[next_device].extend(dpt.data)
        else:
            ip_polltargets[next_device] = dpt.data

    # Poll oids for all devices and update the DeviceDataVariables
    ddv_list = _snmpwalks(ip_snmpvariables, ip_polltargets)
    gateway.add(ddv_list)
    agentdata.add(gateway)

    # Return data
    return agentdata


def _snmpwalks(ip_snmpvariables, ip_polltargets):
    """Get PATOO_SNMP agent data.

    Update the DeviceDataVariables with DataVariables

    Args:
        ip_snmpvariables: Dict of type SNMPVariable keyed by ip_device
        ip_polltargets: Dict keyed by ip_device with PollingTarget lists to poll

    Returns:
        ddv_list: List of type DeviceDataVariables

    """
    # Initialize key variables
    arguments = []
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())

    # Poll all devices in sequence
    for ip_device, snmpvariable in sorted(ip_snmpvariables.items()):
        if ip_device in ip_polltargets:
            polltargets = ip_polltargets[ip_device]
            arguments.append((snmpvariable, polltargets))

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        ddv_list = pool.starmap(_walker, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Return
    return ddv_list


def _walker(snmpvariable, polltargets):
    """Poll each spoke in parallel.

    Args:
        snmpvariable: SNMPVariable to poll
        polltargets: List of PollingTarget objects to poll

    Returns:
        ddv: DeviceDataVariables for the SNMPVariable device

    """
    # Intialize data gathering
    ddv = DeviceDataVariables(snmpvariable.ip_device)

    # Get list of type DataVariable
    datavariables = []
    for polltarget in polltargets:
        # Get OID polling results
        query = snmp.SNMP(snmpvariable)
        query_datavariables = query.walk(polltarget.address)

        # Apply multiplier to the results
        for _dv in query_datavariables:
            # Do multiplication
            if data.is_data_type_numeric(_dv.data_type) is True:
                value = float(_dv.value) * polltarget.multiplier
            else:
                value = _dv.value

            # Update datavariables
            datavariable = DataVariable(
                value=value, data_label=_dv.data_label,
                data_index=_dv.data_index, data_type=_dv.data_type)
            datavariables.append(datavariable)

    # Return
    ddv.add(datavariables)
    return ddv
