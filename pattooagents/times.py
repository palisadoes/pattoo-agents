#!/usr/bin/env python3
"""Pattoo times library."""

import time

# Pattoo libraries
from pattooagents import configuration


def validate_timestamp(timestamp):
    """Validate timestamp to be a multiple of 'interval' seconds.

    Args:
        timestamp: epoch timestamp in seconds

    Returns:
        valid: True if valid

    """
    # Initialize key variables
    valid = False
    interval = configuration.Config().polling_interval()

    # Process data
    test = (int(timestamp) // interval) * interval
    if test == timestamp:
        valid = True

    # Return
    return valid


def normalized_timestamp(timestamp=None):
    """Normalize timestamp to a multiple of 'interval' seconds.

    Args:
        timestamp: epoch timestamp in seconds

    Returns:
        value: Normalized value

    """
    # Initialize key variables
    interval = configuration.Config().polling_interval()

    # Process data
    if timestamp is None:
        value = (int(time.time()) // interval) * interval
    else:
        value = (int(timestamp) // interval) * interval
    # Return
    return value
