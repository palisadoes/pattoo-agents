#!/usr/bin/env python3
"""This is a test of flask."""

# Pip packages
from flask import Flask, jsonify

# Pattoo imports
from pattoo.os import data
from pattoo.os.pattoo import API_PREFIX, PATTOO_OS_SPOKED
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
    data_dict = data.poll(PATTOO_OS_SPOKED)
    return jsonify(data_dict)
