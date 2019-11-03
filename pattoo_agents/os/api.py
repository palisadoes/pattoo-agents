#!/usr/bin/env python3
"""This is a test of flask."""

# Pip packages
from flask import Flask, jsonify

# Pattoo imports
from pattoo_agents.os import collector
from pattoo_shared.constants import (
    PATTOO_AGENT_OS_SPOKED_API_PREFIX, PATTOO_AGENT_OS_SPOKED)
from pattoo_shared.converter import ConvertAgentPolledData


# Define flask parameters
API = Flask(__name__)


@API.route(PATTOO_AGENT_OS_SPOKED_API_PREFIX)
def home():
    """Display api data on home page.

    Args:
        None

    Returns:
        None

    """
    # Process and present
    agentdata = collector.poll(PATTOO_AGENT_OS_SPOKED)
    process = ConvertAgentPolledData(agentdata)
    data_dict = process.data()
    return jsonify(data_dict)
