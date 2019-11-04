
Pattoo ModbusTCP Agent
======================

``pattoo-agent-modbustcpd`` provides performance data on any ModbusTCP enabled system it can poll. The data gathered is posted in ``json`` format using HTTP to a remote server.

The ``json`` data is formatted for easy ingestion by `the Pattoo Server <https://pattoo.readthedocs.io/>`_

Installation
------------

Follow these steps.


#. Follow the installation steps in the :doc:`installation` file.
#. Configure the main section of the configuration file following the steps in :doc:`configuration` file.
#. Populate the configuration with the agent specific details listed below
#. Start the desired daemons using the commands below. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.

Usage
-----

``pattoo-agent-modbustcpd`` has a simple command structure.

The daemon will require a configuration file in the ``etc/``\ directory. See the configuration section for details.

.. code-block:: bash

   $ bin/pattoo-agent-modbustcpd.py --help
   usage: pattoo-agent-modbustcpd.py [-h] [--start] [--stop] [--status] [--restart]
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

Configuration
-------------

You will need to edit a configuration file in ``etc/``\ directory. Pattoo will read any ``.json`` files found in this directory for configuration parameters.

For the sake of simplicity we will assume there is one file called ``etc/config.yaml``


#. Make sure you have configured the ``main`` and ``remote_api`` sections of ``etc/config.yaml`` file before adding any sections for ``pattoo-agent-os`` related daemons. The :doc:`configuration` file explains this in detail.
#. After doing this, edit the ``etc/config.yaml`` file to change configuration options specific to the daemons . An explanation follows.

pattoo-agent-modbustcpd Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add the following statements to the ``config.yaml`` file to configure the  ``pattoo-agent-modbustcpd`` daemon. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

  pattoo-agent-modbustcpd:

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
   * - ``pattoo-agent-modbustcpd:``
     -
     -
     - **Note:** Only required for devices running ``pattoo-agent-modbustcpd``
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
