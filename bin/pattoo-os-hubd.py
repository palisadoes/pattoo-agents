#!/usr/bin/env python3
"""Pattoo reporter daemon.

Posts system data to remote host over HTTP.

"""

# Standard libraries
from time import sleep
import sys
import os
import multiprocessing

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
from pattoo.os.pattoo import PATTOO_OS_HUBD, PATTOO_OS_SPOKED_API_PREFIX
from pattoo.shared import agent
from pattoo.os import get_post
from pattoo.os import configuration


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
        self._agent_program_pattoo_os = PATTOO_OS_HUBD

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
        config = configuration.ConfigHubd()
        interval = config.polling_interval()

        # Post data to the remote server
        while True:
            _parallel_poll()

            # Sleep
            sleep(interval)


def _parallel_poll():
    """Poll each spoke in parallel.

    Args:
        None

    Returns:
        none: result

    """
    # Initialize key variables
    sub_processes_in_pool = max(1, multiprocessing.cpu_count())
    config = configuration.ConfigHubd()
    ip_devices = config.ip_devices()
    argument_list = []

    # Create tuple list of parameters
    for ip_device in ip_devices:
        # Test
        if isinstance(ip_device, dict) is False:
            continue
        if 'ip_address' not in ip_device:
            continue
        if 'ip_bind_port' not in ip_device:
            continue

        # Append argument
        argument_list.append(
            (ip_device['ip_address'], ip_device['ip_bind_port'])
        )

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        pool.starmap(get_post.poll, argument_list)

    # Wait for all the processes to end
    pool.join()


def main():
    """Start the pattoo agent.

    Args:
        None

    Returns:
        None

    """
    # Poll
    agent_poller = PollingAgent(PATTOO_OS_HUBD)

    # Do control
    cli = agent.AgentCLI()
    cli.control(agent_poller)


if __name__ == "__main__":
    main()
