#!/usr/bin/env python3
"""Pattoo library for collecting Modbus data."""


# Standard libraries
# from asyncua import Client
import multiprocessing
import asyncio
import time

# Pattoo libraries
from pattoo_shared.variables import (
    DataPoint, AgentPolledData, TargetPollingPoints)
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
    ddv_list = _parallel_poller(arguments)
    agentdata.add(ddv_list)

    # Return data
    return agentdata


def _parallel_poller(arguments):
    """Get data.

    Update the TargetDataPoints with DataPoints

    Args:
        arguments: List of arguments for _serial_poller

    Returns:
        ddv_list: List of type TargetDataPoints

    """
    # Initialize key variables
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        ddv_list = pool.starmap(_serial_poller, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Return
    return ddv_list


def _serial_poller(argument):
    """Get OPCUA agent data.

    Args:
        argument: TargetPollingPoints object

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    value, _ = loop.run_until_complete(_serial_poller_async(argument))
    loop.close()
    return value


async def _serial_poller_async(tpp):
    """Poll OPCUA agent data.

    Args:
        tpp: TargetDataPoints object

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize key variables
    connected = False
    values = []

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

    for point in tpp.data:
        print(url, point)

    '''
    # Create a client object to connect to OPCUA server
    client = Client(url=url)
    client.set_user('opcuauser')
    client.set_password('password')

    # Connect
    try:
        await client.connect()
        connected = True
    except:
        pass

    if connected is True:
        for point in tpp.data:
            # Get data
            try:
                node = client.get_node(point)
                value = await node.read_value()
                values.append(DataPoint(point, value))
            except:
                pass

        # Disconnect client
        await client.disconnect()
    '''

    time.sleep(0.1)
    return (tpp, time.time())
