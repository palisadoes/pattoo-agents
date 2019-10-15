#!/usr/bin/env python3
"""This is a test of flask."""

# Pip packages
from flask import Flask, jsonify

# Pattoo imports
from pattoo.agents.os import collector
from pattoo.constants import PATTOO_OS_SPOKED_API_PREFIX, PATTOO_OS_SPOKED
from pattoo import data

# Define flask parameters
API = Flask(__name__)


@API.route(PATTOO_OS_SPOKED_API_PREFIX)
def home():
    """Display api data on home page.

    Args:
        None

    Returns:
        None

    """
    # Process and present
    agentdata = collector.poll(PATTOO_OS_SPOKED)
    process = data.Data(agentdata)
    data_dict = process.data()
    return jsonify(data_dict)
