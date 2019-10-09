"""Module used to manipulate OID strings and validate OIDs."""

# Import pattoo libraries
from pattoo import log
from pattoo import data



class OIDstring(object):
    """Class to manipulate OID strings and validate OIDs."""

    def __init__(self, oid):
        """Initialize the class.

        Args:
            oid: OID to process

        Returns:
            None

        """
        # Initialize key variables
        self.oid = str(oid)

        # OID must be string
        if data.is_numeric(self.oid):
            log_message = ('OID value {} is not a string.'.format(
                self.oid))
            log.log2die(1380, log_message)

    def node_z(self):
        """Get the last node of OID.

        Args:
            None

        Returns:
            Last node

        """
        # Initialize key variables
        oid = self.oid

        # Valid OID?
        if self.valid_format() is False:
            log_message = ('OID {} has incorrect format'.format(
                oid))
            log.log2die(1446, log_message)

        # Process data
        nodes = oid.split('.')
        return int(nodes[-1])

    def node_y(self):
        """Get the second to last node of OID.

        Args:
            None

        Returns:
            Last node

        """
        # Initialize key variables
        oid = self.oid

        # Valid OID?
        if self.valid_format() is False:
            log_message = ('OID {} has incorrect format'.format(
                oid))
            log.log2die(1448, log_message)

        # Process data
        nodes = oid.split('.')
        return int(nodes[-2])

    def node_x(self):
        """Get the third to last node of OID.

        Args:
            None

        Returns:
            Last node

        """
        # Initialize key variables
        oid = self.oid

        # Valid OID?
        if self.valid_format() is False:
            log_message = ('OID {} has incorrect format'.format(
                oid))
            log.log2die(1447, log_message)

        # Process data
        nodes = oid.split('.')
        return int(nodes[-3])

    def valid_format(self, is_branch=False):
        """Determine whether the format of the oid is correct.

        Args:
            is_branch: Ture if OID is a branch

        Returns:
            invalid: False if OK

        """
        # Initialize key variables
        oid = self.oid
        valid = True

        # oid cannot be boolean
        if oid is True:
            valid = False
        if oid is False:
            valid = False
        if oid is None:
            valid = False

        # oid cannot be numeric
        if isinstance(oid, str) is False:
            valid = False

        # Make sure the oid is not blank
        stripped_oid = oid.strip()
        if len(stripped_oid) == 0:
            valid = False
            return valid

        # Must start with a '.'
        if oid[0] != '.':
            valid = False

        # Must not end with a '.'
        if oid[-1] == '.':
            valid = False

        # Test each node to be numeric
        nodes = oid.split('.')

        # Remove the first element of the list
        nodes.pop(0)
        for value in nodes:
            if data.is_numeric(value) is False:
                valid = False

        # Otherwise valid
        return valid

    def leaves(self, branch):
        """Get the last octets in oid that extend beyond branch.

        Args:
            branch: OID branch to check against

        Returns:
            leaves: The last octets of oid

        """
        # Initialize key variables
        leaves = None
        oid = self.oid

        # Valid OID?
        if self.valid_format() is False:
            log_message = ('OID {} has incorrect format'.format(
                oid))
            log.log2die(1443, log_message)

        # Valid branch?
        oid_methods = OIDstring(branch)
        if oid_methods.valid_format() is False:
            log_message = ('Branch {} has incorrect format'.format(
                branch))
            log.log2die(1444, log_message)

        # Process OID and branch
        if branch in oid:
            if oid[:len(branch)] == branch:
                leaves = oid[len(branch):]

        # Return
        return leaves
