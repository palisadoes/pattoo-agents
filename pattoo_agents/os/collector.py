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
from pattoo_shared import agent
from pattoo_shared.configuration import Config
from pattoo_shared.variables import (
    DataPoint, DeviceDataPoints, DeviceGateway, AgentPolledData)
from pattoo_shared.constants import (
    DATA_INT, DATA_COUNT64, DATA_STRING, DATA_FLOAT)


def poll(agent_program):
    """Get all agent data.

    Performance data on linux server on which this application is installed.

    Args:
        agentdata: AgentPolledData object for all data gathered by the agent

    Returns:
        None

    """
    # Initialize key variables.
    config = Config()
    polling_interval = config.polling_interval()

    # Initialize AgentPolledData
    agent_hostname = socket.getfqdn()
    agent_id = agent.get_agent_id(agent_program, agent_hostname)
    agentdata = AgentPolledData(
        agent_id, agent_program, agent_hostname, polling_interval)
    gateway = DeviceGateway(agent_hostname)

    # Intialize data gathering
    ddv = DeviceDataPoints(agent_hostname)

    # Update agent with system data
    _stats_system(ddv)

    # Update agent with disk data
    _stats_disk_swap(ddv)
    _stats_disk_partitions(ddv)
    _stats_disk_io(ddv)

    # Update agent with network data
    _stats_network(ddv)

    # Add results to the AgentPolledData object for posting
    gateway.add(ddv)
    agentdata.add(gateway)
    return agentdata


def _stats_system(ddv):
    """Update agent with system data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    #########################################################################
    # Set non timeseries values
    #########################################################################

    ddv.add(DataPoint(value=platform.release(),
                         data_label='release',
                         data_type=DATA_STRING))

    ddv.add(DataPoint(value=platform.system(),
                         data_label='system',
                         data_type=DATA_STRING))

    ddv.add(DataPoint(value=platform.version(),
                         data_label='version',
                         data_type=DATA_STRING))

    ddv.add(DataPoint(value=psutil.cpu_count(),
                         data_label='cpu_count',
                         data_type=DATA_INT))

    #########################################################################
    # Set timeseries values (Integers)
    #########################################################################
    ddv.add(DataPoint(value=len(psutil.pids()),
                         data_label='process_count',
                         data_type=DATA_INT))

    # Load averages
    (la_01, la_05, la_15) = os.getloadavg()

    ddv.add(DataPoint(value=la_01,
                         data_label='load_average_01min',
                         data_type=DATA_INT))

    ddv.add(DataPoint(value=la_05,
                         data_label='load_average_05min',
                         data_type=DATA_INT))

    ddv.add(DataPoint(value=la_15,
                         data_label='load_average_15min',
                         data_type=DATA_INT))

    #########################################################################
    # Set timeseries values (Named Tuples)
    #########################################################################

    # Percentage CPU utilization
    ddv.add(_named_tuple_to_dv(
        psutil.cpu_times_percent(),
        data_label='cpu_times_percent', data_type=DATA_FLOAT))

    # Get CPU runtimes
    ddv.add(_named_tuple_to_dv(
        psutil.cpu_times(),
        data_label='cpu_times', data_type=DATA_COUNT64))

    # Get CPU stats
    ddv.add(_named_tuple_to_dv(
        psutil.cpu_stats(),
        data_label='cpu_stats', data_type=DATA_COUNT64))

    # Get memory utilization
    ddv.add(_named_tuple_to_dv(
        psutil.virtual_memory(),
        data_label='memory', data_type=DATA_INT))


def _stats_disk_swap(ddv):
    """Update agent with disk swap data.

    Args:
        ddv: DeviceDataPoints object

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
        _dv = DataPoint(
            value=value, data_label=data_label, data_type=data_type)
        result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _stats_disk_partitions(ddv):
    """Update agent with disk partition data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    # Initialize key variables
    prefix = 'disk_usage'
    result = []

    # Get filesystem partition utilization
    diskddv = psutil.disk_partitions()
    # "diskddv" is named tuple describing partitions
    for item in diskddv:
        # "source" is the partition mount point
        mountpoint = item.mountpoint
        if "docker" in str(mountpoint):
            pass
        else:
            partition = psutil.disk_usage(mountpoint)._asdict()
            for suffix, value in partition.items():
                data_label = '{}_{}'.format(prefix, suffix)
                _dv = DataPoint(
                    value=value, data_label=data_label,
                    data_index=mountpoint, data_type=DATA_INT)
                result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _stats_disk_io(ddv):
    """Update agent with disk io data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    # Initialize key variables
    regex = re.compile(r'^ram\d+$')
    prefix = 'disk_io'
    result = []

    # Get disk I/O usage
    ioddv = psutil.disk_io_counters(perdisk=True)

    # "source" is disk name
    for disk, disk_named_tuple in ioddv.items():
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
            _dv = DataPoint(
                value=value, data_label=data_label,
                data_index=disk, data_type=DATA_COUNT64)
            result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _stats_network(ddv):
    """Update agent with network data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    # Initialize key variables
    result = []
    prefix = 'network'

    # Get network utilization
    nicddv = psutil.net_io_counters(pernic=True)
    for nic, nic_named_tuple in nicddv.items():
        nic_dict = nic_named_tuple._asdict()
        for suffix, value in nic_dict.items():
            data_label = '{}_{}'.format(prefix, suffix)
            _dv = DataPoint(
                value=value, data_label=data_label,
                data_index=nic, data_type=DATA_COUNT64)
            result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _named_tuple_to_dv(
        values, data_label=None, data_type=DATA_INT):
    """Convert a named tuple to a list of DataPoint objects.

    Args:
        values: Named tuple
        data_label: data_label
        data_type: Data type

    Returns:
        result: List of DataPoint

    """
    # Get data
    data_dict = values._asdict()
    result = []

    # Cycle through results
    for data_index, value in data_dict.items():
        _dv = DataPoint(
            value=value,
            data_label=data_label,
            data_index=data_index,
            data_type=data_type)
        result.append(_dv)

    # Return
    return result
