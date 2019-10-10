#!/usr/bin/env python3
"""Pattoo helper for the Linux _data.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
from collections import defaultdict
import socket
import hashlib


# Pattoo libraries
from pattoo.agents.os import language
from pattoo import times
from pattoo import agent as agent_lib
from pattoo.variables import DataVariable, DATA_INT, DATA_STRING


class Data(object):
    """Pattoo agent that gathers data."""

    def __init__(self, agent_program, polled_objects):
        """Initialize the class.

        Args:
            agent_program: Name of agent program
            polled_objects: One or more DataVariableList objects

        Returns:
            None

        """
        # Initialize key variables
        self._data = defaultdict(lambda: defaultdict(dict))
        agent_id = agent_lib.get_agent_id(agent_program)

        # Convert the polled objects for processing
        if isinstance(polled_objects, list) is True:
            self._polled_objects = polled_objects
        else:
            self._polled_objects = [polled_objects]

        # Get devicename
        self._devicename = socket.getfqdn()

        # Add timestamp
        self._data['timestamp'] = times.normalized_timestamp()
        self._data['agent_id'] = agent_id
        self._data['agent_program'] = agent_program
        self._data['agent_hostname'] = self._devicename
        self._data['devices'] = self._process()

    def _process(self):
        """Return the name of the _data.

        Args:
            None

        Returns:
            result: Data required

        """
        # Intitialize key variables
        # Yes we could have used Lambdas but pprint wouldn't fit on the screen
        result = {}

        # Get information from data
        for polled_device in self._polled_objects:
            # Initialize variable for code simplicity
            device = polled_device.device

            # Pre-populate the result with empty dicts
            result[device] = {}
            result[device]['timefixed'] = {}
            result[device]['timestamp'] = {}

            # Analyze each DataVariable for the polled_device
            for _dvar in polled_device.data:
                # Determine the type of data
                if _dvar.data_type == DATA_STRING:
                    key = 'timefixed'
                else:
                    key = 'timestamp'

                # Add keys if not already there
                if _dvar.data_label not in result[device][key]:
                    result[device][key][_dvar.data_label] = {}

                # Assign data values to result
                data_tuple = (_dvar.data_index, _dvar.value)
                if 'data' in result[device][key][_dvar.data_label]:
                    result[device][
                        key][_dvar.data_label]['data'].append(data_tuple)
                else:
                    result[device][
                        key][_dvar.data_label]['base_type'] = _dvar.data_type
                    result[device][
                        key][_dvar.data_label]['data'] = [data_tuple]

                    # Get a description to use for label value
                    if _dvar.data_label in polled_device.translations:
                        result[device][key][_dvar.data_label][
                            'description'] = polled_device.translations[
                                _dvar.data_label]
        # Return
        return result

    def data(self):
        """Return that that should be posted.

        Args:
            None

        Returns:
            None

        """
        # Return
        return self._data


def encode(value):
    """Encode string value to utf-8.

    Args:
        value: String to encode

    Returns:
        result: encoded value

    """
    # Initialize key variables
    result = value

    # Start decode
    if value is not None:
        if isinstance(value, str) is True:
            result = value.encode()

    # Return
    return result


def decode(value):
    """Decode utf-8 value to string.

    Args:
        value: String to decode

    Returns:
        result: decoded value

    """
    # Initialize key variables
    result = value

    # Start decode
    if value is not None:
        if isinstance(value, bytes) is True:
            result = value.decode('utf-8')

    # Return
    return result


def hashstring(string, sha=256, utf8=False):
    """Create a UTF encoded SHA hash string.

    Args:
        string: String to hash
        length: Length of SHA hash
        utf8: Return utf8 encoded string if true

    Returns:
        result: Result of hash

    """
    # Initialize key variables
    listing = [1, 224, 384, 256, 512]

    # Select SHA type
    if sha in listing:
        index = listing.index(sha)
        if listing[index] == 1:
            hasher = hashlib.sha1()
        elif listing[index] == 224:
            hasher = hashlib.sha224()
        elif listing[index] == 384:
            hasher = hashlib.sha512()
        elif listing[index] == 512:
            hasher = hashlib.sha512()
        else:
            hasher = hashlib.sha256()

    # Encode the string
    hasher.update(bytes(string.encode()))
    device_hash = hasher.hexdigest()
    if utf8 is True:
        result = device_hash.encode()
    else:
        result = device_hash

    # Return
    return result


def is_numeric(val):
    """Check if argument is a number.

    Args:
        val: String to check

    Returns:
        True if a number

    """
    # Try edge case
    if val is True:
        return False
    if val is False:
        return False

    # Try conversions
    try:
        float(val)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
    except:
        return False


def named_tuple_to_dv(
        values, data_label=None, data_type=DATA_INT):
    """Convert a named tuple to a list of DataVariable objects.

    Args:
        values: Named tuple
        data_label: data_label
        data_type: Data type

    Returns:
        result: List of DataVariable

    """
    # Get data
    data_dict = values._asdict()
    result = []

    # Cycle through results
    for data_index, value in data_dict.items():
        _dv = DataVariable(
            value=value,
            data_label=data_label,
            data_index=data_index,
            data_type=data_type)
        result.append(_dv)

    # Return
    return result
