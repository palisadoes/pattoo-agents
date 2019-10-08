#!/usr/bin/env python3
"""Pattoo reporter daemon.

Posts system data to remote host over HTTP.

"""

# Standard libraries
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
from pattoo.os.pattoo import PATTOO_OS_AUTONOMOUSD
from pattoo.os import data
from pattoo.shared import agent
from pattoo.shared import log
from pattoo.shared import post
from pattoo.shared import configuration


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

        # Initialize key variables
        self._agent_program_pattoo_os = PATTOO_OS_AUTONOMOUSD

    def name(self):
        """Return agent name.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self._agent_program_pattoo_os
        return value

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

        # Post data to the remote server
        while True:
            self.upload()

            # Sleep
            sleep(interval)

    def upload(self):
        """Post system data to the central server.

        Args:
            None

        Returns:
            None

        """
        # Get system data
        data_dict = data.poll(self._agent_program_pattoo_os)

        # Post to remote server
        server = post.Data(data_dict)

        # Post data
        success = server.post()

        # Purge cache if success is True
        if success is True:
            server.purge()


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
