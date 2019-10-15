#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import tempfile
import sys
from math import pi
from random import randint
import shutil

# PIP imports
import yaml

# Try to create a working PYTHONPATH
TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(TEST_DIRECTORY, os.pardir))
if TEST_DIRECTORY.endswith('/pattoo-agents/tests') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo-agents/tests" directory. '
        'Please fix.')
    sys.exit(2)

# Pattoo imports
from pattooagents import files
import pattooagents


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_root_directory(self):
        """Testing function root_directory."""
        # Determine root directory for pattoo
        pattoo_dir = pattoo.__path__[0]
        components = pattoo_dir.split(os.sep)

        # Determine root directory 2 levels above
        root_dir = os.sep.join(components[0:-1])
        result = files.root_directory()
        self.assertEqual(result, root_dir)

    def test_read_yaml_files(self):
        """Testing method / function read_yaml_files."""
        # Initializing key variables
        dict_1 = {
            'key1': 1,
            'key2': 2,
            'key3': 3,
            'key4': 4,
        }

        dict_2 = {
            'key6': 6,
            'key7': 7,
        }
        dict_3 = {}

        # Populate a third dictionary with contents of other dictionaries.
        for key, value in dict_1.items():
            dict_3[key] = value

        for key, value in dict_2.items():
            dict_3[key] = value

        # Create temp file with known data
        directory = tempfile.mkdtemp()
        filenames = {
            '{}/file_1.yaml'.format(directory): dict_1,
            '{}/file_2.yaml'.format(directory): dict_2
        }
        for filename, data_dict in filenames.items():
            with open(filename, 'w') as filehandle:
                yaml.dump(data_dict, filehandle, default_flow_style=False)

        # Get Results
        result = files.read_yaml_files(directory)

        # Clean up
        for key in result.keys():
            self.assertEqual(dict_3[key], result[key])
        filelist = [
            next_file for next_file in os.listdir(
                directory) if next_file.endswith('.yaml')]
        for delete_file in filelist:
            delete_path = '{}/{}'.format(directory, delete_file)
            os.remove(delete_path)
        os.removedirs(directory)

    def test_read_yaml_file(self):
        """Testing function read_yaml_file."""
        # Initializing key variables
        dict_1 = {
            'key1': 1,
            'key2': 2,
            'key3': 3,
            'key4': 4,
        }

        # Create temp file with known data
        directory = tempfile.mkdtemp()
        file_data = [
            (('{}/file_1.yaml').format(directory), dict_1)
        ]
        for item in file_data:
            filename = item[0]
            data_dict = item[1]
            with open(filename, 'w') as filehandle:
                yaml.dump(data_dict, filehandle, default_flow_style=False)

            # Get Results
            result = files.read_yaml_file(filename)

            # Test equivalence
            for key in result.keys():
                self.assertEqual(data_dict[key], result[key])

        # Clean up
        filelist = [
            next_file for next_file in os.listdir(
                directory) if next_file.endswith('.yaml')]
        for delete_file in filelist:
            delete_path = ('{}/{}').format(directory, delete_file)
            os.remove(delete_path)
        os.removedirs(directory)

    def test_mkdir(self):
        """Testing function mkdir."""
        # Test with file, not directory
        tmpfile = tempfile.NamedTemporaryFile(delete=False).name
        open(tmpfile, 'a').close()
        with self.assertRaises(SystemExit):
            files.mkdir(tmpfile)
        os.remove(tmpfile)

        # Create a sub directory of a temp directory.
        directory = '/tmp/pattoo-unittest/{}.fake'.format(
            randint(1, 10000) * pi)
        files.mkdir(directory)
        self.assertTrue(os.path.isdir(directory))
        shutil.rmtree(directory)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
