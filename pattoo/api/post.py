"""Pattoo. Posting Routes."""

# Standard imports
import os
import json

# Flask imports
from flask import Blueprint, request, abort

# Infoset-ng imports
from pattoo import files
from pattoo import configuration
from pattoo_shared import PATTOO_API_AGENT_PREFIX


# Define the POST global variable
POST = Blueprint('POST', __name__)


@POST.route('{}/receive/<agent_id>'.format(PATTOO_API_AGENT_PREFIX),
             methods=['POST'])
def receive(agent_id):
    """Function for handling the agent posting route.

    Args:
        agent_id: Unique Identifier of an pattoo agent

    Returns:
        Text response of Received

    """
    # Initialize key variables
    found_count = 0

    # Read configuration
    config = configuration.Config()
    cache_dir = CONFIG.cache_directory()

    # Get JSON from incoming agent POST
    try:
        data = request.json
    else:
        # Don't crash if we cannot convert JSON
        abort(404)

    # Abort if data isn't a dict
    if isinstance(data, dict) is False:
        abort(404)

    # Make sure all the important keys are available
    keys = ['timestamp', 'agent_id', 'agent_hostname']
    for key in keys:
        if key in data:
            found_count += 1

    # Do processing
    if found_count == 3:
        # Extract key values from posting
        try:
            timestamp = int(data['timestamp'])
        except:
            abort(404)
        agent_id = data['agent_id']
        agent_hostname = data['agent_hostname']

        # Create a hash of the agent_hostname
        device_hash = files.hashstring(agent_hostname, sha=1)
        json_path = (
            '{0}{4}{1}_{2}_{3}.json'.format(
                cache_dir, timestamp, agent_id, device_hash, os.sep))

        # Create cache file
        with open(json_path, "w+") as temp_file:
            json.dump(data, temp_file)

        # Return
        return 'OK'

    else:
        abort(404)
