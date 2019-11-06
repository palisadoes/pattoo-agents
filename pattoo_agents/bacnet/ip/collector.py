#!/usr/bin/env python3
"""Pattoo library for collecting BACnetIP data."""

# Standard libraries
import socket

# PIP libraries
from BAC0.core.io.IOExceptions import (
    UnknownObjectError, NoResponseFromController)

# Pattoo libraries
from pattoo_agents.bacnet.ip import configuration
from pattoo_shared import agent
from pattoo_shared import data
from pattoo_shared import log
from pattoo_shared.constants import (
    PATTOO_AGENT_BACNETIPD, DATA_FLOAT, DATA_STRING)
from pattoo_shared.variables import (
    DataVariable, DeviceDataVariables, AgentPolledData, DeviceGateway)


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
        self._bacnet = bacnet

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
        ddv_list = []

        # Poll all devices in sequence
        for ip_device, dpts in sorted(self._ip_polltargets.items()):
            arguments.append((ip_device, dpts))

        for ip_device, dpts in arguments:
            result = self._serial_poller(ip_device, dpts)
            if result.valid is True:
                ddv_list.append(result)

        # Return
        return ddv_list

    def _serial_poller(self, ip_device, polltargets):
        """Poll each spoke in parallel.

        Args:
            ip_device: Device to poll
            polltargets: List of PollingTarget objects to poll
            bacnet: BAC0 connect object

        Returns:
            ddv: DeviceDataVariables for the SNMPVariable device

        """
        # Intialize data gathering
        ddv = DeviceDataVariables(ip_device)
        object2poll = 'analogValue'

        # Get list of type DataVariable
        datavariables = []
        for polltarget in polltargets:
            # Get polling results
            poller_string = (
                '{} {} {} presentValue'.format(
                    object2poll, ip_device, polltarget.address))

            try:
                value = self._bacnet.read(poller_string)
            except NoResponseFromController:
                log_message = (
                    'No BACnet response from {}. Timeout.'.format(ip_device))
                log.log2info(51004, log_message)
                continue
            except UnknownObjectError:
                log_message = ('''\
Unknown BACnet object {} requested from device {}.\
'''.format(object2poll, ip_device))
                log.log2info(51005, log_message)
                continue
            except:
                log_message = (
                    'Unknown BACnet error polling {}.'.format(ip_device))
                log.log2info(51006, log_message)
                continue

            # Do multiplication
            if data.is_numeric(value) is True:
                value = float(value) * polltarget.multiplier
                data_type = DATA_FLOAT
            else:
                data_type = DATA_STRING

            # Setup the data label
            data_label = (
                'analogValue point {} device {}'.format(
                    polltarget.address, ip_device))

            # Update datavariables
            datavariable = DataVariable(
                value=value, data_label=data_label,
                data_index=0, data_type=data_type)
            datavariables.append(datavariable)

        # Return
        ddv.add(datavariables)
        return ddv
