#!/usr/bin/env python3
"""Test the SNMP module."""

import sys
import os
import unittest

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


# Import Colovore libraries
from pattoo_shared.variables import DataPoint
from pattoo_agents.snmp.variables import (
    SNMPAuth, SNMPVariable, SNMPVariableList)
from pattoo_agents.snmp.snmp import SNMP
from tests.libraries.configuration import UnittestConfig


class MockSNMP(object):
    """Mock for use of SNMP."""

    def __init__(self, snmpvariable):

        #####################################################################
        # Create a list of ifMIB oid branches to be used to create
        #####################################################################

        # Add simulated ifMIB walk values for interface descriptions
        self.data = {}

        # IfDesc
        self.data['.1.3.6.1.2.1.2.2.1.2'] = [
            DataPoint('.1.3.6.1.2.1.2.2.1.2.1', 'lo', data_type=2),
            DataPoint('.1.3.6.1.2.1.2.2.1.2.2', 'eth0', data_type=2),
            DataPoint('.1.3.6.1.2.1.2.2.1.2.3', 'wlan0', data_type=2)]

        # sysObjectID
        self.data['.1.3.6.1.2.1.1.2.0'] = [
            DataPoint('.1.3.6.1.2.1.1.2.0', '.1.3.6.1.1234', data_type=2)]

        # ifInOctets
        self.data['.1.3.6.1.2.1.2.2.1.10'] = [
            DataPoint('.1.3.6.1.2.1.2.2.1.10.1', 83554391, data_type=32),
            DataPoint('.1.3.6.1.2.1.2.2.1.10.2', 1099211361, data_type=32),
            DataPoint('.1.3.6.1.2.1.2.2.1.10.3', 0, data_type=32)]
        # ifOutOctets
        self.data['.1.3.6.1.2.1.2.2.1.16'] = [
            DataPoint('.1.3.6.1.2.1.2.2.1.16.1', 83596845, data_type=32),
            DataPoint('.1.3.6.1.2.1.2.2.1.16.2', 2788372879, data_type=32),
            DataPoint('.1.3.6.1.2.1.2.2.1.16.3', 0, data_type=32)]

    def contactable(self):
        """Determine whether contactable.

        Args:
            None

        Returns:
            result: Device ID

        """
        # Return
        result = True
        return result

    def walk(self, item):
        """Return simulated dict of OID values for device.

        Args:
            item: OID branch to walk

        Returns:
            result: List of DataPoint objects

        """
        # Return
        if item in self.data:
            result = self.data[item]
        else:
            result = []
        return result

    def get(self, item):
        """Return simulated dict of OID values for device.

        Args:
            item: OID branch to get

        Returns:
            result: List of DataPoint objects

        """
        # Return
        if item in self.data:
            result = self.data[item]
        else:
            result = []
        return result

    def oid_exists(self, item):
        """Determine whether branch exists.

        Args:
            oid: OID to test

        Returns:
            result: True if exists

        """
        # Return
        result = bool(item in self.data)
        return result

    def branch_exists(self, item):
        """Determine whether branch exists.

        Args:
            item: OID branch to get

        Returns:
            result: True if exists

        """
        # Return
        result = bool(item in self.data)
        return result


class TestSNMP(unittest.TestCase):
    """Checks all SNMP methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_contactable(self):
        """Testing method / function contactable."""
        pass

    def test_sysobjectid(self):
        """Testing method / function sysobjectid."""
        pass

    def test_oid_exists(self):
        """Testing method / function oid_exists."""
        pass

    def test_branch_exists(self):
        """Testing method / function branch_exists."""
        pass

    def test_walk(self):
        """Testing method / function walk."""
        pass

    def test_get(self):
        """Testing method / function get."""
        pass

    def test_query(self):
        """Testing method / function query."""
        pass


class Test_Session(unittest.TestCase):
    """Checks all _Session methods."""

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test__session(self):
        """Testing method / function _session."""
        pass

    def test__security_level(self):
        """Testing method / function _security_level."""
        pass

    def test__auth_protocol(self):
        """Testing method / function _auth_protocol."""
        pass

    def test__priv_protocol(self):
        """Testing method / function _priv_protocol."""
        pass


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    def test__process_error(self):
        """Testing method / function _process_error."""
        pass

    def test__convert_results(self):
        """Testing method / function _convert_results."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
