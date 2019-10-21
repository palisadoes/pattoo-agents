#!/usr/bin/env python3
"""Test the class_oid module."""

import sys
import unittest
import os
import random
import string

# Try to create a working PYTHONPATH
EXEC_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            EXEC_DIRECTORY, os.pardir)), os.pardir)), os.pardir))
if EXEC_DIRECTORY.endswith('/pattoo-agents/tests/test_pattoo_agents/snmp') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print('''\
This script is not installed in the "pattoo-agents/tests/test_pattoo_agents/snmp" \
directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_agents.agents.snmp import configuration
from pattoo_agents.agents.snmp.variables import SNMPVariable, OIDVariable
from tests.dev import unittest_setup


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
        self.assertEqual(snmpvariable.community, 'public')
        self.assertEqual(snmpvariable.port, 161)
        self.assertEqual(snmpvariable.version, 2)
        self.assertEqual(snmpvariable.authpassword, None)
        self.assertEqual(snmpvariable.authprotocol, None)
        self.assertEqual(snmpvariable.privpassword, None)
        self.assertEqual(snmpvariable.privprotocol, None)
        self.assertEqual(snmpvariable.secname, None)

    def test_oidvariables(self):
        """Testing function oidvariables."""
        # Initialize key variables
        result = self.config.oidvariables()
        print(result)

        # Test
        self.assertEqual(isinstance(result, list), True)
        self.assertEqual(len(result), 1)

        # Test the only SNMPVariable in the result
        oidvariable = result[0]
        self.assertEqual(isinstance(oidvariable, OIDVariable), True)
        self.assertEqual(
            oidvariable.oids,
            ['.1.3.6.1.2.1.2.2.1.10', '.1.3.6.1.2.1.2.2.1.16'])
        self.assertEqual(oidvariable.ip_devices, ['localhost'])

    def test__validate_snmp(self):
        """Testing function _validate_snmp."""
        pass

    def test__validate_oids(self):
        """Testing function _validate_oids."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
