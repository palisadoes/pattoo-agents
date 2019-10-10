"""Module used in creating mrtg configuration files for a particular device."""

import sys

# PIP3 imports
import easysnmp
from easysnmp import exceptions

# Import Pattoo libraries
from pattoo import log
from pattoo.snmp import oid as class_oid



class SNMPData(object):
    """Store a SNMP parameters used to interact with an SNMP enabled device."""

    def __init__(self, snmp_params):
        """Initialize the class.

        Args:
            snmp_params: snmp_params dict

        Returns:
            None

        """
        # Initialize key variables
        self.snmp_params = snmp_params
        self.name = snmp_params['name']
        self.device_id = snmp_params['device_id']

        self.datacenter_id = snmp_params['datacenter_id']
        self.device_type = snmp_params['device_type']
        self.ipv4 = snmp_params['ipv4']
        self.ipv6 = snmp_params['ipv6']
        self.snmp_authpassword = snmp_params['snmp_authpassword']
        self.snmp_community = snmp_params['snmp_community']
        self.snmp_port = snmp_params['snmp_port']
        self.snmp_privpassword = snmp_params['snmp_privpassword']
        self.snmp_retries = snmp_params['snmp_retries']
        self.snmp_secname = snmp_params['snmp_secname']
        self.snmp_timeout = snmp_params['snmp_timeout']
        self.snmp_version = snmp_params['snmp_version']


class SNMP(object):
    """Class to interact with devices using SNMP."""

    def __init__(self, snmpdata):
        """Initialize the class.

        Args:
            snmpdata: SNMPData object

        Returns:
            None

        """
        # Initialize key variables
        self.snmpdata = snmpdata

    def device_id(self):
        """Check if device is contactable.

        Args:
            None

        Returns:
            result: Device ID used to instantiate the class

        """
        # Return
        result = self.snmpdata.device_id
        return result

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
        device_name = self.snmpdata.name

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
            log.log2see(1035, log_message)

        except:
            # Not contactable
            _contactable = False

            # Log a message
            log_message = (
                'Unexpected SNMP error for device {}'
                ''.format(device_name))
            log.log2see(1036, log_message)

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
        elif isinstance(result, dict) is True:
            if result[oid_to_get] is None:
                validity = False

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
        elif isinstance(results, dict) is True:
            for _, value in results.items():
                if value is None:
                    validity = False
                    break

        # Return
        return validity

    def walk(
            self, oid_to_get, normalized=False,
            check_reachability=False, check_existence=False, context_name=''):
        """Do an SNMPwalk.

        Args:
            oid_to_get: OID to walk
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
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
            normalized=normalized, context_name=context_name)
        return result

    def get(
            self, oid_to_get, check_reachability=False, check_existence=False,
            normalized=False, context_name=''):
        """Do an SNMPget.

        Args:
            oid_to_get: OID to get
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence:
                Set if checking for the existence of the OID
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
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
            normalized=normalized,
            context_name=context_name)
        if bool(_result) is True:
            result = _result[oid_to_get]
        else:
            result = None
        return result

    def query(
            self, oid_to_get, get=False, check_reachability=False,
            check_existence=False, normalized=False, context_name=''):
        """Do an SNMP query.

        Args:
            oid_to_get: OID to walk
            get: Flag determining whether to do a GET or WALK
            check_reachability:
                Set if testing for connectivity. Some session
                errors are ignored so that a null result is returned
            check_existence:
                Set if checking for the existence of the OID
            normalized: If True, then return results as a dict keyed by
                only the last node of an OID, otherwise return results
                keyed by the entire OID string. Normalization is useful
                when trying to create multidimensional dicts where the
                primary key is a universal value such as IF-MIB::ifIndex
                or BRIDGE-MIB::dot1dBasePort
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
            log.log2die(1449, log_message)

        # Get the SNMP parameters to use for device
        snmp_params = self.snmpdata.snmp_params

        # Create SNMP session
        session = _Session(snmp_params, context_name=context_name).session

        # Create failure log message
        try_log_message = (
            'Error occurred during SNMPget {}, SNMPwalk {} query on {} host '
            'OID {} from {} for context "{}"'
            ''.format(
                get, not get,
                snmp_params['name'],
                oid_to_get, snmp_params['ipv4'],
                context_name))

        # Fill the results object by getting OID data
        try:
            # Get the data
            if get is True:
                results = [session.get(oid_to_get)]

            else:
                if snmp_params['snmp_version'] != 1:
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
                    snmp_params['ipv4']))
            log.log2die(1029, log_message)

        # Format results
        values = _format_results(results, normalized=normalized)

        # Return
        return (_contactable, exists, values)


class _Session(object):
    """Class to create an SNMP session with a device."""

    def __init__(self, snmp_parameters, context_name=''):
        """Initialize the class.

        Args:
            snmp_parameters: Dict of SNMP paramerters
            context_name: Name of context

        Returns:
            session: SNMP session

        """
        # Initialize key variables
        self._context_name = context_name
        self._snmp_params = snmp_parameters

        # Fail if snmp_parameters dictionary is empty
        if snmp_parameters['snmp_version'] is None:
            log_message = (
                'SNMP version is "None". Non existent host? - {}'
                ''.format(snmp_parameters['ipv4']))
            log.log2die(1223, log_message)

        # Fail if snmp_parameters dictionary is empty
        if bool(snmp_parameters) is False:
            log_message = ('SNMP parameters provided are blank. '
                           'Non existent host?')
            log.log2die(1215, log_message)

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
        if self._snmp_params['snmp_version'] != 3:
            session = easysnmp.Session(
                community=self._snmp_params['snmp_community'],
                hostname=self._snmp_params['ipv4'],
                version=self._snmp_params['snmp_version'],
                remote_port=self._snmp_params['snmp_port'],
                use_numeric=True,
                context=self._context_name
            )
        else:
            session = easysnmp.Session(
                hostname=self._snmp_params['ipv4'],
                version=self._snmp_params['snmp_version'],
                remote_port=self._snmp_params['snmp_port'],
                use_numeric=True,
                context=self._context_name,
                security_level=self._security_level(),
                security_username=self._snmp_params['snmp_secname'],
                privacy_protocol=self._priv_protocol(),
                privacy_password=self._snmp_params['snmp_privpassword'],
                auth_protocol=self._auth_protocol(),
                auth_password=self._snmp_params['snmp_authpassword']
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
        # Initialize key variables
        snmp_params = self._snmp_params

        # Determine the security level
        if bool(snmp_params['snmp_authprotocol']) is True:
            if bool(snmp_params['snmp_privprotocol']) is True:
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
        snmp_params = self._snmp_params
        protocol = snmp_params['snmp_authprotocol']

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
        snmp_params = self._snmp_params
        protocol = snmp_params['snmp_privprotocol']

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
    log.log2die(1569, log_message)
    return None


def _format_results(results, normalized=False):
    """Normalize the results of an walk.

    Args:
        results: List of lists of results
        normalized: If True, then return results as a dict keyed by
            only the last node of an OID, otherwise return results
            keyed by the entire OID string. Normalization is useful
            when trying to create multidimensional dicts where the
            primary key is a universal value such as IF-MIB::ifIndex
            or BRIDGE-MIB::dot1dBasePort

    Returns:
        return_results: Dict of results

    """
    # Initialize key variables
    return_results = {}

    for result in results:
        if normalized is True:
            return_results[result.oid_index] = _convert(result)
        else:
            return_results[
                '{}.{}'.format(
                    result.oid, result.oid_index)] = _convert(result)

    # Return
    return return_results


def _convert(result):
    """Convert value from pysnmp object to standard python types.

    Args:
        result: Named tuple result

    Returns:
        _converted: converted value. Only returns BYTES and INTEGERS

    """
    # Initialieze key values
    converted = None
    value = result.value
    snmp_type = result.snmp_type

    # Convert string type values to bytes
    if snmp_type.upper() == 'OCTETSTR':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'OPAQUE':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'BITS':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'IPADDR':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'NETADDR':
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'OBJECTID':
        # DO NOT CHANGE !!!
        # converted = bytes(str(value), 'utf-8')
        converted = bytes(value, 'utf-8')
    elif snmp_type.upper() == 'NOSUCHOBJECT':
        # Nothing if OID not found
        converted = None
    elif snmp_type.upper() == 'NOSUCHINSTANCE':
        # Nothing if OID not found
        converted = None
    elif snmp_type.upper() == 'ENDOFMIBVIEW':
        # Nothing
        converted = None
    elif snmp_type.upper() == 'NULL':
        # Nothing
        converted = None
    else:
        # Convert everything else into integer values
        # rfc1902.Integer
        # rfc1902.Integer32
        # rfc1902.Counter32
        # rfc1902.Gauge32
        # rfc1902.Unsigned32
        # rfc1902.TimeTicks
        # rfc1902.Counter64
        converted = int(value)

    # Convert bytes to string here
    if isinstance(converted, bytes) is True:
        _converted = converted.decode()
    else:
        _converted = converted

    # Return
    return _converted
