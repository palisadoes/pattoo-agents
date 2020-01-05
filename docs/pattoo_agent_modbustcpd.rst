
Pattoo ModbusTCP Agent
======================

``pattoo_agent_modbustcpd`` polls data from ModbusTCP enabled systems and reports it to the ``pattoo`` server.

Installation
------------

These steps outline what needs to be done to get ``pattoo_agent_modbustcpd`` working.

#. Follow the installation steps in the :doc:`installation` file.
#. Configure the ``pattoo.yaml`` configuration file following the steps in :doc:`configuration`. This file tells ``pattoo_agent_modbustcpd``, and all other agents, how to communicate with the ``pattoo`` server.
#. Create a ``pattoo_agent_modbustcpd.yaml`` configuration file. Details on how to do this follow.
#. Start the desired daemons as explained in sections to follow. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.

Setting the  Configuration Directory Location
---------------------------------------------

``pattoo_agent_modbustcpd`` is a standard ``pattoo`` agent and needs its configuration directory defined by using the ``PATTOO_CONFIGDIR`` environmental variable. Here is how to do this from the Linux command line:

.. code-block:: bash

   $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

``pattoo_agent_modbustcpd`` client will read its own ``pattoo_agent_modbustcpd.yaml`` configuration file located this directory when ``PATTOO_CONFIGDIR`` is set.

You can automatically set this variable each time you log in by adding these lines to your ``~/.bash_profile`` file.

.. code-block:: bash

   export PATTOO_CONFIGDIR=/path/to/configuration/directory

Make sure that files in this directory are readable by the user that will be running standard ``pattoo`` agent daemons or scripts.


Configuring ``pattoo_agent_modbustcpd.yaml``
--------------------------------------------

Let's get started on configuring ``pattoo_agent_modbustcpd.yaml``.

``pattoo_agent_modbustcpd`` Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is a sample of what should be added. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

  pattoo_agent_modbustcpd:

    polling_groups:

      - group_name: TEST 1
        ip_devices:
          - test1.modbus.tcp.device.net
        input_registers:
          - address: 30123
            multiplier: 1
          - 30789
            multiplier: 1
        holding_registers:
          - address: 40123
            multiplier: 1
          - address: 40456
            multiplier: 1
        unit: 0

      - group_name: TEST 2
        ip_devices:
          - test2.modbus.tcp.device.net
        input_registers:
          - 30387
          - 30388
        holding_registers:
          - 40123
          - 40456
        unit: 0


Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Sub-Section
     - Config Options
     - Description
   * - ``pattoo_agent_modbustcpd:``
     -
     -
     - **Note:** Only required for devices running ``pattoo_agent_modbustcpd``
   * -
     - ``polling_groups:``
     -
     - List of groupings of ``ip_devices`` that need data from a shared set of Modbus registers
   * -
     -
     - ``group_name:``
     - Unique name for a group of ``ip_devices`` that share the same Modbus parameters. Make this the first entry in the configuration sub-section. Make sure it starts with a dash '-' which indicates the beginning of a new grouping.
   * -
     -
     - ``ip_devices:``
     - List of ``ip_devices`` to poll for data
   * -
     -
     - ``input_registers:``
     - List of Modbus input registers that we need data from for the ``ip_devices``. Each ``address`` must be an OID. The ``multiplier`` is the value by which the polled data result must be multiplied. The default ``multiplier`` is 1.
   * -
     -
     - ``holding_registers:``
     - List of Modbus holding registers that we need data from for the ``ip_devices``. Each ``address`` must be an OID. The ``multiplier`` is the value by which the polled data result must be multiplied. The default ``multiplier`` is 1.
   * -
     - ``unit:``
     -
     - Modbus unit number to poll. If not present or blank, the default is '0'

Polling
-------

Use ``pattoo_agent_modbustcpd`` to poll your devices. The daemon has a simple command structure below.

You will need a ``pattoo_agent_modbustcpd.yaml`` configuration file in the ``PATTOO_CONFIGDIR`` directory before you start.

.. code-block:: bash

   $ bin/pattoo_agent_modbustcpd.py --help
   usage: pattoo_agent_modbustcpd.py [-h] [--start] [--stop] [--status] [--restart]
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

  $ bin/pattoo_agent_modbustcpd.py --start

Stopping
~~~~~~~~
Stop the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_modbustcpd.py --stop


Restarting
~~~~~~~~~~
Restart the daemon using this command.

.. code-block:: bash

    $ bin/pattoo_agent_modbustcpd.py --restart


Start Polling at Boot
^^^^^^^^^^^^^^^^^^^^^

:doc:`configuration` provides information on how to get the ``pattoo_agent_modbustcpd`` daemon to start at boot.

Troubleshooting
---------------

Troubleshooting steps can be found in the `PattooShared troubleshooting documentation <https://pattoo-shared.readthedocs.io/en/latest/troubleshooting.html>`_
