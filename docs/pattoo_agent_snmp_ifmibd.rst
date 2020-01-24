
Pattoo SNMP IfMIB Agent For Network Devices
===========================================

``pattoo_agent_snmp_ifmibd`` polls SNMP IfMIB data from SNMP enabled systems and reports it to the ``pattoo`` server.

Installation
------------

These steps outline what needs to be done to get ``pattoo_agent_snmp_ifmibd`` working.

#. Follow the installation steps in the :doc:`installation` file.
#. Configure the ``pattoo.yaml`` configuration file following the steps in :doc:`configuration`. This file tells ``pattoo_agent_snmp_ifmibd``, and all other agents, how to communicate with the ``pattoo`` server.
#. Create a ``pattoo_agent_snmp_ifmibd.yaml`` configuration file. Details on how to do this follow.
#. Start the desired daemons as explained in sections to follow. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.

Setting the  Configuration Directory Location
---------------------------------------------

``pattoo_agent_snmp_ifmibd`` is a standard ``pattoo`` agent and needs its configuration directory defined by using the ``PATTOO_CONFIGDIR`` environmental variable. Here is how to do this from the Linux command line:

.. code-block:: bash

   $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

``pattoo_agent_snmp_ifmibd`` client will read its own ``pattoo_agent_snmp_ifmibd.yaml`` configuration file located this directory when ``PATTOO_CONFIGDIR`` is set.

You can automatically set this variable each time you log in by adding these lines to your ``~/.bash_profile`` file.

.. code-block:: bash

   export PATTOO_CONFIGDIR=/path/to/configuration/directory

Make sure that files in this directory are readable by the user that will be running standard ``pattoo`` agent daemons or scripts.


Configuring ``pattoo_agent_snmp_ifmibd.yaml``
---------------------------------------------

Let's get started on configuring ``pattoo_agent_snmp_ifmibd.yaml``.

``pattoo_agent_snmp_ifmibd`` Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a sample of what should be added. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

   pattoo_agent_snmp_ifmibd:

     polling_interval: 300

     polling_groups:

       - group_name: TEST 1
         ip_devices:
           - ip.address.of.device1
           - ip.address.of.device2
         oids:
           - address: .1.3.6.1.2.1.2.2.1.10
             multiplier: 8
           - address: .1.3.6.1.2.1.2.2.1.16
             multiplier: 8

       - group_name: TEST 2
         ip_devices:
           - ip.address.of.device3
           - ip.address.of.device4
         oids:
           - address: .1.3.6.1.2.1.2.2.1.10
             multiplier: 8
           - address: .1.3.6.1.2.1.2.2.1.16
             multiplier: 8

     auth_groups:

       - group_name: CISCO
         snmp_authpassword: null
         snmp_authprotocol: null
         snmp_community: public
         snmp_port: 161
         snmp_privpassword: null
         snmp_privprotocol: null
         snmp_secname: null
         snmp_version: 2
         ip_devices:
           - ip.address.of.device1
           - ip.address.of.device2

       - group_name: Juniper
         snmp_authpassword: null
         snmp_authprotocol: null
         snmp_community: notpublic
         snmp_port: 161
         snmp_privpassword: null
         snmp_privprotocol: null
         snmp_secname: null
         snmp_version: 2
         ip_devices:
           - ip.address.of.device3
           - ip.address.of.device4


Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Sub-Section
     - Config Options
     - Description
   * - ``pattoo_agent_snmp_ifmibd:``
     -
     -
     -
   * -
     - ``polling_interval``
     -
     - The ``pattoo_agent_snmp_ifmibd`` will report to the ``pattoo`` server every ``polling_interval`` seconds
   * -
     - ``polling_groups:``
     -
     - List of groupings of ``ip_devices`` that need data from a shared set of SNMP OIDs.  Make this the first entry in the configuration sub-section. Make sure it starts with a dash '-' which indicates the beginning of a new grouping.
   * -
     -
     - ``group_name:``
     - Unique name for a group of ``ip_devices`` that share the same SNMP parameters
   * -
     -
     - ``ip_devices:``
     - List of ``ip_devices`` to poll for OID data
   * -
     -
     - ``oids:``
     - OIDs to poll for data from for the ``ip_devices``. Each ``address`` must be an OID. The ``multiplier`` is the value by which the polled data result must be multiplied. This is useful in converting byte values to bits. The default ``multiplier`` is 1.
   * -
     - ``auth_groups:``
     -
     - List of groupings of ``ip_devices`` that share SNMP authentication parameters
   * -
     -
     - ``group_name:``
     - Unique name for a group of ``ip_devices`` that share the same SNMP parameters.  Make this the first entry in the configuration sub-section. Make sure it starts with a dash '-' which indicates the beginning of a new grouping.
   * -
     -
     - ``snmp_authpassword:``
     - SNMPv3 authpassword
   * -
     -
     - ``snmp_authprotocol:``
     - SNMPv3 authprotocol
   * -
     -
     - ``snmp_community:``
     - SNMPv2 community string
   * -
     -
     - ``snmp_port:``
     - SNMP used by ``ip_devices``
   * -
     -
     - ``snmp_privpassword:``
     - SNMPv3 privpassword
   * -
     -
     - ``snmp_privprotocol:``
     - SNMPv3 privprotocol
   * -
     -
     - ``snmp_secname:``
     - SNMPv3 secname
   * -
     -
     - ``snmp_version:``
     - SNMP version
   * -
     -
     - ``ip_devices:``
     - List of ``ip_addresses`` or hostnmae to poll

Polling
-------

Use ``pattoo_agent_snmp_ifmibd`` to poll your devices. The daemon has a simple command structure below.

You will need a ``pattoo_agent_snmp_ifmibd.yaml`` configuration file in the ``PATTOO_CONFIGDIR`` directory before you start.

.. code-block:: bash

   $ bin/pattoo_agent_snmp_ifmibd.py --help
   usage: pattoo_agent_snmp_ifmibd.py [-h] [--start] [--stop] [--status] [--restart]
                            [--force]

   optional arguments:
     -h, --help  show this help message and exit
     --start     Start the agent daemon.
     --stop      Stop the agent daemon.
     --status    Get daemon daemon status.
     --restart   Restart the agent daemon.
     --force     Stops or restarts the agent daemon ungracefully when used with --stop or
                 --restart.
   $

General Operation
^^^^^^^^^^^^^^^^^
Use these commands for general operation of the daemon.

Starting
~~~~~~~~
Start the daemon using this command.

.. code-block:: bash

  $ bin/pattoo_agent_snmp_ifmibd.py --start

Stopping
~~~~~~~~
Stop the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_snmp_ifmibd.py --stop


Restarting
~~~~~~~~~~
Restart the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_snmp_ifmibd.py --restart


Start Polling at Boot
^^^^^^^^^^^^^^^^^^^^^

:doc:`configuration` provides information on how to get the ``pattoo_agent_snmp_ifmibd`` daemon to start at boot.

Troubleshooting
---------------

Troubleshooting steps can be found in the `PattooShared troubleshooting documentation <https://pattoo-shared.readthedocs.io/en/latest/troubleshooting.html>`_
