
Basic Installation
==================

This section covers some key steps to get you started.

Prerequisites
-------------

There are some software components that need to be installed prior to starting.

#. Install the prerequisite packages for the ``easysnmp`` python pip package. `Instructions can be found here. <https://easysnmp.readthedocs.io/en/latest/>`_
#. ``pattoo`` only runs on Python 3.6 or higher

Let's install the software.

Installation
------------

Follow these steps.

#. Install ``git`` on your system.
#. Select and create the parent directory in which you want to install ``pattoo-agents``.

    .. code-block:: bash

       $ mkdir -p /installation/parent/directory
       $ cd /installation/parent/directory

#. Clone the repository to the parent directory using the ``git clone`` command. You can also choose to downloading and unzip the file in the parent directory. The repository can be found at: https://github.com/PalisadoesFoundation/pattoo-agents

    .. code-block:: bash

       $ cd /installation/parent/directory
       $ git clone https://github.com/PalisadoesFoundation/pattoo-agents.git

#. Enter the ``/installation/parent/directory/pattoo-agents`` directory with the ``pattoo-agents`` files.
#. Install the required packages using the ``pip_requirements`` document in the ``pattoo-agents`` root directory

   .. code-block:: bash

      $ pip3 install -r pip_requirements.txt

#. Populate the mandatory sections of the :doc:`configuration`
#. Follow the configuration steps for each daemon as explained in the :doc:`agent`.

Configuring Agents as systemd Daemons
-------------------------------------

You can also setup all the ``pattoo-agents`` agents as system daemons by executing the ``setup/systemd/bin/install_systemd.py`` script.

You have to specify a ``--config_dir`` defining the configuration file directory.

**Note** The daemons are not enabled or started by default. You will have to do this separately using the ``systemctl`` command after running the script.

.. code-block:: bash

   $ sudo setup/systemd/bin/install_systemd.py --config_dir ~/GitHub/pattoo-agents/etc

   SUCCESS! You are now able to start/stop and enable/disable the following systemd services:

   pattoo_agent_os_spoked.service
   pattoo_agent_snmpd.service
   pattoo_agent_os_autonomousd.service
   pattoo_agent_os_hubd.service

   $
