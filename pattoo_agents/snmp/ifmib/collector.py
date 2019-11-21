#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing
import socket
import collections
from pprint import pprint

# Pattoo libraries
from pattoo_agents.snmp import configuration
from pattoo_shared import agent
from pattoo_shared.variables import (
    DataPoint, DataPointMeta, DeviceDataPoints, AgentPolledData, DeviceGateway)
from pattoo_agents.snmp.constants import PATTOO_AGENT_SNMPD
from pattoo_agents.snmp.ifmib.mib_if import Query


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
    query = Query(snmpvariable)
    results = query.everything()
    datapoints = _create_datapoints(results)
    ddv.add(datapoints)
    return ddv


def _create_datapoints(results):
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
    datapoints = []
    ifindex_lookup = _metadata(results)

    # Process the results
    for key, items in results.items():
        # Ignore keys used to create the ifindex_lookup
        if key in ['ifDescr', 'ifName', 'ifAlias', 'ifIndex']:
            continue
        # Evaluate DataPoint list data from remaining keys
        for item in items:
            # Reassign DataPoint values
            ifindex = item.key.split('.')[-1]
            if ifindex in ifindex_lookup:
                # Ignore administratively down interfaces
                if bool(ifindex_lookup[ifindex].ifadminstatus) is False:
                    continue
                # Otherwise create the datapoint
                datapoint = DataPoint(
                    _key(item.key), item.value, timestamp=item.timestamp)
                if bool(ifindex_lookup[ifindex].ifdescr) is True:
                    datapoint.add(
                        DataPointMeta(
                            'ifDescr', ifindex_lookup[ifindex].ifdescr))
                if bool(ifindex_lookup[ifindex].ifalias) is True:
                    datapoint.add(
                        DataPointMeta(
                            'ifAlias', ifindex_lookup[ifindex].ifalias))
                if bool(ifindex_lookup[ifindex].ifname) is True:
                    datapoint.add(
                        DataPointMeta(
                            'ifName', ifindex_lookup[ifindex].ifname))
                datapoints.append(datapoint)

    return datapoints


def _metadata(results):
    """Create a dict of interface descriptions and status keyed by ifIndex.

    Args:
        results: Dict of SNMP walk results

    Returns:
        result: Dict of data

    """
    # Initialize key variables
    ifdescr = {}
    ifalias = {}
    ifname = {}
    ifadminstatus = {}
    result = {}
    Record = collections.namedtuple(
        'Record', 'ifalias ifdescr ifname ifadminstatus')

    if 'ifDescr' in results:
        _ifdescr = results['ifDescr']
    else:
        _ifdescr = {}

    if 'ifAlias' in results:
        _ifalias = results['ifAlias']
    else:
        _ifalias = {}

    if 'ifName' in results:
        _ifname = results['ifName']
    else:
        _ifname = {}

    if 'ifAdminStatus' in results:
        _ifadminstatus = results['ifAdminStatus']
    else:
        _ifadminstatus = {}

    # Populate dict
    for item in _ifdescr:
        ifindex = item.key.split('.')[-1]
        ifdescr[ifindex] = item.value
    for item in _ifalias:
        ifindex = item.key.split('.')[-1]
        ifalias[ifindex] = item.value
    for item in _ifname:
        ifindex = item.key.split('.')[-1]
        ifname[ifindex] = item.value
    for item in _ifadminstatus:
        ifindex = item.key.split('.')[-1]
        ifadminstatus[ifindex] = False if item.value != 1 else True
    for key, value in sorted(ifdescr.items()):
        use_ifname = ifname.get(key, None)
        use_ifalias = ifalias.get(key, None)
        use_ifadminstatus = ifadminstatus.get(key, False)
        result[key] = Record(
            ifdescr=value,
            ifname=use_ifname,
            ifalias=use_ifalias,
            ifadminstatus=use_ifadminstatus)
    return result


def _key(oid):
    """Create a key for an OID.

    Args:
        oid: SNMP OID

    Returns:
        result: Key value

    """
    # Initialize key variables
    result = ''
    limit = 8
    table = {
        '.1.3.6.1.2.1.2.2.1.1': 'ifIndex',
        '.1.3.6.1.2.1.2.2.1.10': 'ifInOctets',
        '.1.3.6.1.2.1.2.2.1.11': 'ifInUcastPkts',
        '.1.3.6.1.2.1.2.2.1.12': 'ifInNUcastPkts',
        '.1.3.6.1.2.1.2.2.1.13': 'ifInDiscards',
        '.1.3.6.1.2.1.2.2.1.14': 'ifInErrors',
        '.1.3.6.1.2.1.2.2.1.15': 'ifInUnknownProtos',
        '.1.3.6.1.2.1.2.2.1.16': 'ifOutOctets',
        '.1.3.6.1.2.1.2.2.1.17': 'ifOutUcastPkts',
        '.1.3.6.1.2.1.2.2.1.18': 'ifOutNUcastPkts',
        '.1.3.6.1.2.1.2.2.1.19': 'ifOutDiscards',
        '.1.3.6.1.2.1.2.2.1.2': 'ifDescr',
        '.1.3.6.1.2.1.2.2.1.20': 'ifOutErrors',
        '.1.3.6.1.2.1.2.2.1.21': 'ifOutQLen',
        '.1.3.6.1.2.1.2.2.1.22': 'ifSpecific',
        '.1.3.6.1.2.1.2.2.1.3': 'ifType',
        '.1.3.6.1.2.1.2.2.1.4': 'ifMtu',
        '.1.3.6.1.2.1.2.2.1.5': 'ifSpeed',
        '.1.3.6.1.2.1.2.2.1.6': 'ifPhysAddress',
        '.1.3.6.1.2.1.2.2.1.7': 'ifAdminStatus',
        '.1.3.6.1.2.1.2.2.1.8': 'ifOperStatus',
        '.1.3.6.1.2.1.2.2.1.9': 'ifLastChange',
        '.1.3.6.1.2.1.31.1.1.1.1': 'ifName',
        '.1.3.6.1.2.1.31.1.1.1.10': 'ifHCOutOctets',
        '.1.3.6.1.2.1.31.1.1.1.11': 'ifHCOutUcastPkts',
        '.1.3.6.1.2.1.31.1.1.1.12': 'ifHCOutMulticastPkts',
        '.1.3.6.1.2.1.31.1.1.1.13': 'ifHCOutBroadcastPkts',
        '.1.3.6.1.2.1.31.1.1.1.14': 'ifLinkUpDownTrapEnable',
        '.1.3.6.1.2.1.31.1.1.1.15': 'ifHighSpeed',
        '.1.3.6.1.2.1.31.1.1.1.16': 'ifPromiscuousMode',
        '.1.3.6.1.2.1.31.1.1.1.17': 'ifConnectorPresent',
        '.1.3.6.1.2.1.31.1.1.1.18': 'ifAlias',
        '.1.3.6.1.2.1.31.1.1.1.19': 'ifCounterDiscontinuityTime',
        '.1.3.6.1.2.1.31.1.1.1.2': 'ifInMulticastPkts',
        '.1.3.6.1.2.1.31.1.1.1.3': 'ifInBroadcastPkts',
        '.1.3.6.1.2.1.31.1.1.1.4': 'ifOutMulticastPkts',
        '.1.3.6.1.2.1.31.1.1.1.5': 'ifOutBroadcastPkts',
        '.1.3.6.1.2.1.31.1.1.1.6': 'ifHCInOctets',
        '.1.3.6.1.2.1.31.1.1.1.7': 'ifHCInUcastPkts',
        '.1.3.6.1.2.1.31.1.1.1.8': 'ifHCInMulticastPkts',
        '.1.3.6.1.2.1.31.1.1.1.9': 'ifHCInBroadcastPkts',
    }

    # Search for a match in the table
    splits = oid.split('.')
    for count in range(0, limit):
        key = '.'.join(splits[:-count])
        if key in table:
            result = table[key]
            break

    return result
