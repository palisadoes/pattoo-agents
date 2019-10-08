"""Initialize global variables for pattoo-os daemons."""

# Create global variables for the API
API_PREFIX = '/pattoo-os'
API_EXECUTABLE = 'pattoo-os-passived'
API_GUNICORN_AGENT = '{}-gunicorn'.format(API_EXECUTABLE)
POLLER_EXECUTABLE = 'pattoo-os-actived'
