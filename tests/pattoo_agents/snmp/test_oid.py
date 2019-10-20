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
if EXEC_DIRECTORY.endswith('/pattoo-agents/tests/pattoo_agents/snmp') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print('''\
This script is not installed in the "pattoo-agents/tests/pattoo_agents/snmp" \
directory. Please fix.''')
    sys.exit(2)

# Pattoo imports
from pattoo_agents.agents.snmp import oid as class_oid
from tests.dev import unittest_setup



class TestOIDstring(unittest.TestCase):
    """Checks all OIDstring methods."""

    ##########################################################################
    # Initialize variable class
    ##########################################################################

    generic_random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for _ in range(9)])

    # OID related data
    value = {}
    value['fake_test_oid'] = ''
    for count in range(0, 4):
        num = random.randint(0, 9999)
        value['fake_test_oid'] = (
            '{}.{}'.format(value['fake_test_oid'], num))

    value['branch_no_dot'] = '1.300.6.1.2.1.1.2.0'
    value['branch_end_dot'] = '.1.300.6.1.2.1.1.2.0.'
    value['branch_mid_string'] = '1.maybe.6.1.2.1.1.2.0'

    def test___init__(self):
        """Testing function __init__."""
        # Fail if class is instantiated with an invalid integer value. (-1)
        with self.assertRaises(SystemExit):
            class_oid.OIDstring(-1)

    def test_node_z(self):
        """Testing function node_z."""
        # Define key variables
        oid = '.1.3.6.1.2.1.31.1.4.5.7'
        expected_value = 7

        #################################################
        # Test invalid OID
        #################################################

        object2test = class_oid.OIDstring(self.generic_random_string)
        with self.assertRaises(SystemExit):
            object2test.leaves(oid)

        #################################################
        # Test valid data
        #################################################

        object2test = class_oid.OIDstring(oid)
        self.assertEqual(object2test.node_z(), expected_value)

    def test_node_y(self):
        """Testing function node_y."""
        # Define key variables
        oid = '.1.3.6.1.2.1.31.1.4.5.7'
        expected_value = 5

        #################################################
        # Test invalid OID
        #################################################

        object2test = class_oid.OIDstring(self.generic_random_string)
        with self.assertRaises(SystemExit):
            object2test.leaves(oid)

        #################################################
        # Test valid data
        #################################################

        object2test = class_oid.OIDstring(oid)
        self.assertEqual(object2test.node_y(), expected_value)

    def test_node_x(self):
        """Testing function node_x."""
        # Define key variables
        oid = '.1.3.6.1.2.1.31.1.4.5.7'
        expected_value = 4

        #################################################
        # Test invalid OID
        #################################################

        object2test = class_oid.OIDstring(self.generic_random_string)
        with self.assertRaises(SystemExit):
            object2test.leaves(oid)

        #################################################
        # Test valid data
        #################################################

        object2test = class_oid.OIDstring(oid)
        self.assertEqual(object2test.node_x(), expected_value)

    def test_valid_format(self):
        """Testing function valid_format."""
        # Define key variables
        oid_no_dot = self.value['branch_no_dot']
        oid_end_dot = self.value['branch_end_dot']
        oid_mid_string = self.value['branch_mid_string']

        #################################################
        # Cannot be empty oid string
        #################################################

        object2test = class_oid.OIDstring('')
        self.assertEqual(object2test.valid_format(), False)

        #################################################
        # Cannot be blank oid
        #################################################

        object2test = class_oid.OIDstring('     ')
        self.assertEqual(object2test.valid_format(), False)

        #################################################
        # Cannot be oid with no leading '.'
        #################################################

        object2test = class_oid.OIDstring(oid_no_dot)
        self.assertEqual(object2test.valid_format(), False)

        #################################################
        # Cannot be oid with trailing '.'
        #################################################

        object2test = class_oid.OIDstring(oid_end_dot)
        self.assertEqual(object2test.valid_format(), False)

        #################################################
        # No non numeric strings between '.'
        #################################################

        object2test = class_oid.OIDstring(oid_mid_string)
        self.assertEqual(object2test.valid_format(), False)

        #################################################
        # Valid OID
        #################################################

        # Verify oid
        object2test = class_oid.OIDstring(self.value['fake_test_oid'])
        self.assertEqual(object2test.valid_format(), True)

    def test_leaves(self):
        """Testing function leaves."""
        #################################################
        # NOTE: Detailed OID and branch testing in
        # test_oid_valid_format and test_oid_branch_valid
        #################################################

        # Define key variables
        leaf = '1'
        branch = '.1.3.6.1.2.1.31.1.1.1.6'
        oid = '{}.{}'.format(branch, leaf)

        #################################################
        # Test invalid OID
        #################################################

        object2test = class_oid.OIDstring(self.generic_random_string)
        with self.assertRaises(SystemExit):
            object2test.leaves(branch)

        #################################################
        # Test invalid branch
        #################################################

        object2test = class_oid.OIDstring(oid)
        with self.assertRaises(SystemExit):
            object2test.leaves(self.generic_random_string)

        #################################################
        # Test valid data
        #################################################

        # Test with branch not in oid_type database
        fake_branch = '.9.3.6.1.2.1.31.1.1.1.6'
        object2test = class_oid.OIDstring(oid)
        result = object2test.leaves(fake_branch)
        self.assertEqual(result, None)

        # Single number leaf
        object2test = class_oid.OIDstring(oid)
        result = object2test.leaves(branch)
        self.assertEqual(result, '.{}'.format(leaf))

        # Multi-number leaf
        leaf = '1.34'
        oid = '{}.{}'.format(branch, leaf)
        object2test = class_oid.OIDstring(oid)
        result = object2test.leaves(branch)
        self.assertEqual(result, '.{}'.format(leaf))

    def test__oid_branch_valid(self):
        """Testing function _oid_branch_valid."""
        # Tested by other methods in this file
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
