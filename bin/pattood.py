#!/usr/bin/env python3
"""Infoset WSGI script.

Serves as a Gunicorn WSGI entry point for pattoo-api

"""

# Standard libraries
import sys
import os

# Try to create a working PYTHONPATH
_SYS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_BIN_DIRECTORY = os.path.abspath(os.path.join(_SYS_DIRECTORY, os.pardir))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_BIN_DIRECTORY, os.pardir))
if _SYS_DIRECTORY.endswith('/pattoo/bin/systemd') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Infoset libraries
from infoset.agents import agent
from infoset.agents.agent import Agent, AgentAPI
from infoset.constants import API_EXECUTABLE, API_GUNICORN_AGENT


def main():
    """Main function to start the Gunicorn WSGI."""
    # Get PID filenename for Gunicorn
    agent_gunicorn = Agent(API_GUNICORN_AGENT)

    # Get configuration
    agent_api = AgentAPI(API_EXECUTABLE, API_GUNICORN_AGENT)

    # Do control (API first, Gunicorn second)
    cli = agent.AgentCLI()
    cli.control(agent_api)
    cli.control(agent_gunicorn)


if __name__ == '__main__':
    main()
