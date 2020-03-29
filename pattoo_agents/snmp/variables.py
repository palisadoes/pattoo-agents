"""Module for classes that format variables."""

# Import pattoo libraries
from pattoo_agents.snmp import oid as class_oid
from pattoo_shared.variables import PollingPoint


class SNMPAuth():
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
            ip_targets: Targets that have these SNMP security parameters

        Returns:
            None

        """
        # Initialize key variables
        self.authprotocol = 'SHA'
        self.privprotocol = 'AES'

        # Set variables
        self.port = int(port)
        self.version = int(version)
        if self.version in [1, 2]:
            self.community = community
            self.secname = None
            self.authprotocol = None
            self.authpassword = None
            self.privprotocol = None
            self.privpassword = None
        else:
            self.community = None
            self.version = 3
            self.secname = secname
            self.authpassword = authpassword
            self.privpassword = privpassword
            if bool(authprotocol) is True and isinstance(
                    authprotocol, str) is True:
                if authprotocol.upper() in ['MD5', 'SHA']:
                    self.authprotocol = authprotocol.upper()
            if bool(privprotocol) is True and isinstance(
                    privprotocol, str) is True:
                if privprotocol.upper() in ['DES', 'AES']:
                    self.privprotocol = privprotocol.upper()

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


class SNMPVariable():
    """Variable representation for data for SNMP polling."""

    def __init__(self, snmpauth=None, ip_target=None):
        """Initialize the class.

        Args:
            snmpauth: SNMPAuth object
            ip_target: Targets for these SNMP security parameters

        Returns:
            None

        """
        # Initialize variables
        self.snmpauth = None
        self.ip_target = None

        # Assign variables
        if isinstance(snmpauth, SNMPAuth) is True:
            self.snmpauth = snmpauth
        if isinstance(ip_target, str) is True:
            self.ip_target = ip_target
        self.valid = False not in [bool(self.snmpauth), bool(self.ip_target)]

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        # Return repr
        return (
            '<{0} snmpauth={1}, ip_target={2}, valid={3}>'
            ''.format(
                self.__class__.__name__,
                repr(self.snmpauth), repr(self.ip_target),
                repr(self.valid)
            )
        )


class SNMPVariableList():
    """Variable representation for data for SNMP polling."""

    def __init__(self, snmpauth=None, ip_targets=None):
        """Initialize the class.

        Args:
            snmpauth: SNMPAuth authentication parameters
            ip_targets: Targets needing snmpauth

        Returns:
            None

        """
        # Initialize variables
        self.snmpvariables = []
        if isinstance(ip_targets, str) is True:
            _ip_targets = [ip_targets]
        elif isinstance(ip_targets, list) is True:
            _ip_targets = ip_targets
        else:
            _ip_targets = []

        # Append to the SNMP list
        for ip_target in _ip_targets:
            snmpvariable = SNMPVariable(
                snmpauth=snmpauth, ip_target=ip_target)
            if snmpvariable.valid is True:
                self.snmpvariables.append(snmpvariable)

        # Determine if.valid
        self.valid = bool(self.snmpvariables)

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
