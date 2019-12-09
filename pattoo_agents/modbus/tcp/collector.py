#!/usr/bin/env python3
"""Pattoo library for collecting Modbus data."""

# Standard libraries
import multiprocessing
import sys

# PIP libraries
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.pdu import ExceptionResponse
from pymodbus.exceptions import ModbusIOException, ConnectionException

# Pattoo libraries
from pattoo_agents.modbus.tcp import configuration
from pattoo_agents.modbus.variables import (
    InputRegisterVariable, HoldingRegisterVariable, RegisterVariable)
from pattoo_shared import log
from pattoo_shared.constants import DATA_INT
from pattoo_shared.variables import (
    AgentKey, DataPoint, DataPointMetadata, TargetDataPoints, AgentPolledData)
from .constants import PATTOO_AGENT_MODBUSTCPD


def poll():
    """Get Modbus agent data.

    Performance data from Modbus enabled targets.

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
    agentdata = AgentPolledData(agent_program, config)

    # Get registers to be polled
    drvs = config.registervariables()

    # Create a dict of register lists keyed by ip_target
    for drv in drvs:
        arguments.append((drv,))

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


def _serial_poller(drv):
    """Poll each spoke in parallel.

    Args:
        drv: Target to poll
        input_registers: Input registers to poll
        holding_registers: Holding registers to poll

    Returns:
        ddv: TargetDataPoints for the ip_target

    """
    # Intialize data gathering
    ip_target = drv.target
    ddv = TargetDataPoints(ip_target)
    prefix = AgentKey(PATTOO_AGENT_MODBUSTCPD)

    # Get list of type DataPoint
    datapoints = []
    for _rv in drv.data:
        # Ignore invalid data
        if isinstance(_rv, RegisterVariable) is False:
            continue
        if _rv.valid is False:
            continue

        # Poll
        client = ModbusTcpClient(ip_target)
        if isinstance(_rv, InputRegisterVariable):
            try:
                response = client.read_input_registers(
                    _rv.address, count=_rv.count, unit=_rv.unit)
                key = prefix.key('input_register')
            except ConnectionException as _err:
                log_message = ('''\
Cannot connect to target {} to retrieve input register {}, count {}, \
unit {}: {}'''.format(ip_target, _rv.register, _rv.count, _rv.unit, str(_err)))
                log.log2warning(51028, log_message)
                continue
            except:
                log_message = ('''\
Cause unknown failure with target {} getting input register {}, count {}, \
unit {}'''.format(ip_target, _rv.register, _rv.count, _rv.unit))
                log.log2warning(51030, log_message)
                continue
        elif isinstance(_rv, HoldingRegisterVariable):
            try:
                response = client.read_holding_registers(_rv.address)
                key = prefix.key('holding_register')
            except ConnectionException:
                log_message = ('''\
Cannot connect to target {} to retrieve input register {}, count {}, \
unit {}'''.format(ip_target, _rv.register, _rv.count, _rv.unit))
                log.log2warning(51032, log_message)
                continue
            except:
                log_message = ('''\
Cause unknown failure with target {} getting holding register {}, count {}, \
unit {}. [{}, {}, {}]\
'''.format(ip_target, _rv.register, _rv.count, _rv.unit, sys.exc_info()[0],
           sys.exc_info()[1], sys.exc_info()[2]))
                log.log2warning(51031, log_message)
                continue

        # Process data
        if response.isError() is True:
            _log_modbus(ip_target, _rv, response)
        else:
            values = response.registers
            for data_index, _value in enumerate(values):
                # Do multiplication
                value = _value * _rv.multiplier

                # Create DataPoint and append
                new_key = ('''{}_{}_unit_{}\
'''.format(key, _rv.register + data_index, str(_rv.unit).zfill(3)))
                datapoint = DataPoint(new_key, value, data_type=DATA_INT)
                datapoints.append(datapoint)
    ddv.add(datapoints)

    # Return
    return ddv


def _log_modbus(ip_target, registervariable, response):
    """Log error.

    Args:
        ip_target: Target that caused the error
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
        4: '''Slave Target Failure. Unrecoverable error occurred while slave \
was attempting to perform requested action''',
        5: '''Acknowledge. Slave has accepted request and is processing it, \
but a long duration of time is required. This response is returned to \
prevent a timeout error from occurring in the master. Master can next issue \
a Poll Program Complete message to determine whether processing is \
completed''',
        6: '''Slave Target Busy. Slave is engaged in processing a \
long-duration command. Master should retry later''',
        7: '''Negative Acknowledge. Slave cannot perform the programming \
functions. Master should request diagnostic or error information from slave''',
        8: '''Memory Parity Error. Slave detected a parity error in memory. \
Master can retry the request, but service may be required on the \
slave target''',
        10: '''Gateway Path Unavailable. Specialized for Modbus gateways. \
Indicates a misconfigured gateway''',
        11: '''Gateway Target Target Failed to Respond. Specialized for \
Modbus gateways. Sent when slave fails to respond'''
    }

    # Intialize data gathering
    if isinstance(response, ExceptionResponse):
        # Provide more context if required.
        if response.exception_code in exception_codes:
            description = ' Description: {}'.format(
                exception_codes[response.exception_code])
        else:
            description = ''

        # Register does not exist
        log_message = ('''\
Target failure {}: Could not read register {}, count {}, unit {}: \
original code {}, exception code {}, function code {}, check {}, \
protocol ID {}, transaction ID {}, unit ID {}.{}\
'''.format(ip_target,
           registervariable.register, registervariable.count,
           registervariable.unit,
           response.original_code, response.exception_code,
           response.function_code, response.check, response.protocol_id,
           response.transaction_id, response.unit_id, description))
        log.log2warning(51027, log_message)

    elif isinstance(response, ModbusIOException):
        # Target may not be available or not listening on Modbus port
        log_message = ('''\
Pymodbus failure code {}. Message: {}\
'''.format(response.fcode, response.message))
        log.log2warning(51026, log_message)
