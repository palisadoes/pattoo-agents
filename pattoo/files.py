#!/usr/bin/env python3
"""Pattoo files library."""

import os
import sys
import yaml

# Pattoo libraries
from pattoo import log
import pattoo


def root_directory():
    """Determine the root directory in which pattoo is installed.

    Args:
        None

    Returns:
        root_dir: Root directory

    """
    # Get the directory of the pattoo library
    pattoo_dir = pattoo.__path__[0]
    components = pattoo_dir.split(os.sep)

    # Determine the directory two levels above
    root_dir = os.sep.join(components[0:-1])

    # Return
    return root_dir


def read_yaml_files(config_directory):
    """Read the contents of all yaml files in a directory.

    Args:
        config_directory: Directory with configuration files

    Returns:
        config_dict: Dict of yaml read

    """
    # Initialize key variables
    yaml_found = False
    yaml_from_file = ''
    all_yaml_read = ''

    if os.path.isdir(config_directory) is False:
        log_message = (
            'Configuration directory "{}" '
            'doesn\'t exist!'.format(config_directory))
        log.log2die(1009, log_message)

    # Cycle through list of files in directory
    for filename in os.listdir(config_directory):
        # Examine all the '.yaml' files in directory
        if filename.endswith('.yaml'):
            # YAML files found
            yaml_found = True

            # Read file and add to string
            file_path = '{}/{}'.format(config_directory, filename)
            try:
                with open(file_path, 'r') as file_handle:
                    yaml_from_file = file_handle.read()
            except:
                log_message = (
                    'Error reading file {}. Check permissions, '
                    'existence and file syntax.'
                    ''.format(file_path))
                log.log2die(1065, log_message)

            # Append yaml from file to all yaml previously read
            all_yaml_read = '{}\n{}'.format(all_yaml_read, yaml_from_file)

    # Verify YAML files found in directory. We cannot use logging as it
    # requires a logfile location from the configuration directory to work
    # properly
    if yaml_found is False:
        log_message = (
            'No configuration files found in directory "{}" with ".yaml" '
            'extension.'.format(config_directory))
        print(log_message)
        sys.exit(1)

    # Return
    config_dict = yaml.safe_load(all_yaml_read)
    return config_dict


def mkdir(directory):
    """Create a directory if it doesn't already exist.

    Args:
        directory: Directory name

    Returns:
        None

    """
    # Do work
    if os.path.exists(directory) is False:
        try:
            os.makedirs(directory, mode=0o775)
        except:
            log_message = (
                'Cannot create directory {}.'
                ''.format(directory))
            log.log2die(1090, log_message)

    # Fail if not a directory
    if os.path.isdir(directory) is False:
        log_message = (
            '{} is not a directory.'
            ''.format(directory))
        log.log2die(1043, log_message)
