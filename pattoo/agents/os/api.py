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
    # Initialize key variables
    agent_program = PATTOO_OS_SPOKED

    # Process and present
    dv_list = collector.poll()
    process = data.Data(agent_program, dv_list)
    data_dict = process.data()
    return jsonify(data_dict)
