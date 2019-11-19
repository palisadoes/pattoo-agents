#!/usr/bin/env python3
"""Pattoo SNMP daemon.

Posts system data to remote host over HTTP.

"""

# Standard libraries
from __future__ import print_function
from time import sleep
import sys
import os

# Try to create a working PYTHONPATH
_BIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _BIN_DIRECTORY.endswith('/pattoo-agents/bin') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo-agents/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Pattoo libraries
from pattoo_shared.configuration import Config
from pattoo_shared.phttp import PostAgent
from pattoo_shared.agent import Agent, AgentCLI
from pattoo_agents.snmp.default import collector
from pattoo_agents.snmp.constants import PATTOO_AGENT_SNMPD


class PollingAgent(Agent):
    """Agent that gathers data."""

    def __init__(self, parent):
        """Initialize the class.

        Args:
            config_dir: Configuration directory

        Returns:
            None

        """
        # Initialize key variables
        Agent.__init__(self, parent)

        # Initialize key variables
        self._agent_name_constant = PATTOO_AGENT_SNMPD

    def name(self):
        """Return agent name.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self._agent_name_constant
        return value

    def query(self):
        """Query all remote devices for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        config = Config()
        interval = config.polling_interval()

        # Post data to the remote server
        while True:
            # Get system data
            agentdata = collector.poll()

            # Post to remote server
            server = PostAgent(agentdata)

            # Post data
            success = server.post()

            # Purge cache if success is True
            if success is True:
                server.purge()

            # Sleep
            sleep(interval)


def main():
    """Start the pattoo agent.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    agent_poller = PollingAgent(PATTOO_AGENT_SNMPD)

    # Do control
    cli = AgentCLI()
    cli.control(agent_poller)


if __name__ == "__main__":
    main()
