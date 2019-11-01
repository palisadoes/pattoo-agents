#!/usr/bin/env python3
"""Pattoo multi-user operating system reporter daemon.

Retrieve's system data from remote host over HTTP.

"""

# Standard libraries
from __future__ import print_function
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
from pattoo_shared.constants import (
    PATTOO_AGENT_OS_HUBD, PATTOO_AGENT_OS_SPOKED_API_PREFIX)
from pattoo_shared.agent import Agent, AgentCLI
from pattoo_shared.phttp import PassiveAgent
from pattoo_agents.agents.os import configuration


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
        url = _spoked_url(ip_device['ip_address'], ip_device['ip_bind_port'])
        argument_list.append((url,))

    # Create a pool of sub process resources
    with multiprocessing.Pool(processes=sub_processes_in_pool) as pool:

        # Create sub processes from the pool
        pool.starmap(_relay, argument_list)

    # Wait for all the processes to end
    pool.join()


def _relay(url):
    """Relay data to pattoo server.

    Args:
        url: Pattoo spoked agent URL

    Returns:
        None

    """
    # Initialize key variables
    passive = PassiveAgent(url)
    passive.relay()

def _spoked_url(ip_device, ip_bind_port):
    """Poll a spoke.

    Args:
        ip_device: IP device to poll for data
        ip_bind_port: TCP listening port

    Returns:
        url: URL of spoke

    """
    # Initialize key variables
    hostname = ip_device
    if ':' in ip_device:
        hostname = '[{}]'.format(hostname)

    # Return
    url = 'http://{}:{}{}'.format(
        ip_device, ip_bind_port, PATTOO_AGENT_OS_SPOKED_API_PREFIX)
    return url


def main():
    """Start the pattoo agent.

    Args:
        None

    Returns:
        None

    """
    # Poll
    agent_poller = PollingAgent(PATTOO_AGENT_OS_HUBD)

    # Do control
    cli = AgentCLI()
    cli.control(agent_poller)


if __name__ == "__main__":
    main()
