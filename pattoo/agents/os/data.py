#!/usr/bin/env python3
"""Pattoo helper for the Linux _data.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
import os
import re
import platform
from collections import defaultdict

# pip3 libraries
import psutil

# Pattoo libraries
from pattoo.agents.os import language
from pattoo import log
from pattoo import daemon
from pattoo import agent
from pattoo.data import Data


def poll(agent_program):
    """Get all agent data.

    Performance data on linux server on which this application is installed.

    Args:
        agent_program: Agent program name

    Returns:
        None

    """
    # Intialize data gathering
    data = Data(agent_program)

    # Update agent with system data
    _get_data_system(data)

    # Update agent with disk data
    _get_data_storage(data)

    # Update agent with network data
    _get_data_network(data)

    #
    result = data.data()
    return result


def _get_data_system(_data):
    """Update agent with system data.

    Args:
        _data: Data object

    Returns:
        None

    """
    #########################################################################
    # Set non timeseries values
    #########################################################################

    _data.populate_single('release', platform.release(), base_type=None)
    _data.populate_single('system', platform.system(), base_type=None)
    _data.populate_single('version', platform.version(), base_type=None)
    _data.populate_single('cpu_count', psutil.cpu_count(), base_type=1)

    #########################################################################
    # Set timeseries values
    #########################################################################
    _data.populate_single(
        'process_count', len(psutil.pids()), base_type=1)

    _data.populate_named_tuple(
        'cpu_times_percent', psutil.cpu_times_percent(), base_type=1)

    # Load averages
    (la_01, la_05, la_15) = os.getloadavg()
    _data.populate_single(
        'load_average_01min', la_01, base_type=1)
    _data.populate_single(
        'load_average_05min', la_05, base_type=1)
    _data.populate_single(
        'load_average_15min', la_15, base_type=1)

    # Get CPU times
    _data.populate_named_tuple(
        'cpu_times', psutil.cpu_times(), base_type=64)

    # Get CPU stats
    _data.populate_named_tuple(
        'cpu_stats', psutil.cpu_stats(), base_type=64)

    # Get memory utilization
    _data.populate_named_tuple('memory', psutil.virtual_memory())


def _get_data_storage(_data):
    """Update agent with disk data.

    Args:
        _data: Data object

    Returns:
        None

    """
    # Initialize key variables
    regex = re.compile(r'^ram\d+$')

    # Get swap utilization
    multikey = defaultdict(lambda: defaultdict(dict))
    counterkey = defaultdict(lambda: defaultdict(dict))
    swap_data = psutil.swap_memory()
    system_list = swap_data._asdict()
    # "label" is named tuple describing partitions
    for label in system_list:
        value = system_list[label]
        if label in ['sin', 'sout']:
            counterkey[label][None] = value
        else:
            multikey[label][None] = value
    _data.populate_dict('swap', multikey)
    _data.populate_dict('swap', counterkey, base_type=64)

    # Get filesystem partition utilization
    disk_data = psutil.disk_partitions()
    multikey = defaultdict(lambda: defaultdict(dict))
    # "disk" is named tuple describing partitions
    for disk in disk_data:
        # "source" is the partition mount point
        source = disk.mountpoint
        if "docker" in str(source):
            pass
        else:
            system_data = psutil.disk_usage(source)
            system_dict = system_data._asdict()
            for label, value in system_dict.items():
                multikey[label][source] = value
    _data.populate_dict('disk_usage', multikey)

    # Get disk I/O usage
    io_data = psutil.disk_io_counters(perdisk=True)
    counterkey = defaultdict(lambda: defaultdict(dict))
    # "source" is disk name
    for source in io_data.keys():
        # No RAM pseudo disks. RAM disks OK.
        if bool(regex.match(source)) is True:
            continue
        system_data = io_data[source]
        system_dict = system_data._asdict()
        for label, value in system_dict.items():
            counterkey[label][source] = value
    _data.populate_dict('disk_io', counterkey, base_type=64)


def _get_data_network(_data):
    """Update agent with network data.

    Args:
        _data: Data object

    Returns:
        None

    """
    # Get network utilization
    nic_data = psutil.net_io_counters(pernic=True)
    counterkey = defaultdict(lambda: defaultdict(dict))
    for source in nic_data.keys():
        # "source" is nic name
        system_data = nic_data[source]
        system_dict = system_data._asdict()
        for label, value in system_dict.items():
            counterkey[label][source] = value
    _data.populate_dict('network', counterkey, base_type=64)
