#!/usr/bin/env python3
"""Pattoo helper for the Linux _data.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
from collections import defaultdict
import hashlib
from copy import deepcopy


# Pattoo libraries
from pattoo import files
from pattoo.variables import DataVariable, DataVariablesHost, AgentPolledData
from pattoo.constants import (
    DATA_FLOAT, DATA_INT, DATA_COUNT64, DATA_COUNT, DATA_STRING)


class Data(object):
    """Pattoo agent that gathers data."""

    def __init__(self, agentdata):
        """Initialize the class.

        Args:
            agentdata: AgentPolledData object of data polled by agent

        Returns:
            None

        """
        # Initialize key variables
        self._data = defaultdict(lambda: defaultdict(dict))
        self._list_of_dv_host = agentdata.data
        self._data['timestamp'] = agentdata.timestamp
        self._data['agent_id'] = agentdata.agent_id
        self._data['agent_program'] = agentdata.agent_program
        self._data['agent_hostname'] = agentdata.agent_hostname
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
        for dv_host in self._list_of_dv_host:
            # Initialize variable for code simplicity
            device = dv_host.device

            # Pre-populate the result with empty dicts
            result[device] = {}

            # Analyze each DataVariable for the dv_host
            for _dvar in dv_host.data:
                # Add keys if not already there
                if _dvar.data_label not in result[device]:
                    result[device][_dvar.data_label] = {}

                # Assign data values to result
                data_tuple = (_dvar.data_index, _dvar.value)
                if 'data' in result[device][_dvar.data_label]:
                    result[device][_dvar.data_label][
                        'data'].append(data_tuple)
                else:
                    result[device][_dvar.data_label][
                        'data_type'] = _dvar.data_type
                    result[device][_dvar.data_label][
                        'data'] = [data_tuple]

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


def converter(data=None, filepath=None):
    """Convert agent cache data to AgentPolledData object.

    Args:
        data: Agent data dict
        filename: Name of file with Agent data dict

    Returns:
        agentdata: AgentPolledData object

    """
    # Initialize key variables
    agent_id = None
    agent_program = None
    agent_hostname = None
    timestamp = None

    # Get data
    if bool(filepath) is True:
        _data = files.read_json_file(filepath, die=True)
    else:
        _data = data

    # Get values to instantiate an AgentPolledData object
    (agent_id, agent_program, agent_hostname,
     timestamp, polled_data, agent_valid) = _valid_agent(_data)
    if agent_valid is False:
        return None
    agentdata = AgentPolledData(
        agent_id, agent_program, agent_hostname, timestamp)

    # Iterate through devices polled by the agent
    for device, devicedata in sorted(polled_data.items()):
        # Create DataVariablesHost
        dv_host = _datavariablelist(device, devicedata)

        # Append the DataVariablesHost to the AgentPolledData object
        if dv_host.active is True:
            agentdata.append(dv_host)

    # Return
    if agentdata.active is False:
        return None
    else:
        return agentdata


def _valid_agent(_data):
    """Determine the validity of the Agent's data.

    Args:
        _data: Agent data dict

    Returns:
        result: Tuple of (
            agent_id, agent_program, agent_hostname,
            timestamp, polled_data, agent_valid)

    """
    # Initialize key variables
    agent_id = None
    agent_program = None
    agent_hostname = None
    timestamp = None
    polled_data = None
    agent_valid = False

    # Verify values
    if isinstance(_data, dict) is True:
        if 'agent_id' in _data:
            agent_id = _data['agent_id']
        if 'agent_program' in _data:
            agent_program = _data['agent_program']
        if 'agent_program' in _data:
            agent_hostname = _data['agent_hostname']
        if 'timestamp' in _data:
            if isinstance(_data['timestamp'], int) is True:
                timestamp = _data['timestamp']
        if 'devices' in _data:
            if isinstance(_data['devices'], dict) is True:
                polled_data = deepcopy(_data['devices'])

    # Determine validity
    agent_valid = False not in [
        bool(agent_id), bool(agent_program),
        bool(agent_hostname), bool(timestamp),
        bool(polled_data)]

    # Return
    result = (
        agent_id, agent_program, agent_hostname,
        timestamp, polled_data, agent_valid)
    return result


def _datavariablelist(device, devicedata):
    """Create a DataVariablesHost object from Agent data.

    Args:
        device: Device polled by agent
        devicedata: Data polled from device by agent

    Returns:
        datavariablelist: DataVariablesHost object

    """
    # Initialize key variables
    dv_host = DataVariablesHost(device)

    # Ignore invalid data
    if isinstance(devicedata, dict) is True:
        # Iterate through the data_labels in the dict
        for data_label, data4label in sorted(devicedata.items()):
            # Ignore invalid data
            if isinstance(data4label, dict) is False:
                continue

            # Validate the presence of required keys, then process
            if 'data' and 'data_type' in data4label:
                # Skip invalid types
                if data4label['data_type'] not in [
                        DATA_FLOAT, DATA_INT, DATA_COUNT64, DATA_COUNT,
                        DATA_STRING]:
                    continue
                if isinstance(data4label['data'], list) is False:
                    continue

                # Add to the DataVariablesHost
                datavariables = _datavariables(data_label, data4label)
                dv_host.extend(datavariables)

    # Return
    return dv_host


def _datavariables(data_label, data4label):
    """Create a valid list of DataVariables for a specific label.

    Args:
        data_label: Label for data
        data4label: Dict of data represented by the data_label

    Returns:
        datavariables: List of DataVariable objects

    """
    # Initialize key variables
    datavariables = []
    data_type = data4label['data_type']

    # Add the data to the DataVariablesHost
    for item in data4label['data']:
        if isinstance(item, list) is True:
            if len(item) == 2:
                data_index = item[0]
                value = item[1]

                # Skip invalid numerical data
                if data_type is not DATA_STRING:
                    try:
                        float(value)
                    except:
                        continue

                # Update DataVariable with valid data
                datavariable = DataVariable(
                    value=value,
                    data_label=data_label,
                    data_index=data_index,
                    data_type=data4label['data_type'])
                datavariables.append(datavariable)

    # Return
    return datavariables
