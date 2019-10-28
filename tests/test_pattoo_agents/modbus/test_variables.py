#!/usr/bin/env python3
"""Test module."""

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
        '/pattoo-agents/tests/test_pattoo_agents/modbus') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the \
"pattoo-agents/tests/test_pattoo_agents/modbus" directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_agents.agents.modbus.variables import (
    RegisterVariable, InputRegisterVariable,
    HoldingRegisterVariable, DeviceRegisterVariables, )
from tests.libraries.configuration import UnittestConfig


class TestRegisterVariable(unittest.TestCase):
    """Checks all SNMPAuth methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        # Test with invalid count
        _rv = RegisterVariable(address=1, count=2, unit=3)
        self.assertTrue(isinstance(_rv, RegisterVariable))
        self.assertEqual(_rv.address, 1)
        self.assertEqual(_rv.count, 2)
        self.assertEqual(_rv.unit, 3)
        self.assertTrue(_rv.valid)

        # Test with no arguments
        _rv = RegisterVariable()
        self.assertTrue(isinstance(_rv, RegisterVariable))
        self.assertIsNone(_rv.address)
        self.assertEqual(_rv.count, 1)
        self.assertEqual(_rv.unit, 0)
        self.assertFalse(_rv.valid)

        # Test with invalid count
        address = 1
        unit = 0
        for count in [5000, False, None, True, 'test', -1]:
            _rv = RegisterVariable(address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)

        # Test with invalid unit
        address = 1
        count = 0
        for unit in [5000, False, None, True, 'test', -1]:
            _rv = RegisterVariable(address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)

        # Test with invalid Address
        count = 1
        unit = 0
        for address in [False, None, True, 'test', -1]:
            _rv = RegisterVariable(address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)

    def test___repr__(self):
        """Testing method / function __repr__."""
        # Test
        _rv = RegisterVariable()
        result = _rv.__repr__()
        expected = '''\
<RegisterVariable.valid=False, address=None, count=1, unit=0>'''
        self.assertEqual(result, expected)

        _rv = RegisterVariable(address=1, count=2, unit=3)
        result = _rv.__repr__()
        expected = '<RegisterVariable.valid=True, address=1, count=2, unit=3>'
        self.assertEqual(result, expected)


class TestInputRegisterVariable(unittest.TestCase):
    """Checks all InputRegisterVariable methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        # Test with invalid count
        _rv = InputRegisterVariable(address=1, count=2, unit=3)
        self.assertTrue(isinstance(_rv, InputRegisterVariable))
        self.assertTrue(isinstance(_rv, RegisterVariable))
        self.assertEqual(_rv.address, 1)
        self.assertEqual(_rv.count, 2)
        self.assertEqual(_rv.unit, 3)
        self.assertTrue(_rv.valid)

        # Test with no arguments
        _rv = InputRegisterVariable()
        self.assertTrue(isinstance(_rv, InputRegisterVariable))
        self.assertTrue(isinstance(_rv, RegisterVariable))
        self.assertIsNone(_rv.address)
        self.assertEqual(_rv.count, 1)
        self.assertEqual(_rv.unit, 0)
        self.assertFalse(_rv.valid)

        # Test with invalid count
        address = 1
        unit = 0
        for count in [5000, False, None, True, 'test', -1]:
            _rv = InputRegisterVariable(
                address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, InputRegisterVariable))
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)

        # Test with invalid unit
        address = 1
        count = 0
        for unit in [5000, False, None, True, 'test', -1]:
            _rv = InputRegisterVariable(
                address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, InputRegisterVariable))
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)

        # Test with invalid Address
        count = 1
        unit = 0
        for address in [False, None, True, 'test', -1]:
            _rv = InputRegisterVariable(
                address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, InputRegisterVariable))
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)


class TestHoldingRegisterVariable(unittest.TestCase):
    """Checks all HoldingRegisterVariable methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        # Test with invalid count
        _rv = HoldingRegisterVariable(address=1, count=2, unit=3)
        self.assertTrue(isinstance(_rv, HoldingRegisterVariable))
        self.assertTrue(isinstance(_rv, RegisterVariable))
        self.assertEqual(_rv.address, 1)
        self.assertEqual(_rv.count, 2)
        self.assertEqual(_rv.unit, 3)
        self.assertTrue(_rv.valid)

        # Test with no arguments
        _rv = HoldingRegisterVariable()
        self.assertTrue(isinstance(_rv, HoldingRegisterVariable))
        self.assertTrue(isinstance(_rv, RegisterVariable))
        self.assertIsNone(_rv.address)
        self.assertEqual(_rv.count, 1)
        self.assertEqual(_rv.unit, 0)
        self.assertFalse(_rv.valid)

        # Test with invalid count
        address = 1
        unit = 0
        for count in [5000, False, None, True, 'test', -1]:
            _rv = HoldingRegisterVariable(
                address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, HoldingRegisterVariable))
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)

        # Test with invalid unit
        address = 1
        count = 0
        for unit in [5000, False, None, True, 'test', -1]:
            _rv = HoldingRegisterVariable(
                address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, HoldingRegisterVariable))
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)

        # Test with invalid Address
        count = 1
        unit = 0
        for address in [False, None, True, 'test', -1]:
            _rv = HoldingRegisterVariable(
                address=address, count=count, unit=unit)
            self.assertTrue(isinstance(_rv, HoldingRegisterVariable))
            self.assertTrue(isinstance(_rv, RegisterVariable))
            self.assertEqual(_rv.address, address)
            self.assertEqual(_rv.count, count)
            self.assertEqual(_rv.unit, unit)
            self.assertFalse(_rv.valid)


class TestDeviceRegisterVariables(unittest.TestCase):
    """Checks all DeviceRegisterVariables methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        # Setup DeviceRegisterVariables
        device = 'localhost'
        drv = DeviceRegisterVariables(device)

        # Test initial vlues
        self.assertEqual(drv.device, device)
        self.assertFalse(drv.valid)
        self.assertEqual(drv.data, [])

    def test___repr__(self):
        """Testing method / function __repr__."""
        pass

    def test_add(self):
        """Testing method / function add."""
        # Initialize DeviceRegisterVariables
        device = 'teddy_bear'
        drv = DeviceRegisterVariables(device)
        self.assertEqual(drv.device, device)
        self.assertFalse(drv.valid)
        self.assertEqual(drv.data, [])

        # Setup DataVariable
        address = 1
        count = 2
        unit = 3
        variable = HoldingRegisterVariable(
            address=address, count=count, unit=unit)

        # Test add
        drv.add(None)
        self.assertEqual(drv.data, [])

        drv.add(variable)
        self.assertTrue(bool(drv.data))
        self.assertTrue(isinstance(drv.data, list))
        self.assertEqual(len(drv.data), 1)

        # Test the values in the variable
        _variable = drv.data[0]
        self.assertEqual(_variable.address, address)
        self.assertEqual(_variable.count, count)
        self.assertEqual(_variable.unit, unit)
        

if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
