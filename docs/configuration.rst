
Configuration
=============

After installing your agents, you will need to edit a configuration file in the ``etc/`` directory. Pattoo will read any ``.yaml`` files found in this directory for configuration parameters.

For the sake of simplicity we will assume there is one file called ``etc/config.yaml``.

Make sure you have configured the ``main`` and ``polling`` sections of ``etc/config.yaml`` file before adding any sections for ``pattoo-agent-os`` related daemons.

Custom Directory Location
-------------------------

You can selectively set the location of the configuration directory by using the ``PATTOO_CONFIGDIR`` environmental variable.

This can be useful for:


#. Automated deployments
#. Software developer code testing

By default the ``etc/`` directory of the repository is used for all configuration file searches.

Mandatory Configuration Sections
--------------------------------

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up.

.. code-block:: yaml

   main:
       log_level: debug
       log_directory: ~/GitHub/pattoo-agents/log
       cache_directory: ~/GitHub/pattoo-agents/cache
       daemon_directory: ~/GitHub/pattoo-agents/daemon

   polling:
       polling_interval: 300
       ip_address: 192.168.1.100
       ip_bind_port: 20201

Configuration Explanation
^^^^^^^^^^^^^^^^^^^^^^^^^

This table outlines the purpose of each configuration parameter

.. list-table::
   :header-rows: 1

   * - Section
     - Config Options
     - Description
   * - ``main``
     -
     -
   * -
     - ``log_directory``
     - Path to logging directory. Make sure the username running the daemons have RW access to files there.
   * -
     - ``log_level``
     - Default level of logging. ``debug`` is best for troubleshooting.
   * -
     - ``cache_directory``
     - Directory of unsuccessful data posts to ``pattoo``
   * -
     - ``daemon_directory``
     - Directory used to store daemon related data that needs to be maintained between reboots
   * - ``polling``
     -
     - **Note** The ``polling`` section is not required for ``patoo-os-spoked`` configurations
   * -
     - ``ip_address``
     - IP address of remote ``pattoo`` server
   * -
     - ``ip_bind_port``
     - Port of remote ``pattoo`` server accepting agent data. Default 20201.
   * -
     - ``polling_interval``
     - Interval of data collection and posting in seconds


Agent Configuration
-------------------

You will now need to configure each agent individually. See the :doc:`agent` file for details on how to configure each type of agent.

Notes
-----

Here are some additional tips.


#. You can create a separate configuration file for each section. If you are doing this, make sure there is only one file per agent section. Keep the mandtatory configurations sections in a separate file for simplicity. Practice on a test system before doing this. *Start with a single file first to gain confidence.*
