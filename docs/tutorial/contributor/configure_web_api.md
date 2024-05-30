# Running Moonshot as a Web API

Moonshot Web API is built using FastAPI. This guide will help you get started and configure your environment. This will be useful if you are intending to create your own UI.

## Launch Moonshot Web API

To run Moonshot Web API:
```
$ python -m moonshot web-api
```

For instructions on setting up the Moonshot UI, please refer to the [Moonshot UI repository](https://github.com/aiverify-foundation/moonshot-ui).

## Customising Moonshot Web API Configuration

By default, Moonshot Web API uses its own configuration settings. However, you can customize these settings by providing your own `.env` file in the directory where you are running Moonshot.

### Configuring Your Environment Variable File

The `.env` file should include the following variables:

| Key | Description | Example |
| --- | --- | --- |
|`MS_WEB_API_CONFIG` | This is used to specify the path to your configuration file. | `/User/path/to/your/config.yml` |
|`APP_ENVIRONMENT` | This defines the environment in which you are running Moonshot. | `PROD` |
|`HOST` | This is the host where you wish to run Moonshot. | `127.0.0.1` |
|`PORT` | This is the port at which you wish to run your FastAPI. | `/5000` |

### Configuring your Configuration File

The `config.yml` file contains several sections. Here's a brief overview of each section:

#### `asyncio`

| Key | Description | Example |
| --- | --- | --- |
|`monitor_task` | This flag determines whether to monitor tasks in asyncio or not. | `monitor_task: false` |

#### `ssl`

| Key | Description | Example |
| --- | --- | --- |
|`enabled` | This flag determines whether SSL is enabled or not. | `enabled: ${ENABLE_SSL:false}` |
|`file_path` | This is the path to the directory containing the SSL certificate and key files. | `file_path: "${SSL_FILE_PATH:./web_api/certs}` |
|`cert_filename` | This is the filename of the SSL certificate.| `cert_filename: "cert.pem"` |
|`key_filename` | This is the filename of the SSL key. | `key_filename: "key.pem"` |

#### `cors`

| Key | Description | Example |
| --- | --- | --- |
|`enabled` | This flag determines whether CORS is enabled or not. | `enabled: false` |
|`allowed_origins` | This is a list of origins that are allowed to make cross-origin requests.| `allowed_origins: "http://localhost:3000"` |

#### `log`

| Key | Description | Example |
| --- | --- | --- |
|`logging` |This flag determines whether logging is enabled or not. | `logging: ${LOGGING:true}` |
|`level` | This sets the level of logging. It could be `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. | `level: ${LOG_LEVEL:DEBUG}` |
|`format` |  This specifies the format of the log messages.  | `format: "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"` |
|`log_file_path` | This is the path where the log files will be stored. | `log_file_path: "/path/to/write/moonshot.logs"` |
|`log_file_max_size` | This is the maximum size (in bytes) that a log file can have before it gets rolled over. | `log_file_max_size: 5242880` |
|`log_file_backup_count` | This is the number of backup log files to keep. | `log_file_backup_count: 3"` |

For more example on how to structure your `config.yml` file, refer to the example provided [here](https://github.com/aiverify-foundation/moonshot/blob/main/examples/config.yml).