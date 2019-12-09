#!/usr/bin/env python3
"""Class interacts with targets supporting IfMIB. (32 Bit Counters)."""


from collections import defaultdict

from pattoo_shared.variables import DataPoint
from pattoo_agents.snmp import snmp


class Query(object):
    """Class interacts with targets supporting IfMIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        everything: Returns all needed layer 1 MIB information from the target.
            Keyed by OID's MIB name (primary key), ifIndex (secondary key)

    """

    def __init__(self, snmpvariable):
        """Function for intializing the class.

        Args:
            snmpvariable: SNMPVariable to poll

        Returns:
            None

        """
        # Define query object
        self._query = snmp.SNMP(snmpvariable)

    def everything(self):
        """Get layer 1 data from target using Layer 1 OIDs.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface ifDescr data
        _get_data('ifDescr', self.ifdescr, final)

        # Get interface ifAlias data
        _get_data('ifAlias', self.ifalias, final)

        # Get interface ifName data
        _get_data('ifName', self.ifname, final)

        # Get interface ifAdminStatus data
        _get_data('ifAdminStatus', self.ifadminstatus, final)

        # Get interface ifIndex data
        _get_data('ifIndex', self.ifindex, final)

        # Get interface ifInOctets data
        _get_data('ifInOctets', self.ifinoctets, final)

        # Get interface ifOutOctets data
        _get_data('ifOutOctets', self.ifoutoctets, final)

        # Get interface ifInBroadcastPkts data
        _get_data('ifInBroadcastPkts', self.ifinbroadcastpkts, final)

        # Get interface ifOutBroadcastPkts data
        _get_data('ifOutBroadcastPkts', self.ifoutbroadcastpkts, final)

        # Get interface ifInMulticastPkts data
        _get_data('ifInMulticastPkts', self.ifinmulticastpkts, final)

        # Get interface ifOutMulticastPkts data
        _get_data('ifOutMulticastPkts', self.ifoutmulticastpkts, final)

        # Get interface ifHCOutBroadcastPkts data
        _get_data('ifHCOutBroadcastPkts', self.ifhcoutbroadcastpkts, final)

        # Get interface ifHCOutMulticastPkts data
        _get_data('ifHCOutMulticastPkts', self.ifhcoutmulticastpkts, final)

        # Get interface ifHCOutUcastPkts data
        _get_data('ifHCOutUcastPkts', self.ifhcoutucastpkts, final)

        # Get interface ifHCOutOctets data
        _get_data('ifHCOutOctets', self.ifhcoutoctets, final)

        # Get interface ifHCInBroadcastPkts data
        _get_data('ifHCInBroadcastPkts', self.ifhcinbroadcastpkts, final)

        # Get interface ifHCInMulticastPkts data
        _get_data('ifHCInMulticastPkts', self.ifhcinmulticastpkts, final)

        # Get interface ifHCInUcastPkts data
        _get_data('ifHCInUcastPkts', self.ifhcinucastpkts, final)

        # Get interface ifHCInOctets data
        _get_data('ifHCInOctets', self.ifhcinoctets, final)

        # Return
        return final

    def ifinoctets(self):
        """Return dict of IFMIB ifInOctets for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifInOctets DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.10'
        _result = self._query.walk(oid)
        result = _multiply_octets(_result)
        return result

    def ifoutoctets(self):
        """Return dict of IFMIB ifOutOctets for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifOutOctets DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.16'
        _result = self._query.walk(oid)
        result = _multiply_octets(_result)
        return result

    def ifdescr(self):
        """Return dict of IFMIB ifDescr for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifDescr DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.2'
        result = self._query.walk(oid)
        return result

    def ifalias(self):
        """Return dict of IFMIB ifAlias for each ifIndex for target.

        Args:

        Returns:
            result: List of ifAlias DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.18'
        result = self._query.walk(oid)
        return result

    def ifname(self):
        """Return dict of IFMIB ifName for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifName DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.1'
        result = self._query.walk(oid)
        return result

    def ifindex(self):
        """Return dict of IFMIB ifindex for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifindex DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.1'
        result = self._query.walk(oid)
        return result

    def ifadminstatus(self):
        """Return dict of IFMIB ifAdminStatus for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifAdminStatus DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.2.2.1.7'
        result = self._query.walk(oid)
        return result

    def ifinmulticastpkts(self):
        """Return dict of IFMIB ifInMulticastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifInMulticastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.2'
        result = self._query.walk(oid)
        return result

    def ifoutmulticastpkts(self):
        """Return dict of IFMIB ifOutMulticastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifOutMulticastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.4'
        result = self._query.walk(oid)
        return result

    def ifinbroadcastpkts(self):
        """Return dict of IFMIB ifInBroadcastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifInBroadcastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.3'
        result = self._query.walk(oid)
        return result

    def ifoutbroadcastpkts(self):
        """Return dict of IFMIB ifOutBroadcastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifOutBroadcastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.5'
        result = self._query.walk(oid)
        return result

    def ifhcinucastpkts(self):
        """Return dict of IFMIB ifHCInUcastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifHCInUcastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.7'
        result = self._query.walk(oid)
        return result

    def ifhcoutucastpkts(self):
        """Return dict of IFMIB ifHCOutUcastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifHCOutUcastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.11'
        result = self._query.walk(oid)
        return result

    def ifhcinmulticastpkts(self):
        """Return dict IFMIB ifHCInMulticastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifHCInMulticastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.8'
        result = self._query.walk(oid)
        return result

    def ifhcoutmulticastpkts(self):
        """Return dict IFMIB ifHCOutMulticastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifHCOutMulticastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.12'
        result = self._query.walk(oid)
        return result

    def ifhcinbroadcastpkts(self):
        """Return dict IFMIB ifHCInBroadcastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifHCInBroadcastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.9'
        result = self._query.walk(oid)
        return result

    def ifhcoutbroadcastpkts(self):
        """Return dict IFMIB ifHCOutBroadcastPkts for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifHCOutBroadcastPkts DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.13'
        result = self._query.walk(oid)
        return result

    def ifhcinoctets(self):
        """Return dict of IFMIB ifHCInOctets for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifHCInOctets DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.6'
        _result = self._query.walk(oid)
        result = _multiply_octets(_result)
        return result

    def ifhcoutoctets(self):
        """Return dict of IFMIB ifHCOutOctets for each ifIndex for target.

        Args:
            None

        Returns:
            result: List of ifHCOutOctets DataPoint objects

        """
        # Process OID
        oid = '.1.3.6.1.2.1.31.1.1.1.10'
        _result = self._query.walk(oid)
        result = _multiply_octets(_result)
        return result


def _get_data(title, func, dest):
    """Populate dest with data from the given function.

    Args:
        title: The name of the data
        func: The function which will return the data
        dest: a dict which will store the data

    Returns:
        dest: The modified destination dict

    """
    # Get interface data
    dest[title] = func()
    return dest


def _multiply_octets(datapoints):
    """Multiply datapoint value by 8.

    Args:
        datapoints: List of Datapoint objects to multiply

    Returns:
        result: Datapoint with result multiplied by 8

    """
    # Initialize key variables
    result = []

    # Get interface data
    for datapoint in datapoints:
        new_value = datapoint.value * 8
        result.append(
            DataPoint(datapoint.key, new_value, data_type=datapoint.data_type))
    return result
