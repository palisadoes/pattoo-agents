#!/usr/bin/env python3
"""Classe to manage OPCUA agent configurations."""


# Import project libraries
from pattoo_shared import configuration, files
from pattoo_shared.configuration import Config
from pattoo_shared.variables import TargetPollingPoints
from .constants import PATTOO_AGENT_OPCUAD, OPCUAauth


class ConfigOPCUA(Config):
    """Class gathers all configuration information."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Instantiate inheritance
        Config.__init__(self)

        # Get the configuration directory
        config_file = configuration.agent_config_filename(
            PATTOO_AGENT_OPCUAD)
        self._agent_config = files.read_yaml_file(config_file)

    def polling_interval(self):
        """Get targets.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = PATTOO_AGENT_OPCUAD
        sub_key = 'polling_interval'
        intermediate = configuration.search(
            key, sub_key, self._agent_config, die=False)

        # Default to 300
        if bool(intermediate) is False:
            result = 300
        else:
            result = abs(int(intermediate))
        return result

    def target_polling_points(self):
        """Get list polling target information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            result: List of TargetPollingPoints objects

        """
        # Initialize key variables
        result = []

        # Get configuration snippet
        key = PATTOO_AGENT_OPCUAD
        sub_key = 'polling_groups'
        groups = configuration.search(
            key, sub_key, self._agent_config, die=True)

        # Create snmp objects
        for group in groups:
            # Ignore bad values
            if isinstance(group, dict) is False:
                continue

            # Process data
            ip_target = group.get('ip_target')
            ip_port = group.get('ip_port')
            username = group.get('username')
            password = group.get('password')
            auth = OPCUAauth(
                ip_target=ip_target,
                ip_port=ip_port,
                username=username,
                password=password)
            nodes = group.get('nodes')
            poll_targets = configuration.get_polling_points(nodes)
            dpt = TargetPollingPoints(auth)
            dpt.add(poll_targets)
            if dpt.valid is True:
                result.append(dpt)
        return result
