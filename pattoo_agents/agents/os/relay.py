#!/usr/bin/env python3
"""Pattoo get library."""

# Pattoo libraries
from pattoo_agents import get
from pattoo_shared.post import Post
from pattoo_shared import converter
from pattoo_shared.constants import PATTOO_AGENT_OS_SPOKED_API_PREFIX


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
        ip_device, ip_bind_port, PATTOO_AGENT_OS_SPOKED_API_PREFIX)
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
        agentdata = converter.convert(data_dict)
        server = Post(agentdata)
        success = server.post()

        # Purge cache if success is True
        if success is True:
            server.purge()
