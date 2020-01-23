"""Module that defines constants shared between agents."""

import collections

# pattoo-snmp constants
PATTOO_AGENT_OPCUAD = 'pattoo_agent_opcuad'

# Define namedtuple type
OPCUAauth = collections.namedtuple(
    'OPCUAauth', 'ip_target ip_port username password')
