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
from pattoo_shared.configuration import Config
from pattoo_shared.variables import (
    DataPoint, DataPointMetadata, DeviceDataPoints, AgentPolledData)
from pattoo_shared.constants import (
    DATA_INT, DATA_COUNT64, DATA_FLOAT)


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

    # Initialize AgentPolledData
    agent_hostname = socket.getfqdn()
    agentdata = AgentPolledData(agent_program, config)

    # Intialize data gathering
    ddv = DeviceDataPoints(agent_hostname)

    #########################################################################
    # Set non timeseries values
    #########################################################################

    metadata = []
    metadata.append(
        DataPointMetadata('operating_system_release', platform.release()))
    metadata.append(
        DataPointMetadata('operating_system_type', platform.system()))
    metadata.append(
        DataPointMetadata('operating_system_version', platform.version()))
    metadata.append(
        DataPointMetadata('operating_system_cpus', psutil.cpu_count()))
    metadata.append(
        DataPointMetadata('operating_system_hostname', socket.getfqdn()))

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
    agentdata.add(ddv)
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
        'operating_system_process_count',
        len(psutil.pids()),
        data_type=DATA_INT).add(metadata))

    # Load averages
    (la_01, la_05, la_15) = os.getloadavg()

    ddv.add(DataPoint('operating_system_load_average_01min', la_01,
                      data_type=DATA_INT).add(metadata))

    ddv.add(DataPoint('operating_system_load_average_05min', la_05,
                      data_type=DATA_INT).add(metadata))

    ddv.add(DataPoint('operating_system_load_average_15min', la_15,
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
        'cpu_stats', data_type=DATA_COUNT64, metadata=metadata))

    # Get memory utilization
    ddv.add(_named_tuple_to_dv(
        psutil.virtual_memory(),
        'memory', data_type=DATA_INT, metadata=metadata))


def _stats_disk_swap(ddv, metadata):
    """Update agent with disk swap data.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        None

    """
    # Initialize key variables
    result = []
    prefix = 'operating_system_swap_memory_'

    # Get swap information
    system_list = psutil.swap_memory()._asdict()
    for key, value in system_list.items():
        # Different suffixes have different data types
        if key in ['sin', 'sout']:
            data_type = DATA_COUNT64
        else:
            data_type = DATA_INT

        # No need to specify a suffix as there is only one swap
        _dv = DataPoint('{}{}'.format(prefix, key), value, data_type=data_type)
        _dv.add(metadata)
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
    prefix = 'operating_system_disk_partition_'

    # Get filesystem partition utilization
    items = psutil.disk_partitions()
    # "items" is a list of named tuples describing partitions
    for item in items:
        # "source" is the partition mount point
        mountpoint = item.mountpoint
        if "docker" not in str(mountpoint):
            # Add more metadata
            meta = []
            meta.append(DataPointMetadata('{}device'.format(prefix), item.device))
            meta.append(DataPointMetadata(
                '{}mountpoint'.format(prefix), item.mountpoint))
            meta.append(DataPointMetadata('{}fstype'.format(prefix), item.fstype))
            meta.append(DataPointMetadata('{}opts'.format(prefix), item.opts))

            # Get the partition data
            partition = psutil.disk_usage(mountpoint)._asdict()
            for key, value in partition.items():
                _dv = DataPoint(
                    '{}disk_usage_{}'.format(prefix, key),
                    value, data_type=DATA_INT)
                _dv.add(meta)
                _dv.add(metadata)
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
    prefix = 'operating_system_disk_io_'

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
            _dv = DataPoint(
                '{}{}'.format(prefix, key), value, data_type=DATA_COUNT64)
            _dv.add(metadata)
            _dv.add(DataPointMetadata('operating_system_disk_partition', disk))
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
    prefix = 'operating_system_network_io_'

    # Get network utilization
    nicddv = psutil.net_io_counters(pernic=True)
    for nic, nic_named_tuple in nicddv.items():
        nic_dict = nic_named_tuple._asdict()
        for key, value in nic_dict.items():
            _dv = DataPoint(
                '{}{}'.format(prefix, key), value, data_type=DATA_COUNT64)
            _dv.add(metadata)
            _dv.add(DataPointMetadata('{}interface'.format(prefix), nic))
            result.append(_dv)

    # Add the result to data
    ddv.add(result)


def _named_tuple_to_dv(
        values, parameter_label, data_type=DATA_INT, metadata=None):
    """Convert a named tuple to a list of DataPoint objects.

    Args:
        values: Named tuple
        parameter_label: parameter_label
        data_type: Data type

    Returns:
        result: List of DataPoint

    """
    # Get data
    data_dict = values._asdict()
    result = []
    prefix = 'operating_system_'

    # Cycle through results
    for key, value in data_dict.items():
        _dv = DataPoint(
            '{}{}{}'.format(prefix, parameter_label, key),
            value,
            data_type=data_type)
        _dv.add(metadata)
        result.append(_dv)

    # Return
    return result
