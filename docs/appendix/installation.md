## Setting up Logging
By default, the moonshot library uses a logger to write logs with its severity to `moonshot.log`.

There are multiple severity levels that we are currently using:

| Logging Severity | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| debug            | Used for detailed debugging information, helpful during development. |
| info             | General information about system operation, useful for system monitoring. |
| warning          | Indicates a potential issue that should be looked into but is not immediately critical. |
| error            | Reports a failure within the system, requiring immediate attention. |

Additionally, you can customize the logging behavior through environment variables:

| Environment Variable | Description | Default Value |
| -------------------- | ----------- | ------------- |
| MS_LOG_NAME          | The name of the log file. | `moonshot.log` |
| MS_LOG_LEVEL         | The minimum logging severity to capture. Can be one of `debug`, `info`, `warning`, or `error`. | `info` |
| MS_LOG_TO_FILE       | Whether to write logs to a file (`true`) or to standard output (`false`). | `false` |

To customize the logging behavior of Moonshot through environment variables, you can export them in your terminal.<br>
This allows you to override the default logging configurations. Here's how you can set them:
```
export MS_LOG_NAME=moonshot
export MS_LOG_LEVEL=debug
export MS_LOG_TO_FILE=true
```
After exporting these variables, any subsequent runs of the Moonshot application will adhere to these logging settings 
until the terminal session ends or the variables are unset.

The logging format is designed to provide a clear and concise overview of each log entry, structured as follows:
```
%(asctime)s [%(levelname)s][%(filename)s::%(funcName)s(%(lineno)d)] %(message)s
```
This format includes:

- timestamp (`%(asctime)s`)
- severity level (`%(levelname)s`)
- filename (`%(filename)s`)
- function name (`%(funcName)s`)
- line number (`%(lineno)d`)
- log message (`%(message)s`)

For example:
```
2023-04-01 12:00:00 [INFO][module.py::main(10)] Application started successfully.
```
This detailed format ensures that logs are not only easily readable but also provide in-depth information for
debugging and monitoring purposes.

### Specifying Custom Environment File
If you have a custom '<b>.env</b>' file, specify the path to the file as follows:
```
python -m moonshot -e /path/to/your/.env
```