"""Module used polling SNMP enabled devices."""

import sys

# PIP3 imports
import easysnmp
from easysnmp import exceptions

# Import Pattoo libraries
from pattoo_shared import log
from pattoo_shared.variables import DataVariable
from pattoo_shared.constants import (
    DATA_INT, DATA_COUNT64, DATA_COUNT, DATA_STRING, DATA_NONE)
from pattoo_agents.agents.snmp import oid as class_oid
from pattoo_agents.agents.snmp.variables import SNMPVariable


class SNMP(object):
    """Class to interact with devices using SNMP."""

    def __init__(self, snmpvariable):
        """Initialize the class.

        Args:
            snmpvariable: SNMPVariable object

        Returns:
            None

        """
        # Initialize key variables
        self._snmp_ip_device = snmpvariable.ip_device
        self._snmp_version = snmpvariable.snmpauth.version
        self._snmpvariable = snmpvariable

    def contactable(self):
        """Check if device is contactable.

        Args:
            device_id: Device ID

        Returns:
            _contactable: True if a contactable

        """
        # Define key variables
        _contactable = False
        result = None

        # Get device data
        device_name = self._snmp_ip_device

        # Try to reach device
        try:
            # If we can poll the SNMP sysObjectID,
            # then the device is contactable
            result = self.sysobjectid(check_reachability=True)
            if bool(result) is True:
                _contactable = True

        except Exception as exception_error:
            # Not contactable
            _contactable = False

            # Log a message
            log_message = ('''\
Unable to access device {} via SNMP. Make sure device is contactable and \
that the database\'s SNMP parameters for the device are correct. Fix, repeat \
your command AND make sure you set ---active=True. Error: {}\
'''.format(device_name, exception_error))
            log.log2see(51035, log_message)

        except:
            # Not contactable
            _contactable = False

            # Log a message
            log_message = (
                'Unexpected SNMP error for device {}'
                ''.format(device_name))
            log.log2see(51036, log_message)

        # Return
        return _contactable

    def sysobjectid(self, check_reachability=False):
        """Get the sysObjectID of the device.

        Args:
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
        Returns:
            object_id: sysObjectID value

        """
        # Initialize key variables
        oid = '.1.3.6.1.2.1.1.2.0'
        object_id = None

        # Get sysObjectID
        results = self.get(oid, check_reachability=check_reachability)
        if bool(results) is True:
            object_id = results

        # Return
        return object_id

    def oid_exists(self, oid_to_get, context_name=''):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exists

        """
        # Initialize key variables
        validity = False

        # Process
        (_, validity, result) = self.query(
            oid_to_get,
            get=True,
            check_reachability=True, context_name=context_name,
            check_existence=True)

        # If we get no result, then override validity
        if bool(result) is False:
            validity = False
        else:
            validity = True

        # Return
        return validity

    def branch_exists(self, oid_to_get, context_name=''):
        """Determine existence of OID on device.

        Args:
            oid_to_get: OID to get
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            validity: True if exists

        """
        # Initialize key variables
        validity = False

        # Process
        (_, validity, results) = self.query(
            oid_to_get, get=False,
            check_reachability=True,
            context_name=context_name,
            check_existence=True)

        # If we get no result, then override validity
        if bool(results) is False:
            validity = False
        else:
            validity = True

        # Return
        return validity

    def walk(
            self, oid_to_get, check_reachability=False,
            check_existence=False, context_name=''):
        """Do an SNMPwalk.

        Args:
            oid_to_get: OID to walk
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence:
                Set if checking for the existence of the OID
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            result: Dictionary of tuples (OID, value)

        """
        (_, _, result) = self.query(
            oid_to_get, get=False,
            check_reachability=check_reachability,
            check_existence=check_existence,
            context_name=context_name)
        return result

    def get(
            self, oid_to_get, check_reachability=False,
            check_existence=False, context_name=''):
        """Do an SNMPget.

        Args:
            oid_to_get: OID to get
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence:
                Set if checking for the existence of the OID
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            Dictionary of tuples (OID, value)

        """
        (_, _, _result) = self.query(
            oid_to_get, get=True,
            check_reachability=check_reachability,
            check_existence=check_existence,
            context_name=context_name)
        if bool(_result) is True:
            result = _result
        else:
            result = None
        return result

    def query(
            self, oid_to_get, get=False, check_reachability=False,
            check_existence=False, context_name=''):
        """Do an SNMP query.

        Args:
            oid_to_get: OID to walk
            get: Flag determining whether to do a GET or WALK
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence:
                Set if checking for the existence of the OID
            context_name: Set the contextName used for SNMPv3 messages.
                The default contextName is the empty string "".  Overrides the
                defContext token in the snmp.conf file.

        Returns:
            Dictionary of tuples (OID, value)

        """
        # Initialize variables
        _contactable = True
        exists = True
        results = []

        # Create OID string object
        oid_string = class_oid.OIDstring(oid_to_get)

        # Check if OID is valid
        valid_format = oid_string.valid_format()
        if valid_format is False:
            log_message = ('OID {} has an invalid format'.format(oid_to_get))
            log.log2die(51449, log_message)

        # Create SNMP session
        session = _Session(
            self._snmpvariable, context_name=context_name).session

        # Create failure log message
        try_log_message = (
            'Error occurred during SNMPget {}, SNMPwalk {} query against '
            'device {} OID {} for context "{}"'
            ''.format(
                get, not get, self._snmp_ip_device,
                oid_to_get, context_name))

        # Fill the results object by getting OID data
        try:
            # Get the data
            if get is True:
                results = [session.get(oid_to_get)]

            else:
                if self._snmp_version != 1:
                    # Bulkwalk for SNMPv2 and SNMPv3
                    results = session.bulkwalk(
                        oid_to_get, non_repeaters=0, max_repetitions=25)
                else:
                    # Bulkwalk not supported in SNMPv1
                    results = session.walk(oid_to_get)

        # Crash on error, return blank results if doing certain types of
        # connectivity checks
        except (
                exceptions.EasySNMPConnectionError,
                exceptions.EasySNMPTimeoutError,
                exceptions.EasySNMPUnknownObjectIDError,
                exceptions.EasySNMPNoSuchNameError,
                exceptions.EasySNMPNoSuchObjectError,
                exceptions.EasySNMPNoSuchInstanceError,
                exceptions.EasySNMPUndeterminedTypeError) as exception_error:

            # Update the error message
            try_log_message = ("""\
{}: [{}, {}, {}]""".format(try_log_message, sys.exc_info()[0],
                           sys.exc_info()[1], sys.exc_info()[2]))

            # Process easysnmp errors
            (_contactable, exists) = _process_error(
                try_log_message, exception_error,
                check_reachability, check_existence)

        except SystemError as exception_error:
            # Update the error message
            try_log_message = ("""\
{}: [{}, {}, {}]""".format(try_log_message, sys.exc_info()[0],
                           sys.exc_info()[1], sys.exc_info()[2]))

            # Process easysnmp errors
            (_contactable, exists) = _process_error(
                try_log_message, exception_error,
                check_reachability, check_existence, system_error=True)

        except:
            log_message = (
                'Unexpected error: {}, {}, {}, {}'
                ''.format(
                    sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2],
                    self._snmp_ip_device))
            log.log2die(51029, log_message)

        # Format results
        values = _convert_results(results)

        # Return
        return (_contactable, exists, values)


class _Session(object):
    """Class to create an SNMP session with a device."""

    def __init__(self, snmpvariable, context_name=''):
        """Initialize the class.

        Args:
            snmpvariable: SNMPVariable object
            context_name: Name of context

        Returns:
            session: SNMP session

        """
        # Initialize key variables
        self._context_name = context_name
        self._snmp_ip_device = snmpvariable.ip_device
        self._snmp_port = snmpvariable.snmpauth.port
        self._snmp_version = snmpvariable.snmpauth.version
        self._snmp_community = snmpvariable.snmpauth.community
        self._snmp_secname = snmpvariable.snmpauth.secname
        self._snmp_authprotocol = snmpvariable.snmpauth.authprotocol
        self._snmp_authpassword = snmpvariable.snmpauth.authpassword
        self._snmp_privprotocol = snmpvariable.snmpauth.privprotocol
        self._snmp_privpassword = snmpvariable.snmpauth.privpassword

        # Fail if snmpvariable dictionary is empty
        if self._snmp_version is None:
            log_message = (
                'SNMP version is "None". Non existent host? - {}'
                ''.format(self._snmp_ip_device))
            log.log2die(51223, log_message)

        # Fail if snmpvariable dictionary is empty
        if bool(snmpvariable) is False:
            log_message = ('SNMP parameters provided are blank. '
                           'Non existent host?')
            log.log2die(51215, log_message)

        # Fail if invalid snmpvariable
        if isinstance(snmpvariable, SNMPVariable) is False:
            log_message = ('Invalid SNMPVariable parameters')
            log.log2die(51216, log_message)

        # Create SNMP session
        self.session = self._session()

    def _session(self):
        """Create an SNMP session for queries.

        Args:
            None

        Returns:
            session: SNMP session

        """
        # Create session
        if self._snmp_version != 3:
            session = easysnmp.Session(
                community=self._snmp_community,
                hostname=self._snmp_ip_device,
                version=self._snmp_version,
                remote_port=self._snmp_port,
                use_numeric=True,
                context=self._context_name
            )
        else:
            session = easysnmp.Session(
                hostname=self._snmp_ip_device,
                version=self._snmp_version,
                remote_port=self._snmp_port,
                use_numeric=True,
                context=self._context_name,
                security_level=self._security_level(),
                security_username=self._snmp_secname,
                privacy_protocol=self._priv_protocol(),
                privacy_password=self._snmp_privpassword,
                auth_protocol=self._auth_protocol(),
                auth_password=self._snmp_authpassword
            )

        # Return
        return session

    def _security_level(self):
        """Create string for security level.

        Args:
            snmp_params: Dict of SNMP paramerters

        Returns:
            result: security level

        """
        # Determine the security level
        if bool(self._snmp_authprotocol) is True:
            if bool(self._snmp_privprotocol) is True:
                result = 'authPriv'
            else:
                result = 'authNoPriv'
        else:
            result = 'noAuthNoPriv'

        # Return
        return result

    def _auth_protocol(self):
        """Get AuthProtocol to use.

        Args:
            snmp_params: Dict of SNMP paramerters

        Returns:
            result: Protocol to be used in session

        """
        # Initialize key variables
        protocol = self._snmp_authprotocol

        # Setup AuthProtocol (Default SHA)
        if bool(protocol) is False:
            result = 'DEFAULT'
        else:
            if protocol.lower() == 'md5':
                result = 'MD5'
            else:
                result = 'SHA'

        # Return
        return result

    def _priv_protocol(self):
        """Get privProtocol to use.

        Args:
            snmp_params: Dict of SNMP paramerters

        Returns:
            result: Protocol to be used in session

        """
        # Initialize key variables
        protocol = self._snmp_privprotocol

        # Setup privProtocol (Default AES256)
        if bool(protocol) is False:
            result = 'DEFAULT'
        else:
            if protocol.lower() == 'des':
                result = 'DES'
            else:
                result = 'AES'

        # Return
        return result


def _process_error(
        log_message, exception_error, check_reachability,
        check_existence, system_error=False):
    """Process the SNMP error.

    Args:
        params_dict: Dict of SNMP parameters to try

    Returns:
        alive: True if contactable

    """
    # Initialize key varialbes
    _contactable = True
    exists = True
    if system_error is False:
        error_name = 'EasySNMPError'
    else:
        error_name = 'SystemError'

    # Check existence of OID
    if check_existence is True:
        if system_error is False:
            if isinstance(
                    exception_error,
                    easysnmp.exceptions.EasySNMPUnknownObjectIDError) is True:
                exists = False
                return (_contactable, exists)
            elif isinstance(
                    exception_error,
                    easysnmp.exceptions.EasySNMPNoSuchNameError) is True:
                exists = False
                return (_contactable, exists)
            elif isinstance(
                    exception_error,
                    easysnmp.exceptions.EasySNMPNoSuchObjectError) is True:
                exists = False
                return (_contactable, exists)
            elif isinstance(
                    exception_error,
                    easysnmp.exceptions.EasySNMPNoSuchInstanceError) is True:
                exists = False
                return (_contactable, exists)
        else:
            exists = False
            return (_contactable, exists)

    # Checking if the device is reachable
    if check_reachability is True:
        _contactable = False
        exists = False
        return (_contactable, exists)

    # Die an agonizing death!
    log_message = ('{}: {}'.format(error_name, log_message))
    log.log2die(51569, log_message)
    return None


def _convert_results(inbound):
    """Convert results from easysnmp.variables.SNMPVariable to DataVariable.

    Args:
        inbound: SNMP query result as list of easysnmp.variables.SNMPVariable

    Returns:
        outbound: DataVariable formatted equivalent

    """
    # Initialize key variables
    outbound = []

    # Format the results to DataVariable format
    for item in inbound:
        # Initialize loop variables
        converted = None
        snmp_type = item.snmp_type
        data_type = DATA_INT

        # Convert string type values to bytes
        if snmp_type.upper() == 'OCTETSTR':
            converted = item.value
            data_type = DATA_STRING
        elif snmp_type.upper() == 'OPAQUE':
            converted = item.value
            data_type = DATA_STRING
        elif snmp_type.upper() == 'BITS':
            converted = item.value
            data_type = DATA_STRING
        elif snmp_type.upper() == 'IPADDR':
            converted = item.value
            data_type = DATA_STRING
        elif snmp_type.upper() == 'NETADDR':
            converted = item.value
            data_type = DATA_STRING
        elif snmp_type.upper() == 'OBJECTID':
            # DO NOT CHANGE !!!
            # converted = bytes(str(value), 'utf-8')
            converted = item.value
            data_type = DATA_STRING
        elif snmp_type.upper() == 'NOSUCHOBJECT':
            # Nothing if OID not found
            converted = None
            data_type = DATA_NONE
        elif snmp_type.upper() == 'NOSUCHINSTANCE':
            # Nothing if OID not found
            converted = None
            data_type = DATA_NONE
        elif snmp_type.upper() == 'ENDOFMIBVIEW':
            # Nothing
            converted = None
            data_type = DATA_NONE
        elif snmp_type.upper() == 'NULL':
            # Nothing
            converted = None
            data_type = DATA_NONE
        elif snmp_type.upper() == 'COUNTER':
            # Numeric values
            converted = int(item.value)
            data_type = DATA_COUNT
        elif snmp_type.upper() == 'COUNTER64':
            # Numeric values
            converted = int(item.value)
            data_type = DATA_COUNT64
        else:
            # Convert everything else into integer values
            # rfc1902.Integer
            # rfc1902.Integer32
            # rfc1902.Gauge32
            # rfc1902.Unsigned32
            # rfc1902.TimeTicks
            converted = int(item.value)

        # Convert result to DataVariable
        datavariable = DataVariable(
            value=converted,
            data_label=item.oid,
            data_index=item.oid_index,
            data_type=data_type
        )
        # Append to outbound result
        outbound.append(datavariable)

    # Return
    return outbound
