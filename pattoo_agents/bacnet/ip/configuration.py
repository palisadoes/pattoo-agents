#!/usr/bin/env python3
"""Classe to manage SNMP agent configurations."""

# Import project libraries
from pattoo_shared import configuration, files
from pattoo_shared.variables import IPTargetPollingPoints
from .constants import PATTOO_AGENT_BACNETIPD


class ConfigBACnetIP(object):
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Get the configuration directory
        config_file = configuration.agent_config_filename(
            PATTOO_AGENT_BACNETIPD)
        self._configuration = files.read_yaml_file(config_file)

    def agent_ip_address(self):
        """Get list polling target information in configuration file..

        Args:
            None

        Returns:
            result: IP address

        """
        # Initialize key variables
        result = []

        # Get configuration snippet
        key = PATTOO_AGENT_BACNETIPD
        sub_key = 'agent_ip_address'
        result = configuration.search(
            key, sub_key, self._configuration, die=True)
        return result

    def target_polling_points(self):
        """Get list polling target information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of IPTargetPollingPoints objects

        """
        # Initialize key variables
        result = []
        datapoint_key = 'points'

        # Get configuration snippet
        key = PATTOO_AGENT_BACNETIPD
        sub_key = 'polling_groups'
        groups = configuration.search(
            key, sub_key, self._configuration, die=True)

        # Create snmp objects
        for group in groups:
            # Ignore bad values
            if isinstance(group, dict) is False:
                continue

            # Process data
            if 'ip_targets' and datapoint_key in group:
                for ip_target in group['ip_targets']:
                    poll_targets = configuration.get_polling_points(
                        group[datapoint_key])
                    dpt = IPTargetPollingPoints(ip_target)
                    dpt.add(poll_targets)
                    if dpt.valid is True:
                        result.append(dpt)
        return result

    def polling_interval(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_BACNETIPD
        sub_key = 'polling_interval'
        intermediate = configuration.search(
            key, sub_key, self._configuration, die=False)

        # Default to 300
        if bool(intermediate) is False:
            result = 300
        else:
            result = abs(int(intermediate))
        return result
