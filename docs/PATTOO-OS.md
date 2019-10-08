# pattoo-os

`pattoo-os` provide performance data on any Linux system it runs on. The data is presented in `json` format and can either be posted using HTTP to a remote server or viewed on the server on which it runs by visiting a well known URL.

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
1. `pattoo-os-hubd.py` which polls `pattoo-os-spoked` enables devices for data to be posted to the `patoo` server.

Both daemons will require configuration files in one or more subdirectories of the `etc/`directory. See the configuration section for details.

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

You will need to edit configuration files in both the `etc/` and `etc/pattoo-os.d` directories.

### Directory etc/

This directory contains configuration `.yaml` files used by all polling agents. The files in this directory contain shared or common configuration parameters.

Edit the `etc/config.yaml` file to change configuration options. An explanation follows.

```yaml
main:
    log_level: debug
    log_directory: ~/GitHub/pattoo-agents/log
    cache_directory: ~/GitHub/pattoo-agents/cache
    language: en
    polling_interval: 300

remote_api:
    api_server_name: 192.168.1.100
    api_server_port: 6000
    api_server_https: False
    api_server_uri: /pattoo/post

```

#### Configuration Explanation

This table outlines the purpose of each configuration parameter

|Section | Config Options          | Description                    |
|--|--|--|
| `main` |||
||  `log_directory` | Path to logging directory. Make sure the username running the daemons have RW access to files there. |
||  `log_level` | Default level of logging. `debug` is best for troubleshooting. |
|| `cache_directory` | Directory of unsuccessful data posts to `pattoodb`|
|| `language` | Language  to be used in reporting statistics in JSON output. Language files can be found in the `metadata/language/agents/` directory.|
|| `polling_interval`              | Interval of data collection and posting in seconds   |
| `remote_api` |||
|| `api_server_name`       | IP address of remote `pattoodb` server      |
|| `api_server_port`       | Port of remote `pattoodb` server     |
|| `api_server_https`      | Use `https` when sending data  to remote `pattoodb` server|
|| `api_server_uri`        | Remote `pattoodb` route prefix       |


### Directory etc/pattoo-os.d/

Place a configuration file here if you intend to use the `pattoo-os-spoked` daemon.

Edit the `etc/pattoo-os.d/config.yaml` file to change configuration options. An explanation follows.


```yaml
pattoo-os-spoked:
    listen_address: 0.0.0.0
    ip_bind_port: 5000

pattoo-os-hubd:
    ip_devices:
      - ip_address: 127.0.0.1
        ip_bind_port: 5000    
      - ip_address: 127.0.0.2
        ip_bind_port: 5000            
```

#### Configuration Explanation

This table outlines the purpose of each configuration parameter

|Section | Config Options          | Description                    |
|--|--|--|
| `pattoo-os-spoked` | | **Note:** Only required for devices running `pattoo-os-spoked` |
|| `listen_address` | IP address on which the API server will listen. Setting this to `0.0.0.0` will make it listen on all IPv4 addresses. Setting to `"0::"` will make it listen on all IPv6 configured interfaces. It will not listen on IPv4 and IPv6 addresses simultaneously. You must **quote** all IPv6 addresses.|
|| `ip_bind_port`              | TCP port on which the API will listen|
| `pattoo-os-hubd` | | **Note:** Only required for devices running `pattoo-os-hubd` |
|| `ip_devices` | List of IP addresses or hostnames running `pattoo-os-spoked` that need to be polled for data. You must specify an `ip_address` and TCP `ip_bind_port`for these devices.

## JSON Data Format

The `json` data formatting can be found in the [DATA.md](DATA.md) file

## Testing
If you are running `pattoo-os` on your local system, then you can test it by pointing your browser to `http://localhost:5000/pattoo-os` to view the system data.

## Troubleshooting
Check the log files in the `log_directory` specified in your configuration.
