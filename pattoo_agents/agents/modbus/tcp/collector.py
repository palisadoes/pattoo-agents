#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing
import socket
import sys

# PIP libraries
from pymodbus.client.sync import ModbusTcpClient

# Pattoo libraries
from pattoo_agents.agents.modbus.tcp import configuration
from pattoo_agents.agents.modbus.variables import (
    InputRegisterVariable, HoldingRegisterVariable, RegisterVariable)
from pattoo_shared import agent
from pattoo_shared.constants import PATTOO_AGENT_MODBUSTCPD, DATA_INT
from pattoo_shared.variables import (
    DataVariable, DeviceDataVariables, AgentPolledData, DeviceGateway)


def poll():
    """Get PATOO_SNMP agent data.

    Performance data from SNMP enabled devices.

    Args:
        None

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize key variables.
    config = configuration.ConfigModbusTCP()
    arguments = []

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_MODBUSTCPD
    agent_hostname = socket.getfqdn()
    agent_id = agent.get_agent_id(agent_program, agent_hostname)
    agentdata = AgentPolledData(agent_id, agent_program, agent_hostname)
    gateway = DeviceGateway(agent_hostname)

    # Get registers to be polled
    drvs = config.registervariables()

    # Create a dict of register lists keyed by ip_device
    for drv in drvs:
        arguments.append((drv,))

    # Poll registers for all devices and update the DeviceDataVariables
    ddv_list = _parallel_poller(arguments)
    gateway.add(ddv_list)
    agentdata.add(gateway)

    # Return data
    return agentdata


def _parallel_poller(arguments):
    """Get data.

    Update the DeviceDataVariables with DataVariables

    Args:
        arguments: List of arguments for _serial_poller

    Returns:
        ddv_list: List of type DeviceDataVariables

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


def _serial_poller(drv):
    """Poll each spoke in parallel.

    Args:
        drv: Device to poll
        input_registers: Input registers to poll
        holding_registers: Holding registers to poll

    Returns:
        ddv: DeviceDataVariables for the ip_device

    """
    # Intialize data gathering
    ip_device = drv.device
    ddv = DeviceDataVariables(ip_device)

    # Get list of type DataVariable
    datavariables = []
    for _rv in drv.data:
        # Ignore invalid data
        if isinstance(_rv, RegisterVariable) is False:
            continue
        if _rv.active is False:
            continue

        # Poll    
        client = ModbusTcpClient(ip_device)
        if isinstance(_rv, InputRegisterVariable):
            response = client.read_input_registers(_rv.address)
        elif isinstance(_rv, HoldingRegisterVariable):
            response = client.read_holding_registers(_rv.address)
        values = response.registers
        for data_index, value in enumerate(values):
            datavariable = DataVariable(
                value=value, data_index='{}_{}'.format(data_index, _rv.unit),
                data_label=_rv.address, data_type=DATA_INT)
            datavariables.append(datavariable)
    ddv.add(datavariables)
    print('--V--', ddv)

    # Return
    return ddv
