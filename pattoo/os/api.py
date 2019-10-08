#!/usr/bin/env python3
"""This is a test of flask."""

# Pip packages
from flask import Flask, jsonify

# Pattoo imports
from pattoo.os import data
from pattoo.os.pattoo import API_PREFIX, API_EXECUTABLE
from pattoo.os import configuration

# Define flask parameters
API = Flask(__name__)


@API.route(API_PREFIX)
def home():
    """Display api data on home page.

    Args:
        None

    Returns:
        None

    """
    # Return
    data_dict = data.poll(API_EXECUTABLE)
    return jsonify(data_dict)
