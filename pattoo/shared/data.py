#!/usr/bin/env python3
"""Pattoo helper for the Linux _data.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
from collections import defaultdict
from copy import deepcopy
import socket

# Pattoo libraries
from pattoo.os import language
from pattoo.shared import log
from pattoo.shared import general
from pattoo.shared import daemon
from pattoo.shared import agent as agent_lib


class Data(object):
    """Pattoo agent that gathers data."""

    def __init__(self, agent_program):
        """Initialize the class.

        Args:
            agent_program: Name of agent program

        Returns:
            None

        """
        # Initialize key variables
        self._data = defaultdict(lambda: defaultdict(dict))
        agent_id = agent_lib.get_agent_id(agent_program)
        self._lang = language.Agent(agent_program)

        # Get devicename
        self._devicename = socket.getfqdn()

        # Add timestamp
        self._data['timestamp'] = general.normalized_timestamp()
        self._data['agent_id'] = agent_id
        self._data['agent_program'] = agent_program
        self._data['agent_hostname'] = self._devicename
        self._data['devices'] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict())))

    def name(self):
        """Return the name of the _data.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self._data['agent_program']
        return value

    def populate(self, data_in):
        """Populate data for agent to eventually send to server.

        Args:
            data_in: dict of datapoint values from agent
            timeseries: TimeSeries data if True

        Returns:
            None

        """
        # Initialize data
        data = deepcopy(data_in)

        # Validate base_type
        if len(data) != 1 or isinstance(data, defaultdict) is False:
            log_message = 'Agent data "{}" is invalid'.format(data)
            log.log2die(1025, log_message)

        # Get a description to use for label value
        for label in data.keys():
            description = self._lang.label_description(label)
            data[label]['description'] = description
            break

        # Add data to appropriate self._data key
        if data[label]['base_type'] is not None:
            self._data['devices'][self._devicename]['timeseries'].update(data)
        else:
            self._data['devices'][self._devicename]['timefixed'].update(data)

    def populate_single(self, label, value, base_type=None, source=None):
        """Populate a single value in the _data.

        Args:
            label: Agent label for data
            value: Value of data
            source: Source of the data
            base_type: Base type of data

        Returns:
            None

        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        data[label]['base_type'] = base_type
        data[label]['data'] = [[source, value]]

        # Update
        self.populate(data)

    def populate_named_tuple(self, prefix, named_tuple, base_type=1):
        """Post system data to the central server.

        Args:
            prefix: Prefix to append to data keys when populating the agent
            named_tuple: Named tuple with data values
            base_type: SNMP style base_type (integer, counter32, etc.)

        Returns:
            None

        """
        # Get data
        system_dict = named_tuple._asdict()
        return_data = defaultdict(lambda: defaultdict(dict))
        data = []

        # Do nothing if there is no prefix
        if bool(prefix) is False:
            return

        # Cycle through results
        for label, value in system_dict.items():
            # Convert the dict to list of lists [label][value]
            data.append([label, value])

        # Add data
        return_data[prefix]['data'] = data
        return_data[prefix]['base_type'] = base_type

        # Update
        self.populate(return_data)

    def populate_dict(self, prefix, data_in, base_type=1):
        """Populate agent with data that's a dict keyed by [label][source].

        Args:
            prefix: Prefix to append to data keys when populating the agent
            data_in: Dict of data to post "X[label][source] = value"
            base_type: SNMP style base_type (integer, counter32, etc.)

        Returns:
            None

        """
        # Initialize data
        data_input = deepcopy(data_in)

        # Iterate over labels
        for label in data_input.keys():
            # Initialize tuple list to use by _data.populate
            value_sources = []
            new_label = '{}_{}'.format(prefix, label)

            # Initialize data
            data = defaultdict(lambda: defaultdict(dict))
            data[new_label]['base_type'] = base_type

            # Append to tuple list
            # (Sorting is important to keep consistent ordering)
            for source, value in sorted(data_input[label].items()):
                value_sources.append(
                    [source, value]
                )
            data[new_label]['data'] = value_sources

            # Update
            self.populate(data)

    def data(self):
        """Return that that should be posted.

        Args:
            None

        Returns:
            None

        """
        # Return
        return self._data
