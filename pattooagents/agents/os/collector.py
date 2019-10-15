#!/usr/bin/env python3
"""Pattoo library collecting Linux data."""

# Standard libraries
import os
import re
import platform
import socket

# pip3 libraries
import psutil

# Pattoo libraries
from pattooagents import data
from pattooagents.variables import DataVariable, DataVariablesHost, AgentPolledData
from pattooagents import agent
from pattooagents import times
from pattooagents.constants import (
    DATA_INT, DATA_COUNT64, DATA_STRING, DATA_FLOAT)


def poll(agent_program):
    """Get all agent data.

    Performance data on linux server on which this application is installed.

    Args:
        agentdata: AgentPolledData object for all data gathered by the agent

    Returns:
        None

    """
    # Initialize AgentPolledData
    agent_id = agent.get_agent_id(agent_program)
    agent_hostname = socket.getfqdn()
    timestamp = times.normalized_timestamp()
    agentdata = AgentPolledData(
        agent_id, agent_program, agent_hostname, timestamp)

    # Intialize data gathering
    dv_host = DataVariablesHost(agent_hostname)

    # Update agent with system data
    _stats_system(dv_host)

    # Update agent with disk data
    _stats_disk_swap(dv_host)
    _stats_disk_partitions(dv_host)
    _stats_disk_io(dv_host)

    # Update agent with network data
    _stats_network(dv_host)

    # Add results to the AgentPolledData object for posting
    agentdata.append(dv_host)
    return agentdata


def _stats_system(dv_host):
    """Update agent with system data.

    Args:
        dv_host: DataVariablesHost object

    Returns:
        None

    """
    #########################################################################
    # Set non timeseries values
    #########################################################################

    dv_host.append(DataVariable(value=platform.release(),
                                data_label='release',
                                data_type=DATA_STRING))

    dv_host.append(DataVariable(value=platform.system(),
                                data_label='system',
                                data_type=DATA_STRING))

    dv_host.append(DataVariable(value=platform.version(),
                                data_label='version',
                                data_type=DATA_STRING))

    dv_host.append(DataVariable(value=psutil.cpu_count(),
                                data_label='cpu_count',
                                data_type=DATA_INT))

    #########################################################################
    # Set timeseries values (Integers)
    #########################################################################
    dv_host.append(DataVariable(value=len(psutil.pids()),
                                data_label='process_count',
                                data_type=DATA_INT))

    # Load averages
    (la_01, la_05, la_15) = os.getloadavg()

    dv_host.append(DataVariable(value=la_01,
                                data_label='load_average_01min',
                                data_type=DATA_INT))

    dv_host.append(DataVariable(value=la_05,
                                data_label='load_average_05min',
                                data_type=DATA_INT))

    dv_host.append(DataVariable(value=la_15,
                                data_label='load_average_15min',
                                data_type=DATA_INT))

    #########################################################################
    # Set timeseries values (Named Tuples)
    #########################################################################

    # Percentage CPU utilization
    dv_host.extend(data.named_tuple_to_dv(
        psutil.cpu_times_percent(),
        data_label='cpu_times_percent', data_type=DATA_FLOAT))

    # Get CPU runtimes
    dv_host.extend(data.named_tuple_to_dv(
        psutil.cpu_times(),
        data_label='cpu_times', data_type=DATA_COUNT64))

    # Get CPU stats
    dv_host.extend(data.named_tuple_to_dv(
        psutil.cpu_stats(),
        data_label='cpu_stats', data_type=DATA_COUNT64))

    # Get memory utilization
    dv_host.extend(data.named_tuple_to_dv(
        psutil.virtual_memory(),
        data_label='memory', data_type=DATA_INT))


def _stats_disk_swap(dv_host):
    """Update agent with disk swap data.

    Args:
        dv_host: DataVariablesHost object

    Returns:
        None

    """
    # Initialize key variables
    result = []
    prefix = 'swap'

    # Get swap information
    system_list = psutil.swap_memory()._asdict()
    for suffix, value in system_list.items():
        # Different suffixes have different data types
        if suffix in ['sin', 'sout']:
            data_type = DATA_COUNT64
        else:
            data_type = DATA_INT

        # Create records
        data_label = '{}_{}'.format(prefix, suffix)

        # No need to specify a suffix as there is only one swap
        _dv = DataVariable(
            value=value, data_label=data_label, data_type=data_type)
        result.append(_dv)

    # Add the result to data
    dv_host.extend(result)


def _stats_disk_partitions(dv_host):
    """Update agent with disk partition data.

    Args:
        dv_host: DataVariablesHost object

    Returns:
        None

    """
    # Initialize key variables
    prefix = 'disk_usage'
    result = []

    # Get filesystem partition utilization
    diskdv_host = psutil.disk_partitions()
    # "diskdv_host" is named tuple describing partitions
    for item in diskdv_host:
        # "source" is the partition mount point
        mountpoint = item.mountpoint
        if "docker" in str(mountpoint):
            pass
        else:
            partition = psutil.disk_usage(mountpoint)._asdict()
            for suffix, value in partition.items():
                data_label = '{}_{}'.format(prefix, suffix)
                _dv = DataVariable(
                    value=value, data_label=data_label,
                    data_index=mountpoint, data_type=DATA_INT)
                result.append(_dv)

    # Add the result to data
    dv_host.extend(result)


def _stats_disk_io(dv_host):
    """Update agent with disk io data.

    Args:
        dv_host: DataVariablesHost object

    Returns:
        None

    """
    # Initialize key variables
    regex = re.compile(r'^ram\d+$')
    prefix = 'disk_io'
    result = []

    # Get disk I/O usage
    iodv_host = psutil.disk_io_counters(perdisk=True)

    # "source" is disk name
    for disk, disk_named_tuple in iodv_host.items():
        # No RAM pseudo disks. RAM disks OK.
        if bool(regex.match(disk)) is True:
            continue
        # No loopbacks
        if disk.startswith('loop') is True:
            continue

        # Populate data
        disk_dict = disk_named_tuple._asdict()
        for suffix, value in disk_dict.items():
            data_label = '{}_{}'.format(prefix, suffix)
            _dv = DataVariable(
                value=value, data_label=data_label,
                data_index=disk, data_type=DATA_COUNT64)
            result.append(_dv)

    # Add the result to data
    dv_host.extend(result)


def _stats_network(dv_host):
    """Update agent with network data.

    Args:
        dv_host: DataVariablesHost object

    Returns:
        None

    """
    # Initialize key variables
    result = []
    prefix = 'network'

    # Get network utilization
    nicdv_host = psutil.net_io_counters(pernic=True)
    for nic, nic_named_tuple in nicdv_host.items():
        nic_dict = nic_named_tuple._asdict()
        for suffix, value in nic_dict.items():
            data_label = '{}_{}'.format(prefix, suffix)
            _dv = DataVariable(
                value=value, data_label=data_label,
                data_index=nic, data_type=DATA_COUNT64)
            result.append(_dv)

    # Add the result to data
    dv_host.extend(result)
