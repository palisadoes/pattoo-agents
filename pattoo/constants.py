"""Module that defines universal constants.

The aim is to have a single location for constants that may be used across
agents to prevent the risk of duplication.

"""

###############################################################################
# Universal constants for all agents
###############################################################################

DATA_FLOAT = 1
DATA_INT = 0
DATA_COUNT64 = 64
DATA_COUNT = 32
DATA_STRING = 2
DATA_NONE = None

###############################################################################
# Constants for standard agents
###############################################################################

# pattoo-os constants
PATTOO_OS_SPOKED_API_PREFIX = '/pattoo-os'
PATTOO_OS_SPOKED = 'pattoo-os-spoked'
PATTOO_OS_SPOKED_PROXY = '{}-gunicorn'.format(PATTOO_OS_SPOKED)
PATTOO_OS_AUTONOMOUSD = 'pattoo-os-autonomousd'
PATTOO_OS_HUBD = 'pattoo-os-hubd'

# pattoo-snmp constants
PATTOO_SNMPD = 'pattoo-snmpd'
