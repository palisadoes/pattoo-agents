#!/usr/bin/env python3
"""Class used to set test configuration used by unittests."""

# Standard imports
import sys
import os

# Try to create a working PYTHONPATH
TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
ROOT_DIRECTORY = os.path.abspath(os.path.join(TEST_DIRECTORY, os.pardir))
if TEST_DIRECTORY.endswith('/pattoo-agents/test') is True:
    sys.path.append(ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "pattoo-agents/bin" directory. '
        'Please fix.')
    sys.exit(2)


# pattoo libraries
from test import unittest_setup


def main():
    """Create test configurations."""
    # Check environment
    config = unittest_setup.TestConfig()
    config.create()


if __name__ == '__main__':
    # Do the unit test
    main()
