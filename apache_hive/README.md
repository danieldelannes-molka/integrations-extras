# apache_hive Integration

## Overview

[This integration gets hiveserver Metrics from ambari Metrics and sends them to datadog]

* You can also use images here:

![snapshot][1]

## Setup

### Installation

[As a prerequest you must have installed on the target host with ambari metrics activatied. To install go to the configuration file and add the following: to ambari_api_url add the host and port number for the ambari api (should be localhost:6188), to the 'APPID' give the name of the service you want to get metrics from, in this case it should be 'hiveserver2'. tags, hostname and device_name are optional]

### Configuration

Create a `apache_hive.yaml` in the Datadog Agent's `conf.d` directory.

#### Metric Collection

Add this configuration setup to your `apache_hive.yaml` file to start gathering your [metrics][2]:

```
init_config:

instances:
  - []
```

Configuration Options:

[ambari_api_url contains the host and port where the ambari api is located and APPID is the name that the hiveserver is listed under in the api]

[Restart the Agent][3] to begin sending Redis metrics to Datadog.

### Validation

[Run the Agent's `status` subcommand][4] and look for `apache_hive` under the Checks section:

```
  Checks
  ======
    [...]

    apache_hive
    -------
      - instance #0 [OK]
      - Collected 26 metrics, 0 events & 1 service check

    [...]
```

## Compatibility

The check is compatible with all major platforms.

## Data Collected

### Metrics

See [metadata.csv][5] for a list of metrics provided by this integration.

### Events

apache_hive has one event that is triggered if the http request fails.

### Service Checks

[there are currently no service checks for this integration]

## Troubleshooting

[...]

## Development

Please refer to the [main documentation][6]
for more details about how to test and develop Agent based integrations.

[1]: https://raw.githubusercontent.com/DataDog/cookiecutter-datadog-check/master/%7B%7Bcookiecutter.check_name%7D%7D/images/snapshot.png
[2]: #metrics
[3]: https://docs.datadoghq.com/agent/faq/agent-commands/#start-stop-restart-the-agent
[4]: https://docs.datadoghq.com/agent/faq/agent-commands/#agent-status-and-information
[5]: https://github.com/DataDog/cookiecutter-datadog-check/blob/master/%7B%7Bcookiecutter.check_name%7D%7D/metadata.csv
[6]: https://docs.datadoghq.com/developers/
