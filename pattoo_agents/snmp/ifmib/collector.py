#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing
import collections

# Pattoo libraries
from pattoo_shared.variables import (
    DataPointMetadata, DataPoint, TargetDataPoints, AgentPolledData)
from pattoo_agents.snmp.constants import PATTOO_AGENT_SNMP_IFMIBD
from pattoo_agents.snmp.ifmib.mib_if import Query
from pattoo_agents.snmp.configuration import ConfigSNMPIfMIB as Config


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
    agent_program = PATTOO_AGENT_SNMP_IFMIBD
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
    query = Query(snmpvariable)
    results = query.everything()
    datapoints = _create_datapoints(results)
    ddv.add(datapoints)
    return ddv


def _create_datapoints(items):
    """Get PATOO_SNMP agent data.

    Update the TargetDataPoints with DataPoints

    Args:
        items: Dict of type SNMPVariable keyed by OID branch

    Returns:
        result: List of DataPoints with metadata added

    Method:
        1) Poll all desired OIDs from the target target. Ignore shutdown
            interfaces
        2) Get the IfAlias, IfName, and ifDescr values for each snmp ifIndex
            to use as metadata for DataPoints
        3) Convert the polled datapoints to use a key of their MIB string
            versus the OID as the key. Use the OID as a metadata value instead.
        4) Add the IfAlias, IfName, and ifDescr values as metadata to
            each datapoint.

    """
    # Initialize key variables
    result = []
    ifindex_lookup = _metadata(items)

    # Process the results
    for key, polled_datapoints in items.items():
        # Ignore keys used to create the ifindex_lookup
        if key in ['ifDescr', 'ifName', 'ifAlias', 'ifIndex', 'ifAdminStatus']:
            continue

        # Evaluate DataPoint list data from remaining keys
        for polled_datapoint in polled_datapoints:
            if polled_datapoint.valid is False:
                continue

            # Reassign DataPoint values
            ifindex = polled_datapoint.key.split('.')[-1]
            if ifindex in ifindex_lookup:

                # Ignore administratively down interfaces
                if bool(ifindex_lookup[ifindex].ifadminstatus) is False:
                    continue

                # Create a new Datapoint keyed by MIB equivalent
                new_key = _key(polled_datapoint.key)
                datapoint = DataPoint(
                    new_key,
                    polled_datapoint.value,
                    data_type=polled_datapoint.data_type)

                # Add metadata to the datapoint
                datapoint.add(
                    DataPointMetadata('oid', polled_datapoint.key))
                if bool(ifindex_lookup[ifindex].ifdescr) is True:
                    datapoint.add(
                        DataPointMetadata(
                            'ifDescr',
                            ifindex_lookup[ifindex].ifdescr))
                if bool(ifindex_lookup[ifindex].ifalias) is True:
                    datapoint.add(
                        DataPointMetadata(
                            'ifAlias',
                            ifindex_lookup[ifindex].ifalias))
                if bool(ifindex_lookup[ifindex].ifname) is True:
                    datapoint.add(
                        DataPointMetadata(
                            'ifName',
                            ifindex_lookup[ifindex].ifname))
                result.append(datapoint)

    return result


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
