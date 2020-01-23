#!/usr/bin/env python3
"""Pattoo library for collecting Modbus data."""

# Standard libraries
import multiprocessing
import sys
import asyncio
import time
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor

# Pattoo libraries
from pattoo_shared.variables import (
    DataPoint, DataPointMetadata, TargetDataPoints, AgentPolledData)
from .constants import PATTOO_AGENT_OPCUAD, OPCUAauth
from .configuration import ConfigOPCUA as Config


def blocking_poll(tpp):
    """Poll OPCUA agent data.

    Args:
        tpp: TargetDataPoints object

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    time.sleep(0.1)
    return (tpp, time.time())


async def run_blocking_poll(executor):
    """Get OPCUA agent data using per process asyncio.

    Args:
        executor: ProcessPoolExecutor object

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

    # Get current loop and create executor tasks
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, blocking_poll, tpp) for tpp in tpp_list]

    # Get results
    completed, _ = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    return results


def poll():
    """Get Modbus agent data.

    Performance data from Modbus enabled targets.

    Args:
        None

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize key variables
    results = None

    # Create a process pool for asyncio
    executor = ProcessPoolExecutor()

    # Setup asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    try:
        results = loop.run_until_complete(run_blocking_poll(executor))
    finally:
        loop.close()

    pprint(results)
