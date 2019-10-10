"""Initialize global variables for pattoo-os daemons."""

# Create global variables for the API
PATTOO_OS_SPOKED_API_PREFIX = '/pattoo-os'
PATTOO_OS_SPOKED = 'pattoo-os-spoked'
PATTOO_OS_SPOKED_PROXY = '{}-gunicorn'.format(PATTOO_OS_SPOKED)
PATTOO_OS_AUTONOMOUSD = 'pattoo-os-autonomousd'
PATTOO_OS_HUBD = 'pattoo-os-hubd'
