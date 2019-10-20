#!/usr/bin/env python3
"""Pattoo Agent class.

Description:

    This script:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import os
import json

# pip3 libraries
import requests

# Pattoo libraries
from pattoo_shared import log
from pattoo_shared import configuration
from pattoo_shared import data as lib_data
from .converter import ConvertAgentPolledData


class Post(object):
    """Class to prepare data for posting."""

    def __init__(self, agentdata):
        """Initialize the class.

        Args:
            agentdata: AgentPolledData object of data polled by agent

        Returns:
            None

        """
        # Initialize key variables
        config = configuration.Config()
        self._agentdata = agentdata

        # Get posting URL
        self._url = config.api_server_url(agentdata.agent_id)

        # Get the agent cache directory
        self._cache_dir = config.agent_cache_directory(
            self._agentdata.agent_program)

        # All cache files created by this agent will end with this suffix.
        devicehash = lib_data.hashstring(agentdata.agent_hostname, sha=1)
        self._cache_filename_suffix = '{}_{}.json'.format(
            agentdata.agent_id, devicehash)

    def post(self, save=True, data=None):
        """Post data to central server.

        Args:
            save: When True, save data to cache directory if postinf fails
            data: Data to post. If None, then uses self._post_data (
                Used for testing and cache purging)

        Returns:
            success: True: if successful

        """
        # Initialize key variables
        success = False
        response = False
        timestamp = self._agentdata.timestamp

        # Create data to post
        if data is None:
            if self._agentdata.active is True:
                process = ConvertAgentPolledData(self._agentdata)
                data2post = process.data()
            else:
                # Invalid data. Return False
                log_message = (
                    'Agent data invalid agent_id "{}". Will not post.'
                    ''.format(self._agentdata.agent_id))
                log.log2info(1028, log_message)
                success = False
                return success
        else:
            data2post = data

        # Post data save to cache if this fails
        try:
            result = requests.post(self._url, json=data2post)
            response = True
        except:
            if save is True:
                # Create a unique very long filename to reduce risk of
                filename = '{}/{}_{}'.format(
                    self._cache_dir, timestamp, self._cache_filename_suffix)

                # Save data
                with open(filename, 'w') as f_handle:
                    json.dump(data2post, f_handle)
            else:
                # Proceed normally if there is a failure.
                # This will be logged later
                pass

        # Define success
        if response is True:
            if result.status_code == 200:
                success = True

        # Log message
        if success is True:
            log_message = (
                'Agent "{}" successfully contacted server {}'
                ''.format(self._agentdata.agent_program, self._url))
            log.log2info(1027, log_message)
        else:
            log_message = (
                'Agent "{}" failed to contact server {}'
                ''.format(self._agentdata.agent_program, self._url))
            log.log2warning(1028, log_message)

        # Return
        return success

    def purge(self):
        """Purge data from cache by posting to central server.

        Args:
            None

        Returns:
            success: "True: if successful

        """
        # Initialize key variables
        agent_id = self._agentdata.agent_id

        # Add files in cache directory to list only if they match the
        # cache suffix
        all_filenames = [filename for filename in os.listdir(
            self._cache_dir) if os.path.isfile(
                os.path.join(self._cache_dir, filename))]
        filenames = [
            filename for filename in all_filenames if filename.endswith(
                self._cache_filename_suffix)]

        # Read cache file
        for filename in filenames:
            # Only post files for our own UID value
            if agent_id not in filename:
                continue

            # Get the full filepath for the cache file and post
            filepath = os.path.join(self._cache_dir, filename)
            with open(filepath, 'r') as f_handle:
                try:
                    data = json.load(f_handle)
                except:
                    # Log removal
                    log_message = (
                        'Error reading previously cached agent data file {} '
                        'for agent {}. May be corrupted.'
                        ''.format(filepath, self._agentdata.agent_program))
                    log.log2die(1064, log_message)

            # Post file
            success = self.post(save=False, data=data)

            # Delete file if successful
            if success is True:
                os.remove(filepath)

                # Log removal
                log_message = (
                    'Purging cache file {} after successfully '
                    'contacting server {}'
                    ''.format(filepath, self._url))
                log.log2info(1007, log_message)
