# Configuration

After installing your agents, you will need to edit a configuration file in the `etc/`directory. Pattoo will read any `.yaml` files found in this directory for configuration parameters.

For the sake of simplicity we will assume there is one file called `etc/config.yaml`. 

Make sure you have configured the `main` and `remote_api` sections of `etc/config.yaml` file before adding any sections for `pattoo-os` related daemons.

## Custom Directory Location
You can selectively set the location of the configuration directory by using the `PATTOO_CONFIGDIR` environmental variable. 

This can be useful for:

1. Automated deployments
1. Software developer code testing

By default the `etc/` directory of the repository is used for all configuration file searches.

## Mandatory Configuration Sections
```yaml
main:
    log_level: debug
    log_directory: ~/GitHub/pattoo-agents/log
    cache_directory: ~/GitHub/pattoo-agents/cache
    language: en
    polling_interval: 300

remote_api:
    api_ip_address: 192.168.1.100
    api_ip_bind_port: 6000
    api_uses_https: False
    api_uri: /pattoo/post

```

### Configuration Explanation

This table outlines the purpose of each configuration parameter

|Section | Config Options          | Description                    |
|--|--|--|
| `main` |||
||  `log_directory` | Path to logging directory. Make sure the username running the daemons have RW access to files there. |
||  `log_level` | Default level of logging. `debug` is best for troubleshooting. |
|| `cache_directory` | Directory of unsuccessful data posts to `pattoodb`|
|| `language` | Language  to be used in reporting statistics in JSON output. Language files can be found in the `metadata/language/agents/` directory.|
|| `polling_interval`              | Interval of data collection and posting in seconds   |
| `remote_api` || **Note** The `remote_api` section is not required for `patoo-os-spoked` configurations|
|| `api_ip_address`       | IP address of remote `pattoodb` server      |
|| `api_ip_bind_port`       | Port of remote `pattoodb` server     |
|| `api_uses_https`      | Use `https` when sending data  to remote `pattoodb` server|
|| `api_uri`        | Remote `pattoodb` API URI|

## Agent Configuration
See the [README.md](README.md) file for details on how to configure each type of agent.

## Notes
Here are some addtional tips.

1. You can create a separate configuration file for each section. If you are doing this, make sure there is only one file per agent section. Keep the mandtatory configurations sections in a separate file for simplicity. Practice on a test system before doing this. *Start with a single file first to gain confidence.*

