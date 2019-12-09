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
        '/pattoo-agents/tests/test_pattoo_agents/snmp') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the \
"pattoo-agents/tests/test_pattoo_agents/snmp" directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_shared.variables import PollingPoint, TargetPollingPoints
from pattoo_agents.snmp import configuration
from pattoo_agents.snmp.variables import SNMPVariable
from tests.libraries.configuration import UnittestConfig


class TestConfigSNMP(unittest.TestCase):
    """Checks all ConfigSNMP methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################
    config = configuration.ConfigSNMP()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_snmpvariables(self):
        """Testing function snmpvariables."""
        # Initialize key variables
        result = self.config.snmpvariables()

        # Test
        self.assertEqual(isinstance(result, list), True)
        self.assertEqual(len(result), 1)

        # Test the only SNMPVariable in the result
        snmpvariable = result[0]
        self.assertEqual(isinstance(snmpvariable, SNMPVariable), True)
        authvariable = snmpvariable.snmpauth
        self.assertEqual(authvariable.community, 'public')
        self.assertEqual(authvariable.port, 161)
        self.assertEqual(authvariable.version, 2)
        self.assertEqual(authvariable.authpassword, None)
        self.assertEqual(authvariable.authprotocol, None)
        self.assertEqual(authvariable.privpassword, None)
        self.assertEqual(authvariable.privprotocol, None)
        self.assertEqual(authvariable.secname, None)

    def test_target_polling_points(self):
        """Testing function oidvariables."""
        # Initialize key variables.
        result = self.config.target_polling_points()
        oids = ['.1.3.6.1.2.1.2.2.1.10', '.1.3.6.1.2.1.2.2.1.16']

        # Test
        self.assertEqual(isinstance(result, list), True)
        self.assertEqual(len(result), 1)

        # Test each dpt
        item = result[0]
        self.assertEqual(isinstance(item, TargetPollingPoints), True)
        self.assertEqual(item.target, 'localhost')
        for index, value in enumerate(item.data):
            self.assertEqual(isinstance(value, PollingPoint), True)
            self.assertEqual(value.address, oids[index])
            self.assertEqual(value.multiplier, 8)

    def test__validate_snmp(self):
        """Testing function _validate_snmp."""
        pass

    def test__validate_oids(self):
        """Testing function _validate_oids."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
