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
        '/pattoo-agents/tests/test_pattoo_agents/snmp') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print('''\
This script is not installed in the \
"pattoo-agents/tests/test_pattoo_agents/snmp" \
directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_agents.agents.snmp.variables import (
    SNMPVariable, SNMPVariableList, OIDVariable, SNMPAuth)
from tests.dev import unittest_setup


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
        self.assertEqual(sav.authprotocol, None)
        self.assertEqual(sav.authpassword, authpassword)
        self.assertEqual(sav.privprotocol, None)
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
        ip_device = 'localhost'
        snmpvariable = SNMPVariable(snmpauth=sav, ip_device=ip_device)

        # Test
        self.assertEqual(snmpvariable.snmpauth, sav)
        self.assertTrue(isinstance(snmpvariable.snmpauth, SNMPAuth))
        self.assertEqual(snmpvariable.ip_device, ip_device)
        self.assertTrue(snmpvariable.active)

        snmpvariable = SNMPVariable()
        self.assertFalse(snmpvariable.active)

    def test___repr__(self):
        """Testing function __repr__."""
        # Test defaults
        snmpvariable = SNMPVariable()
        expected = ('''\
<SNMPVariable snmpauth=None, ip_device=None, active=False>''')
        result = snmpvariable.__repr__()
        self.assertEqual(expected, result)

        # Test non-default
        sav = SNMPAuth()
        ip_device = 'localhost'
        snmpvariable = SNMPVariable(snmpauth=sav, ip_device=ip_device)
        expected = ('''\
<SNMPVariable snmpauth=<SNMPAuth version=2, community='public', port=161, \
secname=None, authprotocol=None authpassword=None, privpassword=None, \
privprotocol=None>, ip_device='localhost', active=True>''')
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
        ip_device = 'localhost'
        svl = SNMPVariableList(snmpauth=sav, ip_devices=ip_device)
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
        ip_device = 'localhost'
        svl = SNMPVariableList(snmpauth=sav, ip_devices=ip_device)
        expected = ('''\
<SNMPVariableList snmpvariables=[<SNMPVariable snmpauth=<SNMPAuth version=2, \
community='public', port=161, secname=None, authprotocol=None \
authpassword=None, privpassword=None, privprotocol=None>, \
ip_device='localhost', active=True>]>''')
        result = svl.__repr__()
        self.assertEqual(expected, result)


class TestOIDVariable(unittest.TestCase):
    """Checks all OIDVariable methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing function __init__."""
        # Test defaults
        _variable = OIDVariable()
        self.assertFalse(_variable.active)

        # Test non-defaults
        oids = '.1.1.1.1.1'
        ip_devices = 'localhost'
        _variable = OIDVariable(oids=oids, ip_devices=ip_devices)
        self.assertTrue(_variable.active)
        self.assertEqual(_variable.oids, [oids])
        self.assertEqual(_variable.ip_devices, [ip_devices])

    def test___repr__(self):
        """Testing function __repr__."""
        # Test default
        _variable = OIDVariable()
        expected = ('''<OIDVariable active=False, oids=[], ip_devices=[]>''')
        result = _variable.__repr__()
        self.assertEqual(expected, result)

        # Test non-defaults
        oids = '.1.1.1.1.1'
        ip_devices = 'localhost'
        _variable = OIDVariable(oids=oids, ip_devices=ip_devices)
        expected = ('''\
<OIDVariable active=True, oids=['.1.1.1.1.1'], ip_devices=['localhost']>''')
        result = _variable.__repr__()
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
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
