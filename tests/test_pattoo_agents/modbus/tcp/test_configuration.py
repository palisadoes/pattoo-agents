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
                os.path.abspath(os.path.join(
                        EXEC_DIR,
                        os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = ('''\
{0}pattoo-agents{0}tests{0}test_pattoo_agents{0}modbus{0}tcp'''.format(os.sep))
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from pattoo_agents.modbus.tcp import configuration
from pattoo_agents.modbus.variables import (
    InputRegisterVariable, HoldingRegisterVariable, RegisterVariable,
    TargetRegisterVariables)
from tests.libraries.configuration import UnittestConfig


class TestConfigModbusTCP(unittest.TestCase):
    """Checks all ConfigModbusTCP methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################
    config = configuration.ConfigModbusTCP()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_polling_interval(self):
        """Test pattoo_shared.Config inherited method polling_interval."""
        # Initialize key values
        expected = 457

        # Test
        result = self.config.polling_interval()
        self.assertEqual(result, expected)

    def test_registervariables(self):
        """Testing method / function registervariables."""
        # Initialize variables
        expected_ip_target = 'unittest.modbus.tcp.target.net'
        register_variables = []

        # Test
        result = self.config.registervariables()
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 2)
        for drv in result:
            self.assertTrue(isinstance(drv, TargetRegisterVariables))
            self.assertTrue(drv.valid)
            self.assertEqual(drv.target, expected_ip_target)
            for _rv in drv.data:
                self.assertTrue(isinstance(_rv, RegisterVariable))
                self.assertTrue(_rv.valid)
            register_variables.extend(drv.data)

        # Evaluate each RegisterVariable
        self.assertEqual(len(register_variables), 3)
        for index, _rv in enumerate(register_variables):
            if index == 0:
                self.assertEqual(_rv.address, 387)
                self.assertEqual(_rv.count, 2)
                self.assertEqual(_rv.multiplier, 7)
                self.assertEqual(_rv.unit, 3)
                self.assertTrue(isinstance(_rv, InputRegisterVariable))
            elif index == 1:
                self.assertEqual(_rv.address, 123)
                self.assertEqual(_rv.count, 1)
                self.assertEqual(_rv.multiplier, 9)
                self.assertEqual(_rv.unit, 3)
                self.assertTrue(isinstance(_rv, HoldingRegisterVariable))
            else:
                self.assertEqual(_rv.address, 456)
                self.assertEqual(_rv.count, 1)
                self.assertEqual(_rv.multiplier, 9)
                self.assertEqual(_rv.unit, 3)
                self.assertTrue(isinstance(_rv, HoldingRegisterVariable))

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
        """Test pattoo_shared.Config inherited method agent_api_ip_bind_port."""
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


class TestBasicFunctions(unittest.TestCase):
    """Checks all ConfigSNMP methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################

    def test__create_drv(self):
        """Testing method / function _create_drv."""
        # Tested by test_registervariables
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
