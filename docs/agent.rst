
Agent Documentation
===================

Here is a description of currently supported ``pattoo`` agents.

.. list-table::
   :header-rows: 1

   * - Agent
     - Description
     - Documenatation
     * - ``pattoo-agent-modbustcpd``
       - Python3 based daemon that polls remote ``ip_devices`` for Modbus data over TCP.
       - Documentation can be found here. :doc:`pattoo-agent-modbustcpd`
   * - ``pattoo-agent-os-spoked``
     - Python3 based daemon that presents ``pattoo`` data via a web API URL. This data can be regularly polled from a central server
     - Documentation can be found here. :doc:`pattoo-agent-os`
   * - ``pattoo-agent-os-hubd``
     - Python3 based daemon that polls ``pattoo-agent-os-spoked`` APIs for data.
     - Documentation can be found here. :doc:`pattoo-agent-os`
   * - ``pattoo-agent-os-autonomousd``
     - Python3 based daemon that posts  ``pattoo`` to a central server.
     - Documentation can be found here. :doc:`pattoo-agent-os`
   * - ``pattoo-agent-snmpd``
     - Python3 based daemon that polls remote ``ip_devices`` for SNMP data.
     - Documentation can be found here. :doc:`pattoo-agent-snmpd`
