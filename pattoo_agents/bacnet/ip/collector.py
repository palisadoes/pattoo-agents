#!/usr/bin/env python3
"""Pattoo library for collecting BACnetIP data."""

# Standard libraries
import sys

# PIP libraries
from BAC0.core.io.IOExceptions import (
    UnknownObjectError, NoResponseFromController)

# Pattoo libraries
from pattoo_agents.bacnet.ip import configuration
from pattoo_shared import data
from pattoo_shared import log
from pattoo_shared.constants import DATA_FLOAT, DATA_STRING
from pattoo_shared.variables import (
    AgentKey, DataPoint, DataPointMetadata, TargetDataPoints, AgentPolledData)
from .constants import PATTOO_AGENT_BACNETIPD


def poll(bacnet):
    """Get BACnetIP agent data.

    Performance data from BACnetIP enabled devices.

    Args:
        None

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize key variables.
    config = configuration.ConfigBACnetIP()

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_BACNETIPD
    agentdata = AgentPolledData(agent_program, config)

    # Poll oids for all devices and update the TargetDataPoints
    poller = _PollBACnetIP(bacnet)
    ddv_list = poller.data()
    agentdata.add(ddv_list)

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

        Update the TargetDataPoints with DataPoints

        Args:
            None

        Returns:
            ddv_list: List of type TargetDataPoints

        """
        # Initialize key variables
        arguments = []
        ddv_list = []

        # Poll all devices in sequence
        for ip_device, dpts in sorted(self._ip_polltargets.items()):
            arguments.append((ip_device, dpts))

        for ip_device, dpts in arguments:
            result = self._get_device_datapoints(ip_device, dpts)
            if result.valid is True:
                ddv_list.append(result)

        # Return
        return ddv_list

    def _get_device_datapoints(self, ip_device, polltargets):
        """Poll each spoke in parallel.

        Args:
            ip_device: Device to poll
            polltargets: List of PollingTarget objects to poll
            bacnet: BAC0 connect object

        Returns:
            ddv: TargetDataPoints for the SNMPVariable device

        """
        # Intialize data gathering
        ddv = TargetDataPoints(ip_device)
        prefix = AgentKey(PATTOO_AGENT_BACNETIPD)

        # Get list of type DataPoint
        datapoints = []
        for polltarget in polltargets:
            # Get polling results
            value = poll_device_address(
                ip_device, polltarget.address, 'presentValue', self._bacnet)
            name = poll_device_address(
                ip_device, polltarget.address, 'objectName', self._bacnet)

            # Skip if invalid data is received
            if value is None:
                continue

            # Do multiplication
            if data.is_numeric(value) is True:
                value = float(value) * polltarget.multiplier
                data_type = DATA_FLOAT
            else:
                data_type = DATA_STRING

            # Update datapoints
            datapoint = DataPoint(
                prefix.key('analog_value_point_{}'.format(polltarget.address)),
                value,
                data_type=data_type)
            datapoint.add(
                DataPointMetadata(prefix.key('device'), ip_device))
            if name is not None:
                datapoint.add(DataPointMetadata(
                    prefix.key('object_name'), name))
            datapoints.append(datapoint)

        # Return
        ddv.add(datapoints)
        return ddv


def poll_device_address(ip_device, address, object2poll, bacnet):
    """Poll each spoke in parallel.

    Args:
        ip_device: Device to poll
        polltargets: List of PollingTarget objects to poll
        bacnet: BAC0 connect object

    Returns:
        result: Result of the poll

    """
    # Intialize data gathering
    result = None
    poller_string = (
        '{} analogValue {} {}'.format(ip_device, address, object2poll))

    try:
        result = bacnet.read(poller_string)
    except NoResponseFromController:
        log_message = (
            'No BACnet response from {}. Timeout.'.format(ip_device))
        log.log2warning(51004, log_message)
    except UnknownObjectError:
        log_message = ('''\
Unknown BACnet object {} requested from device {}.\
'''.format(object2poll, ip_device))
        log.log2warning(51005, log_message)
    except Exception as reason:
        log_message = ('BACnet error polling {}. Reason: {}'.format(
            ip_device, str(reason)))
        log.log2warning(51006, log_message)
    except:
        log_message = ('''Unknown BACnet error polling {}: [{}, {}, {}]\
'''.format(ip_device, sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
        log.log2warning(51007, log_message)

    # Return
    return result
