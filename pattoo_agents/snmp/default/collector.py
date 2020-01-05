#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing


# Pattoo libraries
from pattoo_agents.snmp import snmp
from pattoo_shared import data
from pattoo_shared.variables import (
    AgentKey, DataPoint, DataPointMetadata, TargetDataPoints, AgentPolledData)
from pattoo_agents.snmp.constants import PATTOO_AGENT_SNMPD
from pattoo_agents.snmp.configuration import ConfigSNMP as Config


def poll():
    """Get PATOO_SNMP agent data.

    Performance data from SNMP enabled targets.

    Args:
        None

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize key variables.
    config = Config()
    ip_snmpvariables = {}
    ip_polltargets = {}
    _pi = config.polling_interval()

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_SNMPD
    agentdata = AgentPolledData(agent_program, _pi)

    # Get SNMP OIDs to be polled (Along with authorizations and ip_targets)
    cfg_snmpvariables = config.snmpvariables()
    target_poll_targets = config.target_polling_points()

    # Create a dict of snmpvariables keyed by ip_target
    for snmpvariable in cfg_snmpvariables:
        ip_snmpvariables[snmpvariable.ip_target] = snmpvariable

    # Create a dict of oid lists keyed by ip_target
    for dpt in target_poll_targets:
        # Ignore invalid data
        if dpt.valid is False:
            continue

        # Process
        next_target = dpt.target
        if next_target in ip_polltargets:
            ip_polltargets[next_target].extend(dpt.data)
        else:
            ip_polltargets[next_target] = dpt.data

    # Poll oids for all targets and update the TargetDataPoints
    ddv_list = _snmpwalks(ip_snmpvariables, ip_polltargets)
    agentdata.add(ddv_list)

    # Return data
    return agentdata


def _snmpwalks(ip_snmpvariables, ip_polltargets):
    """Get PATOO_SNMP agent data.

    Update the TargetDataPoints with DataPoints

    Args:
        ip_snmpvariables: Dict of type SNMPVariable keyed by ip_target
        ip_polltargets: Dict keyed by ip_target with PollingPoint
            lists to poll

    Returns:
        ddv_list: List of type TargetDataPoints

    """
    # Initialize key variables
    arguments = []
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())

    # Poll all targets in sequence
    for ip_target, snmpvariable in sorted(ip_snmpvariables.items()):
        if ip_target in ip_polltargets:
            polltargets = ip_polltargets[ip_target]
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
        polltargets: List of PollingPoint objects to poll

    Returns:
        ddv: TargetDataPoints for the SNMPVariable target

    """
    # Intialize data gathering
    ddv = TargetDataPoints(snmpvariable.ip_target)
    prefix = AgentKey(PATTOO_AGENT_SNMPD)

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
                value = float(_dp.value) * polltarget.multiplier
            else:
                value = _dp.value

            # Update datapoints
            datapoint = DataPoint(
                prefix.key(polltarget.address),
                value,
                data_type=_dp.data_type)
            datapoint.add(DataPointMetadata(prefix.key('oid'), _dp.key))
            datapoints.append(datapoint)

    # Return
    ddv.add(datapoints)
    return ddv
