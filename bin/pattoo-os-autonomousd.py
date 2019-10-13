#!/usr/bin/env python3
"""Pattoo reporter daemon.

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
from pattoo.constants import PATTOO_OS_AUTONOMOUSD
from pattoo.agents.os import collector
from pattoo import agent
from pattoo import post
from pattoo import configuration


class PollingAgent(agent.Agent):
    """Agent that gathers data."""

    def __init__(self, parent):
        """Initialize the class.

        Args:
            config_dir: Configuration directory

        Returns:
            None

        """
        # Initialize key variables
        agent.Agent.__init__(self, parent)
        self._parent = parent

    def query(self):
        """Query all remote devices for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        config = configuration.Config()
        interval = config.polling_interval()
        agent_program = self._parent

        # Post data to the remote server
        while True:

            # Get system data
            dv_list = collector.poll()

            # Post to remote server
            server = post.Post(agent_program, dv_list)

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
    agent_poller = PollingAgent(PATTOO_OS_AUTONOMOUSD)

    # Do control
    cli = agent.AgentCLI()
    cli.control(agent_poller)


if __name__ == "__main__":
    main()
