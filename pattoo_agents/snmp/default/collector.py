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
from pattoo_shared.variables import (
    DataPoint, DeviceDataPoints, AgentPolledData, DeviceGateway)
from pattoo_agents.snmp.constants import PATTOO_AGENT_SNMPD


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
    polling_interval = config.polling_interval()
    ip_snmpvariables = {}
    ip_polltargets = {}

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_SNMPD
    agent_hostname = socket.getfqdn()
    agent_id = agent.get_agent_id(agent_program, agent_hostname)
    agentdata = AgentPolledData(
        agent_id, agent_program, agent_hostname, polling_interval)
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

    # Poll oids for all devices and update the DeviceDataPoints
    ddv_list = _snmpwalks(ip_snmpvariables, ip_polltargets)
    gateway.add(ddv_list)
    agentdata.add(gateway)

    # Return data
    return agentdata


def _snmpwalks(ip_snmpvariables, ip_polltargets):
    """Get PATOO_SNMP agent data.

    Update the DeviceDataPoints with DataPoints

    Args:
        ip_snmpvariables: Dict of type SNMPVariable keyed by ip_device
        ip_polltargets: Dict keyed by ip_device with PollingTarget
            lists to poll

    Returns:
        ddv_list: List of type DeviceDataPoints

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
        ddv: DeviceDataPoints for the SNMPVariable device

    """
    # Intialize data gathering
    ddv = DeviceDataPoints(snmpvariable.ip_device)

    # Get list of type DataPoint
    datapoints = []
    for polltarget in polltargets:
        # Get OID polling results
        query = snmp.SNMP(snmpvariable)
        query_datapoints = query.walk(polltarget.address)

        # Apply multiplier to the results
        for _dp in query_datapoints:
            # Do multiplication
            if data.is_data_type_numeric(_dp.data_type) is True:
                value = float(_dp.data_value) * polltarget.multiplier
            else:
                value = _dp.data_value

            # Update datapoints
            datapoint = DataPoint(
                value, data_label=_dp.data_label,
                data_index=_dp.data_index, data_type=_dp.data_type)
            datapoints.append(datapoint)

    # Return
    ddv.add(datapoints)
    return ddv
