#!/usr/bin/env python3
"""Pattoo library collecting Linux data."""

# Standard libraries
import os
import re
import platform
import socket
from copy import deepcopy

# pip3 libraries
import psutil

# Pattoo libraries
from pattoo_shared import agent
from pattoo_shared.configuration import Config
from pattoo_shared.variables import (
    DataPoint, DataPointMeta, DeviceDataPoints, DeviceGateway, AgentPolledData)
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
    ddv = DeviceDataPoints(agent_hostname, device_type=0)

    #########################################################################
    # Set non timeseries values
    #########################################################################

    metadata = []
    metadata.append(
        DataPointMeta('OperatingSystem_Release', platform.release()))
    metadata.append(
        DataPointMeta('OperatingSystem_Type', platform.system()))
    metadata.append(
        DataPointMeta('OperatingSystem_Version', platform.version()))
    metadata.append(
        DataPointMeta('OperatingSystem_CPUs', psutil.cpu_count()))
    metadata.append(
        DataPointMeta('Hostname', socket.getfqdn()))

    #########################################################################
    # Get timeseries values
    #########################################################################

    # Update agent with system data
    _stats_system(ddv, metadata)

    # Update agent with disk data
    _stats_disk_swap(ddv, metadata)
    _stats_disk_partitions(ddv, metadata)
    _stats_disk_io(ddv, metadata)

    # Update agent with network data
    _stats_network(ddv, metadata)

    # Add results to the AgentPolledData object for posting
    gateway.add(ddv)
    agentdata.add(gateway)
    return agentdata


def _stats_system(ddv, metadata):
    """Update agent with system data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    #########################################################################
    # Set timeseries values (Integers)
    #########################################################################

    ddv.add(DataPoint(
        'OperatingSystem_ProcessCount',
        len(psutil.pids()),
        data_type=DATA_INT).add(metadata))

    # Load averages
    (la_01, la_05, la_15) = os.getloadavg()

    ddv.add(DataPoint('load_average_01min', la_01,
                      data_type=DATA_INT).add(metadata))

    ddv.add(DataPoint('load_average_05min', la_05,
                      data_type=DATA_INT).add(metadata))

    ddv.add(DataPoint('load_average_15min', la_15,
                      data_type=DATA_INT).add(metadata))

    #########################################################################
    # Set timeseries values (Named Tuples)
    #########################################################################

    # Percentage CPU utilization
    ddv.add(_named_tuple_to_dv(
        psutil.cpu_times_percent(),
        'cpu_times_percent', data_type=DATA_FLOAT, metadata=metadata))

    # Get CPU runtimes
    ddv.add(_named_tuple_to_dv(
        psutil.cpu_times(),
        'cpu_times', data_type=DATA_COUNT64, metadata=metadata))

    # Get CPU stats
    ddv.add(_named_tuple_to_dv(
        psutil.cpu_stats(),
        data_label='cpu_stats', data_type=DATA_COUNT64, metadata=metadata))

    # Get memory utilization
    ddv.add(_named_tuple_to_dv(
        psutil.virtual_memory(),
        data_label='memory', data_type=DATA_INT, metadata=metadata))


def _stats_disk_swap(ddv, metadata):
    """Update agent with disk swap data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    # Initialize key variables
    result = []

    # Get swap information
    system_list = psutil.swap_memory()._asdict()
    for key, value in system_list.items():
        # Different suffixes have different data types
        if key in ['sin', 'sout']:
            data_type = DATA_COUNT64
        else:
            data_type = DATA_INT

        # No need to specify a suffix as there is only one swap
        _dv = DataPoint(key, value, data_type=data_type)
        _dv.add(metadata)
        _dv.add(DataPointMeta('Parameter', 'SwapMemory'))
        result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _stats_disk_partitions(ddv, metadata):
    """Update agent with disk partition data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    # Initialize key variables
    result = []

    # Get filesystem partition utilization
    diskddv = psutil.disk_partitions()
    # "diskddv" is named tuple describing partitions
    for item in diskddv:
        if "docker" not in str(mountpoint):
            # "source" is the partition mount point
            mountpoint = item.mountpoint

            # Add more metadata
            meta = []
            for key, value in item._asdict():
                meta.append(DataPointMeta(key, value))

            partition = psutil.disk_usage(mountpoint)._asdict()
            for key, value in partition.items():
                _dv = DataPoint(key, value, data_type=DATA_INT)
                _dv.add(meta)
                _dv.add(metadata)
                _dv.add(DataPointMeta('Parameter', 'PartitonUsage'))
                result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _stats_disk_io(ddv, metadata):
    """Update agent with disk io data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    # Initialize key variables
    regex = re.compile(r'^ram\d+$')
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
        for key, value in disk_dict.items():
            _dv = DataPoint(key, value, data_type=DATA_COUNT64)
            _dv.add(metadata)
            _dv.add(DataPointMeta('Partition', disk))
            _dv.add(DataPointMeta('Parameter', 'DiskIO'))
            result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _stats_network(ddv, metadata):
    """Update agent with network data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    # Initialize key variables
    result = []

    # Get network utilization
    nicddv = psutil.net_io_counters(pernic=True)
    for nic, nic_named_tuple in nicddv.items():
        nic_dict = nic_named_tuple._asdict()
        for key, value in nic_dict.items():
            _dv = DataPoint(key, value, data_type=DATA_COUNT64)
            _dv.add(metadata)
            _dv.add(DataPointMeta('interface', nic))
            _dv.add(DataPointMeta('Parameter', 'NetworkIO'))
            result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _named_tuple_to_dv(
        values, data_label=None, data_type=DATA_INT, metadata=None):
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
    for key, value in data_dict.items():
        _dv = DataPoint(key, value, data_type=data_type)
        _dv.add(metadata)
        _dv.add(DataPointMeta('Parameter', data_label))
        result.append(_dv)

    # Return
    return result
