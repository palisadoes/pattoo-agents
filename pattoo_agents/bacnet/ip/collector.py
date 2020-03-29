#!/usr/bin/env python3
"""Pattoo library for collecting BACnetIP data."""

# Standard libraries
import sys

# PIP libraries
from BAC0.core.io.IOExceptions import (
    UnknownObjectError, NoResponseFromController)

# Pattoo libraries
from pattoo_agents.bacnet.ip import configuration
from pattoo_shared import network
from pattoo_shared import data
from pattoo_shared import log
from pattoo_shared.constants import DATA_FLOAT, DATA_STRING
from pattoo_shared.variables import (
    DataPoint, DataPointMetadata, TargetDataPoints, AgentPolledData)
from .constants import PATTOO_AGENT_BACNETIPD


def poll(bacnet):
    """Get BACnetIP agent data.

    Performance data from BACnetIP enabled targets.

    Args:
        None

    Returns:
        agentdata: AgentPolledData object for all data gathered by the agent

    """
    # Initialize key variables.
    config = configuration.ConfigBACnetIP()
    _pi = config.polling_interval()

    # Initialize AgentPolledData
    agent_program = PATTOO_AGENT_BACNETIPD
    agentdata = AgentPolledData(agent_program, _pi)

    # Poll oids for all targets and update the TargetDataPoints
    poller = _PollBACnetIP(bacnet)
    ddv_list = poller.data()
    agentdata.add(ddv_list)

    # Return data
    return agentdata


class _PollBACnetIP():
    """Poll BACnetIP targets."""

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

        # Get points to be polled (Along with authorizations and ip_targets)
        self._target_poll_targets = config.target_polling_points()

    def data(self):
        """Get agent data.

        Update the TargetDataPoints with DataPoints

        Args:
            None

        Returns:
            ddv_list: List of type TargetDataPoints

        """
        # Initialize key variables
        ddv_list = []

        # Poll all targets in sequence
        for item in self._target_poll_targets:
            result = self._get_target_datapoints(item)
            if result.valid is True:
                ddv_list.append(result)

        # Return
        return ddv_list

    def _get_target_datapoints(self, item):
        """Poll each spoke in parallel.

        Args:
            item: TargetPollingPoints object

        Returns:
            ddv: TargetDataPoints for the SNMPVariable target

        """
        # Intialize data gathering
        ip_target = item.target
        ddv = TargetDataPoints(ip_target)

        # BAC0 only works with IP addresses
        ip_address = network.get_ipaddress(ip_target)
        if bool(ip_address) is False:
            return ddv

        # Get list of type DataPoint
        datapoints = []
        for polltarget in item.data:
            # Get polling results
            value = poll_target_address(
                ip_address, polltarget.address, 'presentValue', self._bacnet)
            name = poll_target_address(
                ip_address, polltarget.address, 'objectName', self._bacnet)

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
                'analog_value_point_{}'.format(polltarget.address),
                value,
                data_type=data_type)
            datapoint.add(
                DataPointMetadata('target', ip_target))
            if name is not None:
                datapoint.add(DataPointMetadata('object_name', name))
            datapoints.append(datapoint)

        # Return
        ddv.add(datapoints)
        return ddv


def poll_target_address(ip_target, address, object2poll, bacnet):
    """Poll each spoke in parallel.

    Args:
        ip_target: Target to poll
        polltargets: List of PollingPoint objects to poll
        bacnet: BAC0 connect object

    Returns:
        result: Result of the poll

    """
    # Intialize data gathering
    result = None
    poller_string = (
        '{} analogValue {} {}'.format(ip_target, address, object2poll))

    try:
        result = bacnet.read(poller_string)
    except NoResponseFromController:
        log_message = (
            'No BACnet response from {}. Timeout.'.format(ip_target))
        log.log2warning(51004, log_message)
    except UnknownObjectError:
        log_message = ('''\
Unknown BACnet object {} requested from target {} at address {}.\
'''.format(object2poll, ip_target, address))
        log.log2warning(51005, log_message)
    except Exception as reason:
        log_message = ('BACnet error polling {}. Reason: {}'.format(
            ip_target, str(reason)))
        log.log2warning(51006, log_message)
    except:
        log_message = ('''Unknown BACnet error polling {}: [{}, {}, {}]\
'''.format(ip_target, sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
        log.log2warning(51007, log_message)

    # Return
    return result
