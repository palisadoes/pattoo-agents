"""Module for classes that format variables."""


class RegisterVariable(object):
    """Variable representation for Register data for Modbus polling."""

    def __init__(self, address=None, count=1, unit=None):
        """Initialize the class.

        Args:
            address: Register address
            count: The number of registers to read
            unit: The slave unit this request is targeting

        Returns:
            None

        """
        # Initialize ip_devices
        self.address = address
        self.count = count
        self.unit = unit

        # Set object as being active
        self.active = False not in [
            isinstance(address, int), isinstance(count, int),
            bool(address), bool(count),
            (unit is None or isinstance(unit, int)) and (
                unit is not False) and (unit is not True)
            ]

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return ('''\
<{} active={}, address={}, count={}, unit={}>\
'''.format(self.__class__.__name__,
           repr(self.active), repr(self.address),
           repr(self.count), repr(self.unit)))


class InputRegisterVariable(RegisterVariable):
    """Variable representation for Register data for Modbus polling."""

    def __init__(self, address=None, count=1, unit=None):
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

    def __init__(self, address=None, count=1, unit=None):
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
            self.active: True if the object is populated with RegisterVariables

        """
        # Initialize key variables
        self.data = []
        self.device = device
        self.active = False

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Create a printable variation of the value
        result = (
            '<{0} device={1} active={2}, data={3}'
            ''.format(
                self.__class__.__name__,
                repr(self.device), repr(self.active), repr(self.data)
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

                # Set object as being active
                self.active = False not in [bool(self.data), bool(self.device)]
