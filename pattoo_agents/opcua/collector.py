#!/usr/bin/env python3
"""Pattoo library for collecting Modbus data."""

# Standard libraries
import multiprocessing
import asyncio
import sys
from time import sleep

# PIP libraries
from asyncua import Client
from asyncua.ua.uaerrors import BadNodeIdUnknown

# Pattoo libraries
from pattoo_shared.variables import (
    DataPoint, DataPointMetadata, PollingPoint, AgentPolledData,
    TargetDataPoints, TargetPollingPoints)
from pattoo_shared import log
from pattoo_shared.data import is_numeric

from .constants import PATTOO_AGENT_OPCUAD, OPCUAauth
from .configuration import ConfigOPCUA as Config


def poll():
    """Get Modbus agent data.

    Performance data from Modbus enabled targets.

    Args:
        None

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize key variables.
    config = Config()
    _pi = config.polling_interval()

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_OPCUAD
    agentdata = AgentPolledData(agent_program, _pi)

    # Get registers to be polled
    tpp_list = config.target_polling_points()
    arguments = [(tpp,) for tpp in tpp_list]

    # Poll registers for all targets and update the TargetDataPoints
    target_datapoints_list = _parallel_poller(arguments)
    agentdata.add(target_datapoints_list)

    # Return data
    return agentdata


def _parallel_poller(arguments):
    """Get data.

    Update the TargetDataPoints with DataPoints

    Args:
        arguments: List of arguments for _serial_poller

    Returns:
        target_datapoints_list: List of type TargetDataPoints

    """
    # Initialize key variables
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        target_datapoints_list = pool.starmap(_serial_poller, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Return
    return target_datapoints_list


def _serial_poller(argument):
    """Get OPCUA agent data.

    Args:
        argument: TargetPollingPoints object

    Returns:
        datapoints: List of DataPoint objects

    """
    # Sleep for a very short time to make sure process stabilizes
    sleep(0.1)

    # Get data
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    target_datapoints = loop.run_until_complete(_serial_poller_async(argument))
    loop.close()
    return target_datapoints


async def _serial_poller_async(tpp):
    """Poll OPCUA agent data.

    Args:
        tpp: TargetDataPoints object

    Returns:
        target_datapoints: TargetDataPoints object

    """
    # Initialize key variables
    connected = False

    # Test for validity
    if isinstance(tpp, TargetPollingPoints) is False:
        return None
    if isinstance(tpp.target, OPCUAauth) is False:
        return None
    if tpp.valid is False:
        return None

    # Create URL for polling
    ip_target = tpp.target.ip_target
    ip_port = tpp.target.ip_port
    username = tpp.target.username
    password = tpp.target.password
    url = 'opc.tcp://{}:{}'.format(ip_target, ip_port)

    # Intialize data gathering
    target_datapoints = TargetDataPoints(ip_target)

    # Create a client object to connect to OPCUA server
    client = Client(url=url)
    client.set_user(username)
    client.set_password(password)

    # Connect
    try:
        await client.connect()
        connected = True
    except:
        log_message = (
            'Authentication for polling target {} is incorrect'.format(url))
        log.log2warning(51011, log_message)
        pass

    if connected is True:
        for point in tpp.data:
            # Make sure we have the right data type
            if isinstance(point, PollingPoint) is False:
                log_message = ('''\
Invalid polling point {} for OPC UA URL {}'''.format(point, url))
                log.log2info(51012, log_message)
                continue

            # Get data
            address = point.address
            try:
                node = client.get_node(address)
                value = await node.read_value()
            except BadNodeIdUnknown:
                log_message = ('''\
OPC UA node {} not found on server {}'''.format(address, url))
                log.log2warning(51015, log_message)
                continue
            except:
                _exception = sys.exc_info()
                log_message = ('OPC UA server communication error')
                log.log2exception(51014, _exception, message=log_message)
                log_message = ('''\
Cannot get value from polling point {} for OPC UA URL {}\
'''.format(address, url))
                log.log2info(51013, log_message)
                continue

            # Create datapoint
            if bool(point.multiplier) is True:
                if is_numeric(value) is True and (
                        is_numeric(point.multiplier) is True):
                    value = value * point.multiplier
            else:
                value = 0
            datapoint = DataPoint(address, value)
            datapoint.add(DataPointMetadata('OPCUA Server', ip_target))
            target_datapoints.add(datapoint)

        # Disconnect client
        await client.disconnect()

    return target_datapoints
