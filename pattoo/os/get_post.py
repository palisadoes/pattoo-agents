#!/usr/bin/env python3
"""Pattoo get library."""

# Pattoo libraries
from pattoo.os.pattoo import PATTOO_OS_SPOKED_API_PREFIX
from pattoo.shared import post
from pattoo.shared import get


def spoked_url(ip_device, bind_port):
    """Poll a spoke.

    Args:
        ip_device: IP device to poll for data
        bind_port: TCP listening port

    Returns:
        url: URL of spoke

    """
    # Initialize key variables
    hostname = ip_device
    if ':' in ip_device:
        hostname = '[{}]'.format(hostname)

    # Return
    url = 'http://{}:{}{}'.format(
        ip_device, bind_port, PATTOO_OS_SPOKED_API_PREFIX)
    return url


def poll(ip_device, bind_port):
    """Poll a spoke.

    Args:
        ip_device: IP device to poll for data

    Returns:
        none: result

    """
    # Get data
    url = spoked_url(ip_device, bind_port)
    data_dict = get.get_url_json(url)

    # Post data
    if bool(data_dict) is True:
        # Post to remote server
        server = post.Data(data_dict)

        # Post data
        success = server.post()

        # Purge cache if success is True
        if success is True:
            server.purge()
