
Basic Installation
==================

This section covers some key installation and setup steps

Installation
------------

Follow these steps


#. Install the prerequisite packages for the ``easysnmp`` python pip package. `Instructions can be found here. <https://easysnmp.readthedocs.io/en/latest/>`_
#. Install the required packages using the ``pip_requirements`` document in the root directory
   .. code-block::

      $ sudo pip3 install -r pip_requirements.txt

#. Populate the mandatory sections of the `configuration files. <CONFIGURATION.rst>`_
#. Follow the configuration steps for each daemon as explained in the `README.rst <README.rst>`_ file.

Configuring Agents as Syst.rst Daemons
-------------------------------------

You can setup all the ``patoo-agents`` agents as system daemons by executing the ``setup/syst.rst/bin/install_syst.rst.py`` script.

You have to specify a ``--config_dir`` defining the configuration file directory.

After running the script you will be able to start/stop and enable/disable the daemons using the ``systemctl`` command.

**Note** The daemons are not enabled by default.

.. code-block:: bash

   $ sudo setup/syst.rst/bin/install_syst.rst.py --config_dir ~/GitHub/pattoo-agents/etc

   SUCCESS! You are now able to start/stop and enable/disable the following syst.rst services:

   pattoo-agent-os-spoked.service
   pattoo-agent-snmpd.service
   pattoo-agent-os-autonomousd.service
   pattoo-agent-os-hubd.service

   $
