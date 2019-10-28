"""Module for classes that format variables."""


class RegisterVariable(object):
    """Variable representation for Register data for Modbus polling."""

    def __init__(self, address=None, count=1, unit=0):
        """Initialize the class.

        Args:
            address: Register address
            count: The number of registers to read
            unit: The slave unit this request is targeting

        Returns:
            None

        """
        # Set object as being.valid
        valid = False not in [
            isinstance(address, int),
            bool(address),
            address is not False,
            address is not True,
            address is not None,
            isinstance(count, int),
            count is not False,
            count is not True,
            count is not None,
            isinstance(unit, int) is True,
            unit is not False,
            unit is not True,
            unit is not None
            ]
        # This part is separate as we need to do some mathematical functions
        # that are based on the validity of the previous tests
        if valid is True:
            self.valid = False not in [
                valid,
                0 <= unit <= 246,
                0 < count < 2008,
                address > 0
                ]
        else:
            self.valid = False

        # Assign values
        self.count = count
        self.unit = unit
        self.address = address

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return ('''\
<{}.valid={}, address={}, count={}, unit={}>\
'''.format(self.__class__.__name__,
           repr(self.valid), repr(self.address),
           repr(self.count), repr(self.unit)))


class InputRegisterVariable(RegisterVariable):
    """Variable representation for Register data for Modbus polling."""

    def __init__(self, address=None, count=1, unit=0):
        """Initialize the class.

        Args:
            address: Register address
            count: The number of registers to read
            unit: The slave unit this request is targeting

        Returns:
            None

        """
        # Initialize variables
        RegisterVariable.__init__(
            self, address=address, count=count, unit=unit)


class HoldingRegisterVariable(RegisterVariable):
    """Variable representation for Register data for Modbus polling."""

    def __init__(self, address=None, count=1, unit=0):
        """Initialize the class.

        Args:
            address: Register address
            count: The number of registers to read
            unit: The slave unit this request is targeting

        Returns:
            None

        """
        # Initialize variables
        RegisterVariable.__init__(
            self, address=address, count=count, unit=unit)


class DeviceRegisterVariables(object):
    """Object defining a list of RegisterVariable objects.

    Stores RegisterVariables polled from a specific ip_device.

    """

    def __init__(self, device):
        """Initialize the class.

        Args:
            device: Device polled to get the RegisterVariable objects

        Returns:
            None

        Variables:
            self.data: List of RegisterVariables retrieved from the device
            self.valid: True if the object is populated with RegisterVariables

        """
        # Initialize key variables
        self.data = []
        self.device = device
        self.valid = False

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Create a printable variation of the value
        result = (
            '<{0} device={1}.valid={2}, data={3}'
            ''.format(
                self.__class__.__name__,
                repr(self.device), repr(self.valid), repr(self.data)
            )
        )
        return result

    def add(self, items):
        """Append RegisterVariable to the internal self.data list.

        Args:
            items: A RegisterVariable object list

        Returns:
            None

        """
        # Ensure there is a list of objects
        if isinstance(items, list) is False:
            items = [items]

        # Only append approved data types
        for item in items:
            if isinstance(item, RegisterVariable) is True:
                self.data.append(item)

                # Set object as being.valid
                self.valid = False not in [bool(self.data), bool(self.device)]
