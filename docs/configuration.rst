
Configuration
=============

After installation, you will need to create a configuration file in a directory dedicated to ``pattoo``.

Set the  Configuration Directory Location
-----------------------------------------

You must set the location of the configuration directory by using the ``PATTOO_CONFIGDIR`` environmental variable. Here is how to do this:

.. code-block:: bash

    $ export PATTOO_CONFIGDIR=/path/to/configuration/directory

``pattoo`` will only read the configuration placed in a file named ``pattoo.yaml`` in this directory.

Make sure that files in this directory are readable by the user that will be running ``pattoo`` daemons or scripts.

Copy the Template to Your Configuration Directory
-------------------------------------------------

Copy the template file in the ``examples/etc`` directory to the ``PATTOO_CONFIGDIR`` location.

**NOTE:** If a ``/path/to/configuration/directory/pattoo.yaml`` file already exists in the directory then skip this step and edit the file according to the steps in following sections.

.. code-block:: bash

    $ cp examples/etc/pattoo.yaml.template \
      /path/to/configuration/directory/pattoo.yaml

The next step is to edit the contents of ``pattoo.yaml``

Edit Your Configuration
-----------------------

Take some time to read up on ``YAML`` formatted files if you are not familiar with them. A background knowledge is always helpful.

The ``pattoo.yaml`` file created from the template will have sections that you will need to edit with custom values. Don't worry, these sections are easily identifiable as they all start with ``PATTOO_``

**NOTE:** The indentations in the YAML configuration are important. Make sure indentations line up. Dashes '-' indicate one item in a list of items (if applicable).

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
     -
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
