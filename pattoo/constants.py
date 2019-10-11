"""Module that defines universal constants.

The aim is to have a single location for constants that may be used across
agents to prevent the risk of duplication.

"""

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
