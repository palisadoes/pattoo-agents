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
_EXPECTED = (
    '{0}pattoo-agents{0}tests{0}test_pattoo_agents{0}snmp'.format(os.sep))
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

# Pattoo imports
from pattoo_agents.snmp.variables import (
    SNMPVariable, SNMPVariableList, SNMPAuth)
from tests.libraries.configuration import UnittestConfig


class TestSNMPAuth(unittest.TestCase):
    """Checks all SNMPAuth methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing function __init__."""
        # Setup SNMPAuth variable
        community = 'brown_bear'
        port = 4500
        secname = 'grizzly_bear'
        authprotocol = 'md5'
        authpassword = 'polar_bear'
        privprotocol = 'aes'
        privpassword = 'black_bear'

        # Test with defaults
        sav = SNMPAuth()
        self.assertEqual(sav.port, 161)
        self.assertEqual(sav.version, 2)
        self.assertEqual(sav.community, 'public')
        self.assertIsNone(sav.secname)
        self.assertIsNone(sav.authprotocol)
        self.assertIsNone(sav.authpassword)
        self.assertIsNone(sav.privprotocol)
        self.assertIsNone(sav.privpassword)

        # Test SNMPv2
        sav = SNMPAuth(community=community)
        self.assertEqual(sav.port, 161)
        self.assertEqual(sav.version, 2)
        self.assertEqual(sav.community, community)
        self.assertIsNone(sav.secname)
        self.assertIsNone(sav.authprotocol)
        self.assertIsNone(sav.authpassword)
        self.assertIsNone(sav.privprotocol)
        self.assertIsNone(sav.privpassword)

        sav = SNMPAuth(
            version=2, community=community, port=port,
            secname=secname,
            authprotocol=authprotocol, authpassword=authpassword,
            privprotocol=privprotocol, privpassword=privpassword)
        self.assertEqual(sav.port, port)
        self.assertEqual(sav.version, 2)
        self.assertEqual(sav.community, community)
        self.assertIsNone(sav.secname)
        self.assertIsNone(sav.authprotocol)
        self.assertIsNone(sav.authpassword)
        self.assertIsNone(sav.privprotocol)
        self.assertIsNone(sav.privpassword)

        # Test SNMPv3
        sav = SNMPAuth(
            version=3, community=community, port=port,
            secname=secname,
            authprotocol=authprotocol, authpassword=authpassword,
            privprotocol=privprotocol, privpassword=privpassword)
        self.assertEqual(sav.port, port)
        self.assertEqual(sav.version, 3)
        self.assertIsNone(sav.community)
        self.assertEqual(sav.secname, secname)
        self.assertEqual(sav.authprotocol, authprotocol.upper())
        self.assertEqual(sav.authpassword, authpassword)
        self.assertEqual(sav.privprotocol, privprotocol.upper())
        self.assertEqual(sav.privpassword, privpassword)

        sav = SNMPAuth(
            version=3, community=community, port=port,
            secname=secname,
            authprotocol='teddy_bear', authpassword=authpassword,
            privprotocol='panda_bear', privpassword=privpassword)
        self.assertEqual(sav.port, port)
        self.assertEqual(sav.version, 3)
        self.assertIsNone(sav.community)
        self.assertEqual(sav.secname, secname)
        self.assertEqual(sav.authprotocol, 'SHA')
        self.assertEqual(sav.authpassword, authpassword)
        self.assertEqual(sav.privprotocol, 'AES')
        self.assertEqual(sav.privpassword, privpassword)

    def test___repr__(self):
        """Testing function __repr__."""
        # Test defaults
        sav = SNMPAuth()
        expected = ('''\
<SNMPAuth version=2, community='public', port=161, secname=None, \
authprotocol=None authpassword=None, privpassword=None, privprotocol=None>''')
        result = sav.__repr__()
        self.assertEqual(expected, result)


class TestSNMPVariable(unittest.TestCase):
    """Checks all SNMPVariable methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing function __init__."""
        # Initialize variables
        sav = SNMPAuth()
        ip_target = 'localhost'
        snmpvariable = SNMPVariable(snmpauth=sav, ip_target=ip_target)

        # Test
        self.assertEqual(snmpvariable.snmpauth, sav)
        self.assertTrue(isinstance(snmpvariable.snmpauth, SNMPAuth))
        self.assertEqual(snmpvariable.ip_target, ip_target)
        self.assertTrue(snmpvariable.valid)

        snmpvariable = SNMPVariable()
        self.assertFalse(snmpvariable.valid)

    def test___repr__(self):
        """Testing function __repr__."""
        # Test defaults
        snmpvariable = SNMPVariable()
        expected = ('''\
<SNMPVariable snmpauth=None, ip_target=None, valid=False>''')
        result = snmpvariable.__repr__()
        self.assertEqual(expected, result)

        # Test non-default
        sav = SNMPAuth()
        ip_target = 'localhost'
        snmpvariable = SNMPVariable(snmpauth=sav, ip_target=ip_target)
        expected = ('''\
<SNMPVariable snmpauth=<SNMPAuth version=2, community='public', port=161, \
secname=None, authprotocol=None authpassword=None, privpassword=None, \
privprotocol=None>, ip_target='localhost', valid=True>''')
        result = snmpvariable.__repr__()
        self.assertEqual(expected, result)


class TestSNMPVariableList(unittest.TestCase):
    """Checks all SNMPVariableList methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing function __init__."""
        # Test default
        svl = SNMPVariableList()
        self.assertFalse(bool(svl.snmpvariables))

        # Test non-default
        sav = SNMPAuth()
        ip_target = 'localhost'
        svl = SNMPVariableList(snmpauth=sav, ip_targets=ip_target)
        self.assertTrue(bool(svl.snmpvariables))

        for item in svl.snmpvariables:
            self.assertTrue(isinstance(item, SNMPVariable))

    def test___repr__(self):
        """Testing function __repr__."""
        # Test default
        svl = SNMPVariableList()
        expected = ('''<SNMPVariableList snmpvariables=[]>''')
        result = svl.__repr__()
        self.assertEqual(expected, result)

        # Test non-default
        sav = SNMPAuth()
        ip_target = 'localhost'
        svl = SNMPVariableList(snmpauth=sav, ip_targets=ip_target)
        expected = ('''\
<SNMPVariableList snmpvariables=[<SNMPVariable snmpauth=<SNMPAuth version=2, \
community='public', port=161, secname=None, authprotocol=None \
authpassword=None, privpassword=None, privprotocol=None>, \
ip_target='localhost', valid=True>]>''')
        result = svl.__repr__()
        self.assertEqual(expected, result)


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test__strip_non_printable(self):
        """Testing function _strip_non_printable."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
