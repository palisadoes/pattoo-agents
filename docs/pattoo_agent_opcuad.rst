
Pattoo OPC UA Agents
====================

``pattoo_agent_opcuad`` polls ``Analog Value`` data from OPC UA enabled systems and reports it to the ``pattoo`` server.

Installation
------------

These steps outline what needs to be done to get ``pattoo_agent_opcuad`` working.

#. Follow the installation steps in the :doc:`installation` file.
#. Configure the ``pattoo.yaml`` configuration file following the steps in :doc:`configuration`. This file tells ``pattoo_agent_opcuad``, and all other agents, how to communicate with the ``pattoo`` server.
#. Create a ``pattoo_agent_opcuad.yaml`` configuration file. Details on how to do this follow.
#. Start the desired daemons as explained in sections to follow. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.

Setting the  Configuration Directory Location
---------------------------------------------

``pattoo_agent_opcuad`` is a standard ``pattoo`` agent and needs its configuration directory defined by using the ``PATTOO_CONFIGDIR`` environmental variable. Here is how to do this from the Linux command line:

.. code-block:: bash

   $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

``pattoo_agent_opcuad`` client will read its own ``pattoo_agent_opcuad.yaml`` configuration file located this directory when ``PATTOO_CONFIGDIR`` is set.

You can automatically set this variable each time you log in by adding these lines to your ``~/.bash_profile`` file.

.. code-block:: bash

   export PATTOO_CONFIGDIR=/path/to/configuration/directory

Make sure that files in this directory are readable by the user that will be running standard ``pattoo`` agent daemons or scripts.


Configuring ``pattoo_agent_opcuad.yaml``
-------------------------------------------

Let's get started on configuring ``pattoo_agent_opcuad.yaml``.

``pattoo_agent_opcuad`` Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a sample of what should be added. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

   pattoo_agent_opcuad:

     polling_interval: 300

     polling_groups:

       - group_name: GROUP 1
         ip_target: server-01.opcua.net
         ip_port: 4840
         username: opcua_username
         password: opcua_password
         nodes:
           - address: ns=1;s=[OPCUA_SERVER_1]DischargehAirTemp.PV

       - group_name: GROUP 2
         ip_target: server-02.opcua.net
         ip_port: 4840
         username: opcua_username
         password: opcua_password
         nodes:
           - address: ns=1;s=[OPCUA_SERVER_2]DischargehAirTemp.PV


Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Sub-Section
     - Config Options
     - Description
   * - ``pattoo_agent_opcuad:``
     -
     -
     -
   * -
     - ``polling_interval``
     -
     - The ``pattoo_agent_opcuad`` will report to the ``pattoo`` server every ``polling_interval`` seconds
   * -
     - ``polling_groups:``
     -
     - List of groupings of ``ip_devices`` that need data from a shared set of OPC UA nodes. Make this the first entry in the configuration sub-section. Make sure it starts with a dash '-' which indicates the beginning of a new grouping.
   * -
     -
     - ``group_name:``
     - Unique name for the set of parameters required to poll an OPC UA ``ip_device``
   * -
     -
     - ``ip_device:``
     - The ``ip_device`` to poll for data
   * -
     -
     - ``ip_port:``
     - The ``ip_port`` on which the ``ip_device`` is listening for data
   * -
     -
     - ``username:``
     - The OPC UA ``username`` to use when querying the ``ip_device``
   * -
     -
     - ``password:``
     - The OPC UA ``password`` to use when querying the ``ip_device``
   * -
     -
     - ``nodes:``
     - OPC UA ``Analog Value`` node to poll for data from for the ``ip_devices``. Each ``address`` must be a OPC UA node. The ``multiplier`` is the value by which the polled data result must be multiplied. This is useful in converting byte values to bits. The default ``multiplier`` is 1.


Polling
-------

Use ``pattoo_agent_opcuad`` to poll your devices. The daemon has a simple command structure below.

You will need a ``pattoo_agent_opcuad.yaml`` configuration file in the ``PATTOO_CONFIGDIR`` directory before you start.

.. code-block:: bash

   $ bin/pattoo_agent_opcuad.py --help
   usage: pattoo_agent_opcuad.py [-h] [--start] [--stop] [--status] [--restart]
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

  $ bin/pattoo_agent_opcuad.py --start

Stopping
~~~~~~~~
Stop the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_opcuad.py --stop


Restarting
~~~~~~~~~~
Restart the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_opcuad.py --restart


Start Polling at Boot
^^^^^^^^^^^^^^^^^^^^^

:doc:`configuration` provides information on how to get the ``pattoo_agent_opcuad`` daemon to start at boot.

Troubleshooting
---------------

Troubleshooting steps can be found in the `PattooShared troubleshooting documentation <https://pattoo-shared.readthedocs.io/en/latest/troubleshooting.html>`_
