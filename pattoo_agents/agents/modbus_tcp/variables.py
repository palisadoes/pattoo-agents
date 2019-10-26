"""Module for classes that format variables."""


class RegisterVariable(object):
    """Variable representation for Register data for ModbusTCP polling."""

    def __init__(self, registers=None, ip_devices=None):
        """Initialize the class.

        Args:
            registers: Modbus registers
            ip_devices: Devices that require data from registers

        Returns:
            None

        """
        # Initialize ip_devices
        if isinstance(ip_devices, str) is True:
            self.ip_devices = [ip_devices]
        elif isinstance(ip_devices, list) is True:
            self.ip_devices = ip_devices
        else:
            self.ip_devices = []

        # Initialize registers
        if isinstance(registers, str) is True:
            self.registers = [registers]
        elif isinstance(registers, list) is True:
            self.registers = registers
        else:
            self.registers = []

        # Set active
        self.active = False not in [
            bool(self.registers), bool(self.ip_devices)]

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return (
            '<{0} active={3}, registers={1}, ip_devices={2}>'
            ''.format(
                self.__class__.__name__,
                repr(self.registers), repr(self.ip_devices), repr(self.active)
            )
        )
