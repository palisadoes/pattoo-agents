# Basic Installation

This section covers some key installation and setup steps

## Installation
Follow these steps

1. Install the prerequisite packages for the `easysnmp` python pip package. [Instructions can be found here.](https://easysnmp.readthedocs.io/en/latest/)
1. Install the required packages using the `pip_requirements` document in the root directory
```
$ sudo pip3 install -r pip_requirements.txt
```
1. Populate the mandatory sections of the [configuration files.](CONFIGURATION.md)
1. Follow the configuration steps for each daemon as explained in the [README.md](README.md) file.


## Configuring Agents as Systemd Daemons

You can setup all the `patoo-agents` agents as system daemons by executing the `setup/systemd/bin/install_systemd.py` script.

You have to specify a `--config_dir` defining the configuration file directory.

After running the script you will be able to start/stop and enable/disable the daemons using the `systemctl` command.

**Note** The daemons are not enabled by default.

```bash
$ sudo setup/systemd/bin/install_systemd.py --config_dir ~/GitHub/pattoo-agents/etc

SUCCESS! You are now able to start/stop and enable/disable the following systemd services:

pattoo-os-spoked.service
pattoo-snmpd.service
pattoo-os-autonomousd.service
pattoo-os-hubd.service

$
```
