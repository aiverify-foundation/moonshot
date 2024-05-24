# Installing Moonshot

## Preinstallation Requirements

This project <span style="color:red;">strictly</span> requires Python <span style="color:red;">3.11</span>. Ensure that you have Python 3.11 installed on your system before proceeding with installation and usage.

 | Software                                                                           | Version Requirement |
| ---------------------------------------------------------------------------------- | ------------------- |
| [Python](https://www.python.org/downloads/)                                        | v3.11               |
| [NodeJs](https://nodejs.org/en/download)                                           | v20.11.1 LTS or above               |
| npm                                        | v10.8.0 or above               |
| git                                        |                |

It is recommended to create a new Python virtual environment in your working directory before proceeding with installation. To do so, enter working directory and proceed with following steps:

=== "Windows Powershell"

    ``` 
    $ python -m venv venv
    $ venv/Scripts/Activate.ps1
    ```

=== "Windows Command Prompt"

    ```
    $ python -m venv venv
    $ venv/Scripts/activate.bat
    ```

=== "Mac"

    ```
    $ python -m venv venv
    $ source venv/bin/activate
    ```

## Installation from PyPi (To be updated - Please skip to next installation section)
*You can find the Moonshot Package [here](https://pypi.org/project/projectmoonshot-imda/).*


### Installing the Moonshot Library
The Moonshot Library allows you to interact with the Moonshot API without any additional features. This is the simplest way to get started with Moonshot if you only need to use the API. Install with:
```
$ pip install aiverify-moonshot
```

### Enabling Moonshot Web API
The Moonshot Web API enables you to interact with the Moonshot Library through HTTP requests. The Web API accomodates building a web application or accessing the Moonshot Library from a remote machine. Install with:
```
$ pip install "aiverify-moonshot[web-api]"
```

### Enabling Moonshot CLI
The Moonshot CLI enables you to interact with the Moonshot Library through your terminal. This allows you to run Moonshot commands directly from your terminal. 

```
$ pip install "aiverify-moonshot[cli]"
```

### Enabling Both CLI and WebAPI
This command enables you to interact with the Moonshot Library through HTTP requests and CLI. It gives you the most flexibility, as you can interact with Moonshot through both command-line commands and HTTP requests.
```
$ pip install "aiverify-moonshot[all]"
```

## Installation from Source
The source code is available on GitHub [here](https://github.com/moonshot-admin/moonshot). Ensure that [git](https://git-scm.com/downloads) is installed before proceeding with below steps.

1. Download the source files by cloning the repository:
```
$ git clone https://github.com/moonshot-admin/moonshot.git
```
2. Change directory to project's root directory:
```
cd moonshot
```
3. Checkout to the <i>run-moonshot</i> branch (temporary step):
```
git checkout run-moonshot
``` 
4. Install the required packages:
```
$ pip install -r requirements.txt
```


## Installation from PyPi (Latest)
The source code is available on GitHub [here](https://github.com/moonshot-admin/moonshot). Ensure that [git](https://git-scm.com/downloads) is installed before proceeding with below steps.

### Installation
Install the Moonshot package using pip by fetching the package from the specificied repository:
```
$ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple "projectmoonshot-imda[all]==0.3.13"

```

### Running Moonshot
Moonshot can be run in 3 different modes depending on your needs:  
<span style="font-size:15px;"> 1. Web and API Server</span>  
<span style="font-size:15px;"> 2. API Server</span>  
<span style="font-size:15px;"> 3. CLI</span>  


Before running Moonshot, clone Moonshot data from GitHub:

```
$ python -m moonshot -i moonshot-data
```

#### Web and API Server 
Before running the Web and API server, make sure <b>moonshot-ui</b> is installed. To clone moonshot-ui from GitHub:

```
$ python -m moonshot -i moonshot-ui
```

To start web-API server and UI server:

```
$ python -m moonshot web
``` 

#### API Server 
To run the web-API only:
```
$ python -m moonshot web-api
``` 

#### CLI Commands
To execute CLI commands:
```
$ python -m moonshot cli [command]
```

Replace [command] with a specific CLI command. For example, to run a recipe:
```
$ python -m moonshot cli list_cookbooks
``` 

Alternatively, to enter interactive mode in CLI (Recommended):
```
$ python -m moonshot cli interactive
``` 

### Additional Arguments

#### Specify Custom Environment File
If you have a custom '<b>.env</b>' file, specify the path to the file as follows:
```
python -m moonshot -e /path/to/your/.env
```
#### Others

You can also combine additional arguments with Moonshot's run commands like this:

```
python -m moonshot web -i moonshot-data -i moonshot-ui -e /path/to/your/.env
```

This example demonstrates how to launch the Moonshot web server with additional parameters to install <b>moonshot-data</b> and <b>moonshot-ui</b>, and to configure it using a specified '<b>.env</b>' file.