#!/usr/bin/env python3
"""Pattoo get library."""

# Pattoo libraries
from pattooagents.constants import PATTOO_OS_SPOKED_API_PREFIX
from pattooagents import post
from pattooagents import get
from pattooagents import data


def spoked_url(ip_device, ip_bind_port):
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
        ip_device, ip_bind_port, PATTOO_OS_SPOKED_API_PREFIX)
    return url


def relay(ip_device, ip_bind_port):
    """Poll a spoke.

    Args:
        ip_device: IP device to poll for data

    Returns:
        none: result

    """
    # Get data
    url = spoked_url(ip_device, ip_bind_port)
    data_dict = get.get_url_json(url)

    # Post data
    if bool(data_dict) is True:
        # Post to remote server
        agentdata = data.converter(data=data_dict)
        server = post.Post(agentdata)
        success = server.post()

        # Purge cache if success is True
        if success is True:
            server.purge()
