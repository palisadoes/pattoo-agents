# pattoo-os

`pattoo-os` daemons provide performance data on any Linux system it runs on. The data is presented in `json` format and can either be posted using HTTP to a remote server or viewed on the server on which it runs by visiting a well known URL.

The `json` data is formatted for easy ingestion by [pattooDB](https://github.com/PalisadoesFoundation/pattoo-ng)

## Installation
The steps are simple.

* Install the required packages using the `pip_requirements` document in the root directory
```
$ sudo pip3 install -r pip_requirements.txt
```
* Populate the configuration files.
* Start the desired daemons.
* Add the daemons to `systemd` so they start on reboot. (TBD / Pending)

## Usage

`pattoo-os` contains multiple daemons.

1. `pattoo-os-autonomousd.py` which will post `linux` system data in `json` format to a remote `pattoo` server
1. `pattoo-os-spoked.py` which will make the same `linux` system data in `json` format available for viewing on the local server. This allows the server to be polled for data from remote servers running  `pattoo-os-hubd` software agents.
1. `pattoo-os-hubd.py` which polls `pattoo-os-spoked` enables devices for data to be posted to the `pattoo` server.

The daemons will require a configuration file in the `etc/`directory. See the configuration section for details.

###
```bash
$ bin/pattoo-os-autonomousd.py --help
usage: pattoo-os-autonomousd.py [-h] [--start] [--stop] [--status] [--restart]
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
```


```bash
$ bin/pattoo-os-spoked.py --help
usage: pattoo-os-spoked.py [-h] [--start] [--stop] [--status] [--restart]
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
```

```bash
$ bin/pattoo-os-hubd.py --help
usage: pattoo-os-hubd.py [-h] [--start] [--stop] [--status] [--restart]
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
```


## Configuration

You will need to edit a configuration file in `etc/`directory. Pattoo will read any `.json` files found in this directory for configuration parameters.

For the sake of simplicity we will assume there is one file called `etc/config.yaml`

1. Make sure you have configured the `main` and `remote_api` sections of `etc/config.yaml` file before adding any sections for `pattoo-os` related daemons. The [CONFIGURATION.md](CONFIGURATION.md) file explains this in detail.
1. After doing this, edit the `etc/config.yaml` file to change configuration options specific to the daemons . An explanation follows.

### pattoo-os-hubd Section

Add the following statements to the `config.yaml` file to configure the  `pattoo-os-hubd` daemon. An explanation follows.


```yaml
pattoo-os-hubd:
    ip_devices:
      - ip_address: 127.0.0.1
        ip_bind_port: 5000    
      - ip_address: 127.0.0.2
        ip_bind_port: 5000            
```

#### Configuration Explanation

This table outlines the purpose of each configuration parameter

|Section | Sub-Section|Config Options          | Description                    |
|--|--|--|--|
| `pattoo-os-hubd`||| **Note:** Only required for devices running `pattoo-os-hubd` |
|| `ip_devices` | |Sub-Section providing a list of IP addresses or hostnames running `pattoo-os-spoked` that need to be polled for data. You must specify an `ip_address` and TCP `ip_bind_port`for each of these devices.|
||| `ip_address` | The IP adrress of the remote `ip_device`.|
||| `bind_port` | The TCP port on which the remote `ip_device` is listening.|

### pattoo-os-spoked Section

Add the following statements to the `config.yaml` file to configure the  `pattoo-os-spoked` daemon. An explanation follows.


```yaml
pattoo-os-spoked:
    listen_address: 0.0.0.0
    ip_bind_port: 5000
```

#### Configuration Explanation

This table outlines the purpose of each configuration parameter

|Section | Config Options          | Description                    |
|--|--|--|
| `pattoo-os-spoked` | | **Note:** Only required for devices running `pattoo-os-spoked` |
|| `listen_address` | IP address on which the API server will listen. Setting this to `0.0.0.0` will make it listen on all IPv4 addresses. Setting to `"0::"` will make it listen on all IPv6 configured interfaces. It will not listen on IPv4 and IPv6 addresses simultaneously. You must **quote** all IPv6 addresses.|
|| `ip_bind_port`              | TCP port on which the API will listen|

### pattoo-os-autonomousd Section

There is no `pattoo-os-autonomousd` section. The parameters in the `main` and `remote_api` sections is sufficient.

## Testing
If you are running `pattoo-os-spoked` on your local system, then you can test it by pointing your browser to `http://localhost:5000/pattoo-os` to view the system data.

## Troubleshooting
Check the log files in the `log_directory` specified in your configuration.
