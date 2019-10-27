#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing
import socket


# Pattoo libraries
from pattoo_agents.agents.snmp import configuration
from pattoo_agents.agents.snmp import snmp
from pattoo_shared import agent
from pattoo_shared.constants import PATTOO_AGENT_SNMPD
from pattoo_shared.variables import (
    DeviceDataVariables, AgentPolledData, DeviceGateway)


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
    ip_oidvariables = {}

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_SNMPD
    agent_hostname = socket.getfqdn()
    agent_id = agent.get_agent_id(agent_program, agent_hostname)
    agentdata = AgentPolledData(agent_id, agent_program, agent_hostname)
    gateway = DeviceGateway(agent_hostname)

    # Get SNMP OIDs to be polled (Along with authorizations and ip_devices)
    cfg_snmpvariables = config.snmpvariables()
    cfg_oidvariables = config.oidvariables()

    # Create a dict of snmpvariables keyed by ip_device
    for snmpvariable in cfg_snmpvariables:
        ip_snmpvariables[snmpvariable.ip_device] = snmpvariable

    # Create a dict of oid lists keyed by ip_device
    for oidvariable in cfg_oidvariables:
        next_device = oidvariable.ip_device
        if next_device in ip_oidvariables:
            ip_oidvariables[next_device].extend(oidvariable.oids)
        else:
            ip_oidvariables[next_device] = oidvariable.oids

    # Poll oids for all devices and update the DeviceDataVariables
    ddv_list = _snmpwalks(ip_snmpvariables, ip_oidvariables)
    gateway.add(ddv_list)
    agentdata.add(gateway)

    # Return data
    return agentdata


def _snmpwalks(ip_snmpvariables, ip_oidvariables):
    """Get PATOO_SNMP agent data.

    Update the DeviceDataVariables with DataVariables

    Args:
        ip_snmpvariables: Dict of type SNMPVariable keyed by ip_device
        ip_oidvariables: Dict of OID lists keyed by ip_device

    Returns:
        ddv_list: List of type DeviceDataVariables

    """
    # Initialize key variables
    arguments = []
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())

    # Poll all devices in sequence
    for ip_device, snmpvariable in sorted(ip_snmpvariables.items()):
        if ip_device in ip_oidvariables:
            oidvariables = ip_oidvariables[ip_device]
            arguments.append((snmpvariable, oidvariables))

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        ddv_list = pool.starmap(_walker, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Return
    return ddv_list


def _walker(snmpvariable, oidvariables):
    """Poll each spoke in parallel.

    Args:
        snmpvariable: SNMPVariable to poll
        oidvariables: OIDs to poll

    Returns:
        ddv: DeviceDataVariables for the SNMPVariable device

    """
    # Intialize data gathering
    ddv = DeviceDataVariables(snmpvariable.ip_device)

    # Get list of type DataVariable
    datavariables = []
    for oid in oidvariables.oids:
        query = snmp.SNMP(snmpvariable)
        query_datavariables = query.walk(oid)
        datavariables.extend(query_datavariables)
    ddv.add(datavariables)

    # Return
    return ddv
