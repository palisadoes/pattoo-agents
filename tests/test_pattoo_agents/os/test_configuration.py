#!/usr/bin/env python3
"""Test the class_oid module."""

import sys
import unittest
import os

# Try to create a working PYTHONPATH
EXEC_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIRECTORY, os.pardir)), os.pardir)), os.pardir))
if EXEC_DIRECTORY.endswith(
        '/pattoo-agents/tests/test_pattoo_agents/os') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print('''\
This script is not installed in the \
"pattoo-agents/tests/test_pattoo_agents/os" \
directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_agents.agents.os import configuration
from tests.libraries.configuration import UnittestConfig


class TestConfigSpoked(unittest.TestCase):
    """Checks all ConfigSpoked methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################
    config = configuration.ConfigSpoked()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_listen_address(self):
        """Testing function listen_address."""
        # Initialize key values
        expected = '127.0.0.1'

        # Test
        result = self.config.listen_address()
        self.assertEqual(result, expected)

    def test_ip_bind_port(self):
        """Testing function ip_bind_port."""
        # Initialize key values
        expected = 5000

        # Test
        result = self.config.ip_bind_port()
        self.assertEqual(result, expected)


class TestConfigHubd(unittest.TestCase):
    """Checks all ConfigHubd methods."""

    ##########################################################################
    # Initialize variable class.
    ##########################################################################
    config = configuration.ConfigHubd()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_ip_devices(self):
        """Testing function ip_devices."""
        # Test
        result = self.config.ip_devices()
        self.assertEqual(isinstance(result, list), True)
        self.assertEqual(len(result), 1)
        for item in result:
            self.assertEqual(isinstance(item, dict), True)
            self.assertEqual(len(item), 2)
            self.assertEqual('ip_address' in item, True)
            self.assertEqual('ip_bind_port' in item, True)
            self.assertEqual(item['ip_address'], '127.0.0.1')
            self.assertEqual(item['ip_bind_port'], 5000)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
