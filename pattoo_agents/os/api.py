#!/usr/bin/env python3
"""This is a test of flask."""

# Pip packages
from flask import Flask, jsonify

# Pattoo imports
from pattoo_agents.os import collector
from pattoo_shared import converter
from .constants import (
    PATTOO_AGENT_OS_SPOKED_API_PREFIX, PATTOO_AGENT_OS_SPOKED)


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
    datapoints = converter.agentdata_to_datapoints(agentdata)
    datapoint_dicts = converter.datapoints_to_dicts(datapoints)
    return jsonify(datapoint_dicts)
