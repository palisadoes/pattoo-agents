"""Module for classes that format variables."""


class SNMPAuth(object):
    """Variable representation for data for SNMP polling."""

    def __init__(self, version=2, community='public', port=161,
                 secname=None,
                 authprotocol=None, authpassword=None,
                 privprotocol=None, privpassword=None):
        """Initialize the class.

        Args:
            version: SNMP version
            community: SNMP community
            port: SNMP port
            secname: SNMP secname
            authprotocol: SNMP authprotocol
            authpassword: SNMP authpassword
            privprotocol: SNMP privprotocol
            privpassword: SNMP privpassword
            ip_devices: Devices that have these SNMP security parameters

        Returns:
            None

        """
        # Initialize variables
        self.version = int(version)
        self.community = community
        self.port = int(port)
        self.secname = secname
        self.authprotocol = authprotocol
        self.authpassword = authpassword
        self.privprotocol = privprotocol
        self.privpassword = privpassword

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return (
            '<{0} version={2}, community={3}, port={8}, secname={4}, '
            'authprotocol={1} authpassword={5}, '
            'privpassword={6}, privprotocol={7}>'
            ''.format(
                self.__class__.__name__,
                repr(self.authprotocol), repr(self.version),
                repr(self.community), repr(self.secname),
                repr(self.authpassword), repr(self.privpassword),
                repr(self.privprotocol), repr(self.port)
            )
        )


class SNMPVariable(object):
    """Variable representation for data for SNMP polling."""

    def __init__(self, version=2, community='public', port=161,
                 secname=None,
                 authprotocol=None, authpassword=None,
                 privprotocol=None, privpassword=None,
                 ip_device=None):
        """Initialize the class.

        Args:
            version: SNMP version
            community: SNMP community
            port: SNMP port
            secname: SNMP secname
            authprotocol: SNMP authprotocol
            authpassword: SNMP authpassword
            privprotocol: SNMP privprotocol
            privpassword: SNMP privpassword
            ip_device: Devices for these SNMP security parameters

        Returns:
            None

        """
        # Initialize variables
        self.version = int(version)
        self.community = community
        self.port = int(port)
        self.secname = secname
        self.authprotocol = authprotocol
        self.authpassword = authpassword
        self.privprotocol = privprotocol
        self.privpassword = privpassword
        self.ip_device = ip_device

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return (
            '<{0} version={2}, community={3}, port={8}, secname={4}, '
            'authprotocol={1} authpassword={5}, '
            'privpassword={6}, privprotocol={7}, '
            'ip_device={9}>'
            ''.format(
                self.__class__.__name__,
                repr(self.authprotocol), repr(self.version),
                repr(self.community), repr(self.secname),
                repr(self.authpassword), repr(self.privpassword),
                repr(self.privprotocol), repr(self.port),
                repr(self.ip_device)
            )
        )


class SNMPVariableList(object):
    """Variable representation for data for SNMP polling."""

    def __init__(self, snmpauth=None, ip_devices=None):
        """Initialize the class.

        Args:
            snmpauth: SNMPAuth authentication parameters
            ip_devices: Devices needing snmpauth

        Returns:
            None

        """
        # Initialize variables
        self.snmpvariables = []
        if isinstance(snmpauth, SNMPAuth) is False:
            # Die
            pass
        if isinstance(ip_devices, str) is True:
            _ip_devices = [ip_devices]
        elif isinstance(ip_devices, list) is True:
            _ip_devices = ip_devices
        else:
            _ip_devices = []

        # Append to the SNMP list
        for ip_device in _ip_devices:
            snmpvariable = SNMPVariable(
                version=snmpauth.version,
                community=snmpauth.community,
                port=snmpauth.port,
                authprotocol=snmpauth.authprotocol,
                authpassword=snmpauth.authpassword,
                secname=snmpauth.secname,
                privprotocol=snmpauth.privprotocol,
                privpassword=snmpauth.privpassword,
                ip_device=ip_device)
            self.snmpvariables.append(snmpvariable)

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation

        """
        # Return repr
        return (
            '<{0} snmpvariables={1}>'
            ''.format(
                self.__class__.__name__,
                repr(self.snmpvariables)
            )
        )


class OIDVariable(object):
    """Variable representation for OID data for SNMP polling."""

    def __init__(self, oids=None, ip_devices=None):
        """Initialize the class.

        Args:
            oids: SNMP oids
            ip_devices: Devices that require data from oids

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

        # Initialize oids
        if isinstance(oids, str) is True:
            self.oids = [oids]
        elif isinstance(oids, list) is True:
            self.oids = oids
        else:
            self.oids = []

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return (
            '<{0} oids={1}, ip_devices={2}>'
            ''.format(
                self.__class__.__name__,
                repr(self.oids), repr(self.ip_devices)
            )
        )


def _strip_non_printable(value):
    """Strip non printable characters.

    Removes any non-printable characters and adds an indicator to the string
    when binary characters are found.

    Args:
        value: the value that you wish to strip

    Returns:
        printable_value: Printable string

    """
    # Initialize key variables
    printable_value = ''

    if isinstance(value, str) is False:
        printable_value = value
    else:
        # Filter all non-printable characters
        # (note that we must use join to account for the fact that Python 3
        # returns a generator)
        printable_value = ''.join(
            [x for x in value if x.isprintable() is True])
        if printable_value != value:
            if bool(printable_value) is True:
                printable_value = '{} '.format(printable_value)
            printable_value = '{}(contains binary)'.format(printable_value)

    # Return
    return printable_value
