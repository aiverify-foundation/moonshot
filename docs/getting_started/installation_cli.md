# Installing Moonshot for CLI

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
  
       
<span style="font-size: 17px">There are 2 ways to install Moonshot - PyPi (Method 1) or Source (Method 2).</span>

## Method 1: Installation from PyPi
*You can find the Moonshot Package [here](https://pypi.org/project/projectmoonshot-imda/).* The source code is available on [GitHub](https://github.com/moonshot-admin/moonshot).


### Installing the Moonshot Library
The Moonshot Library allows you to interact with the Moonshot API without any additional features. This is the simplest way to get started with Moonshot if you only need to use the API. Install with:
```
$ pip install aiverify-moonshot
```

### Enabling Moonshot CLI
The Moonshot CLI enables you to interact with the Moonshot Library through your terminal. This allows you to run Moonshot commands directly from your terminal. 

```
$ pip install "aiverify-moonshot[cli]"
```

## Method 2: Installation from Source
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

## Running Moonshot

Before running Moonshot, ensure that [git](https://git-scm.com/downloads) is installed. Clone Moonshot data from GitHub:

```
$ python -m moonshot -i moonshot-data
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
python -m moonshot cli interactive -i moonshot-data -i moonshot-ui -e /path/to/your/.env
```

This example demonstrates how to launch the Moonshot CLI with additional parameters to install <b>moonshot-data</b> and <b>moonshot-ui</b>, and to configure it using a specified '<b>.env</b>' file.