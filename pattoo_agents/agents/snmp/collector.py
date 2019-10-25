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
from pattoo_shared.variables import DeviceDataVariables, AgentPolledData


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
    ip_devices = {}
    oids4devices = {}

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_SNMPD
    agent_hostname = socket.getfqdn()
    agent_id = agent.get_agent_id(agent_program, agent_hostname)
    agentdata = AgentPolledData(agent_id, agent_program, agent_hostname)

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

    # Poll oids for all devices and update the DeviceDataVariables
    dv_hosts = _snmpwalks(ip_devices, oids4devices)
    agentdata.extend(dv_hosts)

    # Return data
    return agentdata


def _snmpwalks(ip_devices, oids4devices):
    """Get PATOO_SNMP agent data.

    Update the DeviceDataVariables with DataVariables

    Args:
        ip_devices: Dict of type SNMPVariable keyed by ip_device
        oids4devices: Dict of OID lists keyed by ip_device

    Returns:
        dv_host: List of type DeviceDataVariables

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
        dv_hosts = pool.starmap(_walker, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Return
    return dv_hosts


def _walker(snmpvariable, oids):
    """Poll each spoke in parallel.

    Args:
        snmpvariable: SNMPVariable to poll
        oids: OIDs to poll

    Returns:
        dv_host: DeviceDataVariables for the SNMPVariable device

    """
    # Intialize data gathering
    dv_host = DeviceDataVariables(snmpvariable.ip_device)

    # Get list of type DataVariable
    datavariables = []
    for oid in oids:
        query = snmp.SNMP(snmpvariable)
        query_datavariables = query.walk(oid)
        datavariables.extend(query_datavariables)
    dv_host.extend(datavariables)

    # Return
    return dv_host
