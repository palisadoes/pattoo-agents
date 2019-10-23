
Pattoo Agent Documentation
==========================

Introduction
------------

``pattoo`` agents can be used to easily poll IoT data. The data is sent to a centralized ``pattoo`` server for processing.

Terminology
-----------

A comprehensive list of ``pattoo`` terminologies ` can be found here. <GLOSSARY.rst>`_

Installation
------------

The documentation in `INSTALLATION.rst <INSTALLATION.rst>`_  covers this.

Configuration
-------------

The documentation in `CONFIGURATION.rst <CONFIGURATION.rst>`_  covers this.

Agents
------

Here is a description of currently supported ``pattoo`` agents.

.. list-table::
   :header-rows: 1

   * - Agent
     - Description
   * - `pattoo-agent-os-spoked <PATTOO-OS.rst>`_
     - Python3 based daemon that presents ``pattoo`` data via a web API URL. This data can be regularly polled from a central server
   * - `pattoo-agent-os-hubd <PATTOO-OS.rst>`_
     - Python3 based daemon that polls ``pattoo-agent-os-spoked`` APIs for data. 
   * - `pattoo-agent-os-autonomousd <PATTOO-OS.rst>`_
     - Python3 based daemon that posts  ``pattoo`` to a central server.
   * - `pattoo-os-snmpd <PATTOO-SNMPD.rst>`_
     - Python3 based daemon that polls remote ``ip_devices`` for SNMP data.


JSON Data Format
----------------

A comprehensive description of ``pattoo`` JSON data ` can be found here. <DATA.rst>`_
