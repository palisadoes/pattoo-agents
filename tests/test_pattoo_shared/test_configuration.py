#!/usr/bin/env python3
"""Test the files module."""

# Standard imports
import unittest
import os
import tempfile
import sys
import json
from math import pi
from random import randint
import shutil

# PIP imports
import yaml

# Try to create a working PYTHONPATH
EXEC_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIRECTORY, os.pardir)), os.pardir))
if EXEC_DIRECTORY.endswith('/pattoo-agents/tests/test_pattoo_shared') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print('''\
This script is not installed in the "pattoo-agents/tests/test_pattoo_shared" \
directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_shared import configuration
from tests.dev import unittest_setup


class TestConfig(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    config = configuration.Config()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_api_listen_address(self):
        """Testing function api_listen_address."""
        # Initialize key values
        expected = 6060

        # Test
        result = self.config.api_listen_address()
        self.assertEqual(result, expected)

    def test_polling_interval(self):
        """Testing function polling_interval."""
        # Initialize key values
        expected = 20

        # Test
        result = self.config.polling_interval()
        self.assertEqual(result, expected)

    def test_api_ip_address(self):
        """Testing function api_ip_address."""
        # Initialize key values
        expected = '127.0.0.1'

        # Test
        result = self.config.api_ip_address()
        self.assertEqual(result, expected)

    def test_api_ip_bind_port(self):
        """Testing function api_ip_bind_port."""
        # Initialize key values
        expected = 6060

        # Test
        result = self.config.api_ip_bind_port()
        self.assertEqual(result, expected)

    def test_api_uses_https(self):
        """Testing function api_uses_https."""
        # Initialize key values
        expected = False

        # Test
        result = self.config.api_uses_https()
        self.assertEqual(result, expected)

    def test_api_uri(self):
        """Testing function api_uri."""
        # Initialize key values
        expected = '/pattoo/agent/receive'

        # Test
        result = self.config.api_uri()
        self.assertEqual(result, expected)

    def test_api_server_url(self):
        """Testing function api_server_url."""
        # Initialize key values
        expected = '/pattoo/agent/receive'

        # Test
        result = self.config.api_server_url()
        self.assertEqual(result, expected)

    def test_log_directory(self):
        """Testing function log_directory."""
        pass

    def test_log_file(self):
        """Testing function log_file."""
        pass

    def test_log_file_api(self):
        """Testing function log_file_api."""
        pass

    def test_log_level(self):
        """Testing function log_level."""
        pass

    def test_cache_directory(self):
        """Testing function cache_directory."""
        pass

    def test_agent_cache_directory(self):
        """Testing function agent_cache_directory."""
        pass

    def test_search(self):
        """Testing function search."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
