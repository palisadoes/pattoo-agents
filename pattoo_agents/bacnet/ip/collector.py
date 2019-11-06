#!/usr/bin/env python3
"""Pattoo library for collecting BACnetIP data."""

# Standard libraries
import multiprocessing
import socket
from pprint import pprint

# Pattoo libraries
from pattoo_agents.bacnet.ip import configuration
from pattoo_shared import agent
from pattoo_shared import data
from pattoo_shared.constants import (
    PATTOO_AGENT_BACNETIPD, DATA_FLOAT, DATA_STRING)
from pattoo_shared.variables import (
    DataVariable, DeviceDataVariables, AgentPolledData, DeviceGateway)

_BACNET = None


def poll(bacnet):
    """Get BACnetIP agent data.

    Performance data from BACnetIP enabled devices.

    Args:
        None

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_BACNETIPD
    agent_hostname = socket.getfqdn()
    agent_id = agent.get_agent_id(agent_program, agent_hostname)
    agentdata = AgentPolledData(agent_id, agent_program, agent_hostname)
    gateway = DeviceGateway(agent_hostname)

    # Poll oids for all devices and update the DeviceDataVariables
    poller = _PollBACnetIP(bacnet)
    ddv_list = poller.data()
    gateway.add(ddv_list)
    agentdata.add(gateway)

    # Return data
    return agentdata


class _PollBACnetIP(object):
    """Poll BACnetIP devices."""

    def __init__(self, bacnet):
        """Initialize the class.

        Args:
            bacnet: BAC0 object

        Returns:
            None

        """
        # Initialize key variables.
        global _BACNET
        _BACNET = bacnet

        config = configuration.ConfigBACnetIP()
        self._ip_polltargets = {}

        # Get SNMP OIDs to be polled (Along with authorizations and ip_devices)
        device_poll_targets = config.device_polling_targets()

        # Create a dict of oid lists keyed by ip_device
        for dpt in device_poll_targets:
            # Ignore invalid data
            if dpt.valid is False:
                continue

            # Process
            next_device = dpt.device
            if next_device in self._ip_polltargets:
                self._ip_polltargets[next_device].extend(dpt.data)
            else:
                self._ip_polltargets[next_device] = dpt.data

    def data(self):
        """Get agent data.

        Update the DeviceDataVariables with DataVariables

        Args:
            None

        Returns:
            ddv_list: List of type DeviceDataVariables

        """
        # Initialize key variables
        arguments = []
        sub_processes_in_pool = max(1, multiprocessing.cpu_count())

        # Poll all devices in sequence
        for ip_device, dpts in sorted(self._ip_polltargets.items()):
            arguments.append((ip_device, dpts))

        # Create a pool of sub process resources
        with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

            # Create sub processes from the pool
            ddv_list = pool.starmap(_tester, arguments)

        # Wait for all the processes to end and get results
        pool.join()

        # Return
        return ddv_list


def _serial_poller(ip_device, polltargets):
    """Poll each spoke in parallel.

    Args:
        ip_device: Device to poll
        polltargets: List of PollingTarget objects to poll

    Returns:
        ddv: DeviceDataVariables for the SNMPVariable device

    """
    return []
    
    # Intialize data gathering
    global _BACNET
    ddv = DeviceDataVariables(ip_device)

    # Get list of type DataVariable
    datavariables = []
    for polltarget in polltargets:
        # Get polling results
        poller_string = (
            '{} analogValue {} presentValue'.format(
                ip_device, polltarget.address))
        data_label = (
            'analogValue point {} device {}'.format(
                polltarget.address, ip_device))
        value = _BACNET.read(poller_string)

        # Do multiplication
        if data.is_numeric(value) is True:
            value = float(value) * polltarget.multiplier
            data_type = DATA_FLOAT
        else:
            data_type = DATA_STRING

        # Update datavariables
        datavariable = DataVariable(
            value=value, data_label=data_label,
            data_index=0, data_type=data_type)
        datavariables.append(datavariable)

    # Return
    ddv.add(datavariables)
    return ddv


def _tester(x, y):
    return []
