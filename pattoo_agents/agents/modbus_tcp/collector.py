#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing
import socket

# PIP libraries
from pymodbus.client.sync import ModbusTcpClient

# Pattoo libraries
from pattoo_agents.agents.modbus_tcp import configuration
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
    config = configuration.ConfigMODBUSTCP()
    registers4devices = {}

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_MODBUSTCPD
    agent_hostname = socket.getfqdn()
    agent_id = agent.get_agent_id(agent_program, agent_hostname)
    agentdata = AgentPolledData(agent_id, agent_program, agent_hostname)
    gateway = DeviceGateway(agent_hostname)

    # Get registers to be polled
    registervariables = config.registervariables()

    # Create a dict of register lists keyed by ip_device
    for registervariable in registervariables:
        for next_device in registervariable.ip_devices:
            if next_device in registers4devices:
                registers4devices[next_device].extend(
                    registervariable.registers)
            else:
                registers4devices[next_device] = registervariable.registers

    # Poll registers for all devices and update the DeviceDataVariables
    ddv_list = _parallel_poller(registers4devices)
    gateway.add(ddv_list)
    agentdata.add(gateway)

    # Return data
    return agentdata


def _parallel_poller(registers4devices):
    """Get data.

    Update the DeviceDataVariables with DataVariables

    Args:
        ip_devices: Dict of type SNMPVariable keyed by ip_device
        registers4devices: Dict of OID lists keyed by ip_device

    Returns:
        ddv_list: List of type DeviceDataVariables

    """
    # Initialize key variables
    arguments = []
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())

    # Poll all devices in sequence
    for ip_device, registers in sorted(registers4devices.items()):
        arguments.append((ip_device, registers))

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        ddv_list = pool.starmap(_serial_poller, arguments)

    # Wait for all the processes to end and get results
    pool.join()

    # Return
    return ddv_list


def _serial_poller(ip_device, registers):
    """Poll each spoke in parallel.

    Args:
        ip_device: Device to poll
        registers: Registers to poll

    Returns:
        ddv: DeviceDataVariables for the ip_device

    """
    # Intialize data gathering
    ddv = DeviceDataVariables(ip_device)

    # Get list of type DataVariable
    datavariables = []
    for register in registers:
        client = ModbusTcpClient(ip_device)
        response = client.read_input_registers(register)
        values = response.registers
        for value in values:
            datavariable = DataVariable(
                value=value, data_index=0,
                data_label=register, data_type=DATA_INT)
            datavariables.append(datavariable)
    ddv.add(datavariables)

    # Return
    return ddv
