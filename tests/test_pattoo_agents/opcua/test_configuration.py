#!/usr/bin/env python3
"""Test the class_oid module."""

import sys
import unittest
import os

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIR, os.pardir)), os.pardir)), os.pardir))
if EXEC_DIR.endswith(
        '/pattoo-agents/tests/test_pattoo_agents/opcua') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the \
"pattoo-agents/tests/test_pattoo_agents/opcua" directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_shared.variables import PollingPoint, TargetPollingPoints
from pattoo_agents.opcua import configuration
from pattoo_agents.opcua.constants import OPCUAauth
from tests.libraries.configuration import UnittestConfig


class TestConfigOPCUA(unittest.TestCase):
    """Checks all ConfigSpoked methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################
    config = configuration.ConfigOPCUA()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_polling_interval(self):
        """Test polling_interval."""
        # Initialize key values
        expected = 102

        # Test
        result = self.config.polling_interval()
        self.assertEqual(result, expected)

    def test_target_polling_points(self):
        """Testing function target_polling_points."""
        # Initialize key variables.
        result = self.config.target_polling_points()

        # Test
        self.assertEqual(isinstance(result, list), True)
        self.assertEqual(len(result), 1)

        # Test each dpt
        item = result[0]
        self.assertIsInstance(item, TargetPollingPoints)
        self.assertIsInstance(item.target, OPCUAauth)
        self.assertEqual(
            item.target, OPCUAauth(
                ip_target='unittest.opcua.tcp.target.net',
                ip_port=7844,
                username='nTbJazc6q3MaMazT',
                password='eQ6KnJcCk3qLkB73')
        )

        expected = [
            PollingPoint(address=1, multiplier=2),
            PollingPoint(address=3, multiplier=4)]
        for index, result in enumerate(item.data):
            self.assertEqual(result.address, expected[index].address)
            self.assertEqual(result.multiplier, expected[index].multiplier)

    def test_language(self):
        """Test pattoo_shared.Config inherited method language."""
        # Initialize key values
        expected = 'abc'

        # Test
        result = self.config.language()
        self.assertEqual(result, expected)

    def test_agent_api_ip_address(self):
        """Test pattoo_shared.Config inherited method agent_api_ip_address."""
        # Initialize key values
        expected = '127.0.0.11'

        # Test
        result = self.config.agent_api_ip_address()
        self.assertEqual(result, expected)

    def test_agent_api_ip_bind_port(self):
        """Test pattoo_shared.Config method agent_api_ip_bind_port."""
        # Initialize key values
        expected = 50001

        # Test
        result = self.config.agent_api_ip_bind_port()
        self.assertEqual(result, expected)

    def test_agent_api_uri(self):
        """Test pattoo_shared.Config inherited method api_uri."""
        # Initialize key values
        expected = '/pattoo/api/v1/agent/receive'

        # Test
        result = self.config.agent_api_uri()
        self.assertEqual(result, expected)

    def test_agent_api_server_url(self):
        """Test pattoo_shared.Config inherited method agent_api_server_url."""
        # Initialize key values
        expected = 'http://127.0.0.11:50001/pattoo/api/v1/agent/receive/123'
        agent_id = 123

        # Test
        result = self.config.agent_api_server_url(agent_id)
        self.assertEqual(result, expected)

    def test_web_api_ip_address(self):
        """Testing method / function web_api_ip_address."""
        # Test
        result = self.config.web_api_ip_address()
        self.assertEqual(result, '127.0.0.12')

    def test_web_api_ip_bind_port(self):
        """Testing method / function web_api_ip_bind_port."""
        # Test
        result = self.config.web_api_ip_bind_port()
        self.assertEqual(result, 50002)

    def test_web_api_server_url(self):
        """Testing method / function web_api_server_url."""
        # Test
        result = self.config.web_api_server_url()
        self.assertEqual(
            result, 'http://127.0.0.12:50002/pattoo/api/v1/web/graphql')

    def test_daemon_directory(self):
        """Test pattoo_shared.Config inherited method daemon_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.daemon_directory()

    def test_log_directory(self):
        """Test pattoo_shared.Config inherited method log_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.log_directory()

    def test_log_file(self):
        """Test pattoo_shared.Config inherited method log_file."""
        # Initialize key values
        expected = '{1}{0}pattoo.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file()
        self.assertEqual(result, expected)

    def test_log_file_api(self):
        """Test pattoo_shared.Config inherited method log_file_api."""
        # Initialize key values
        expected = '{1}{0}pattoo-api.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file_api()
        self.assertEqual(result, expected)

    def test_log_level(self):
        """Test pattoo_shared.Config inherited method log_level."""
        # Initialize key values
        expected = 'debug'

        # Test
        result = self.config.log_level()
        self.assertEqual(result, expected)

    def test_log_file_daemon(self):
        """Test pattoo_shared.Config inherited method log_file_daemon."""
        # Initialize key values
        expected = '{1}{0}pattoo-daemon.log'.format(
            os.sep, self.config.log_directory())

        # Test
        result = self.config.log_file_daemon()
        self.assertEqual(result, expected)

    def test_cache_directory(self):
        """Test pattoo_shared.Config inherited method cache_directory."""
        # Nothing should happen. Directory exists in testing.
        _ = self.config.cache_directory()

    def test_agent_cache_directory(self):
        """Test pattoo_shared.Config inherited method agent_cache_directory."""
        # Initialize key values
        agent_id = 123
        expected = '{1}{0}{2}'.format(
            os.sep, self.config.cache_directory(), agent_id)

        # Test
        result = self.config.agent_cache_directory(agent_id)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
