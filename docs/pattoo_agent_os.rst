
Pattoo Operating System Agents
==============================

``pattoo_agent_os`` daemons provide performance data on any Linux system it runs on. The data is presented in ``json`` format and can either be posted using HTTP to a remote server or viewed on the server on which it runs by visiting a well known URL.

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

``pattoo_agent_os`` contains multiple daemons.


#. ``pattoo_agent_os_autonomousd.py`` which will post ``linux`` system data in ``json`` format to a remote ``pattoo`` server
#. ``pattoo_agent_os_spoked.py`` which will make the same ``linux`` system data in ``json`` format available for viewing on the local server. This allows the server to be polled for data from remote servers running  ``pattoo_agent_os_hubd`` software agents.
#. ``pattoo_agent_os_hubd.py`` which polls ``pattoo_agent_os_spoked`` enables devices for data to be posted to the ``pattoo`` server.

The daemons will require a configuration file in the ``etc/``\ directory. See the configuration section for details.

.. code-block:: bash

   $ bin/pattoo_agent_os_autonomousd.py --help
   usage: pattoo_agent_os_autonomousd.py [-h] [--start] [--stop] [--status] [--restart]
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

.. code-block:: bash

   $ bin/pattoo_agent_os_spoked.py --help
   usage: pattoo_agent_os_spoked.py [-h] [--start] [--stop] [--status] [--restart]
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

.. code-block:: bash

   $ bin/pattoo_agent_os_hubd.py --help
   usage: pattoo_agent_os_hubd.py [-h] [--start] [--stop] [--status] [--restart]
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

Pattoo-OS Agent Configuration
-----------------------------

You will need to edit a configuration file in ``etc/``\ directory. Pattoo will read any ``.json`` files found in this directory for configuration parameters.

For the sake of simplicity we will assume there is one file called ``etc/config.yaml``


#. Make sure you have configured the ``main`` and ``remote_api`` sections of ``etc/config.yaml`` file before adding any sections for ``pattoo_agent_os`` related daemons. The :doc:`configuration` file explains this in detail.
#. After doing this, edit the ``etc/config.yaml`` file to change configuration options specific to the daemons . An explanation follows.

pattoo_agent_os_hubd Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add the following statements to the ``config.yaml`` file to configure the  ``pattoo_agent_os_hubd`` daemon. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

   pattoo_agent_os_hubd:
       ip_devices:
         - ip_address: 127.0.0.1
           ip_bind_port: 5000
         - ip_address: 127.0.0.2
           ip_bind_port: 5000

Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Sub-Section
     - Config Options
     - Description
   * - ``pattoo_agent_os_hubd``
     -
     -
     - **Note:** Only required for devices running ``pattoo_agent_os_hubd``
   * -
     - ``ip_devices``
     -
     - Sub-Section providing a list of IP addresses or hostnames running ``pattoo_agent_os_spoked`` that need to be polled for data. You must specify an ``ip_address`` and TCP ``ip_bind_port``\ for each of these devices.
   * -
     -
     - ``ip_address``
     - The IP adrress of the remote ``ip_device``.
   * -
     -
     - ``bind_port``
     - The TCP port on which the remote ``ip_device`` is listening.


pattoo_agent_os_spoked Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add the following statements to the ``config.yaml`` file to configure the  ``pattoo_agent_os_spoked`` daemon. An explanation follows.

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items.

.. code-block:: yaml

   pattoo_agent_os_spoked:
       ip_listen_address: 0.0.0.0
       ip_bind_port: 5000

Configuration Explanation
~~~~~~~~~~~~~~~~~~~~~~~~~

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Config Options
     - Description
   * - ``pattoo_agent_os_spoked``
     -
     - **Note:** Only required for devices running ``pattoo_agent_os_spoked``
   * -
     - ``ip_listen_address``
     - IP address on which the API server will listen. Setting this to ``0.0.0.0`` will make it listen on all IPv4 addresses. Setting to ``"0::"`` will make it listen on all IPv6 configured interfaces. It will not listen on IPv4 and IPv6 addresses simultaneously. You must **quote** all IPv6 addresses. The default value is ``0.0.0.0``
   * -
     - ``ip_bind_port``
     - TCP port on which the API will listen


pattoo_agent_os_autonomousd Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is no ``pattoo_agent_os_autonomousd`` section. The parameters in the ``main`` and ``remote_api`` sections is sufficient.

Testing
-------

If you are running ``pattoo_agent_os_spoked`` on your local system, then you can test it by pointing your browser to ``http://localhost:5000/pattoo_agent_os`` to view the system data.