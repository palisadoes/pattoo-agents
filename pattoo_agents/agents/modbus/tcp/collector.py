#!/usr/bin/env python3
"""Pattoo library for collecting SNMP data."""

# Standard libraries
import multiprocessing
import socket

# PIP libraries
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.pdu import ExceptionResponse
from pymodbus.exceptions import ModbusIOException, ConnectionException

# Pattoo libraries
from pattoo_agents.agents.modbus.tcp import configuration
from pattoo_agents.agents.modbus.variables import (
    InputRegisterVariable, HoldingRegisterVariable, RegisterVariable)
from pattoo_shared import agent
from pattoo_shared import log
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
        if _rv.valid is False:
            continue

        # Poll
        client = ModbusTcpClient(ip_device)
        if isinstance(_rv, InputRegisterVariable):
            try:
                response = client.read_input_registers(_rv.address)
            except ConnectionException:
                log_message = ('''\
Cannot connect to device {} to retrieve input register {}, count {}, \
unit {}'''.format(ip_device, _rv.register, _rv.count, _rv.unit))
                log.log2info(51028, log_message)
                continue
            except:
                log_message = ('''\
Cause unknown failure with device {} getting input register {}, count {}, \
unit {}'''.format(ip_device, _rv.register, _rv.count, _rv.unit))
                log.log2info(51030, log_message)
                continue
        elif isinstance(_rv, HoldingRegisterVariable):
            try:
                response = client.read_holding_registers(_rv.address)
            except ConnectionException:
                log_message = ('''\
Cannot connect to device {} to retrieve input register {}, count {}, \
unit {}'''.format(ip_device, _rv.register, _rv.count, _rv.unit))
                log.log2info(51032, log_message)
                continue
            except:
                log_message = ('''\
Cause unknown failure with device {} getting holding register {}, count {}, \
unit {}'''.format(ip_device, _rv.register, _rv.count, _rv.unit))
                log.log2info(51031, log_message)
                continue

        # Process data
        if response.isError() is True:
            _log_modbus(ip_device, _rv, response)
        else:
            values = response.registers
            for data_index, value in enumerate(values):
                datavariable = DataVariable(
                    value=value,
                    data_index='{}_{}'.format(data_index, _rv.unit),
                    data_label=_rv.address,
                    data_type=DATA_INT)
                datavariables.append(datavariable)
    ddv.add(datavariables)

    # Return
    return ddv


def _log_modbus(ip_device, registervariable, response):
    """Log error.

    Args:
        ip_device: Device that caused the error
        registervariable: RegisterVariable object
        response: Pymodbus response object

    Returns:
        None

    """
    # Initialize key variables
    exception_codes = {
        1: '''Illegal Function. Function code received in the query is not \
    recognized or allowed by slave''',
        2: '''Illegal Data Address. Data address of some or all the required \
    entities are not allowed or do not exist in slave''',
        3: '''Illegal Data Value. Value is not accepted by slave''',
        4: '''Slave Device Failure. Unrecoverable error occurred while slave \
was attempting to perform requested action''',
        5: '''Acknowledge. Slave has accepted request and is processing it, \
but a long duration of time is required. This response is returned to \
prevent a timeout error from occurring in the master. Master can next issue \
a Poll Program Complete message to determine whether processing is \
completed''',
        6: '''Slave Device Busy. Slave is engaged in processing a \
long-duration command. Master should retry later''',
        7: '''Negative Acknowledge. Slave cannot perform the programming \
functions. Master should request diagnostic or error information from slave''',
        8: '''Memory Parity Error. Slave detected a parity error in memory. \
Master can retry the request, but service may be required on the \
slave device''',
        10: '''Gateway Path Unavailable. Specialized for Modbus gateways. \
Indicates a misconfigured gateway''',
        11: '''Gateway Target Device Failed to Respond. Specialized for \
Modbus gateways. Sent when slave fails to respond'''
    }

    # Intialize data gathering
    if isinstance(response, ExceptionResponse):
        # Provide more context if required.
        if response.exception in exception_codes:
            description = ' Description: {}'.format(
                exception_codes[response.exception])
        else:
            description = ''

        # Register does not exist
        log_message = ('''\
Device failure {}: Could not read register {}, count {}, unit {}: \
original code {}, exception code {}, function code {}, check {}, \
protocol ID {}, transaction ID {}, unit ID {}.{}\
'''.format(ip_device,
           registervariable.register, registervariable.count,
           registervariable.unit,
           response.original_code, response.exception_code,
           response.function_code, response.check, response.protocol_id,
           response.transaction_id, response.unit_id, description))
        log.log2info(51027, log_message)

    elif isinstance(response, ModbusIOException):
        # Device may not be available or not listening on Modbus port
        log_message = ('''\
Pymodbus failure code {}. Message: {}\
'''.format(response.fcode, response.message))
        log.log2info(51026, log_message)
