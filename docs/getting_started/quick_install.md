# Installing Moonshot for User Interface

## Dependencies needed for installation

This project <span style="color:red;">strictly</span> requires Python <span style="color:red;">3.11</span>. Ensure that you have Python 3.11 installed on your system before proceeding with installation and usage.

 | Software                                                                           | Version Requirement |
| ---------------------------------------------------------------------------------- | ------------------- |
| [Python](https://www.python.org/downloads/)                                        | v3.11               |
| [NodeJs](https://nodejs.org/en/download)                                           | v20.11.1 LTS or above               |
| npm                                        | v10.8.0 or above               |
| git                                        |                |

## Install Moonshot
Run the following command in a virtual environment of your choice:

```
$ pip install "aiverify-moonshot[all]"
```

Once installed, Moonshot provides commands to download all the test assets required to start testing your AI system:

```
$ python -m moonshot -i moonshot-data -i moonshot-ui
```

Run Moonshot UI with the following command:

```
$ python -m moonshot web
``` 

Lastly, access Moonshot UI using a browser (`http://localhost:3000`).

!!! warning
    If you are operating on an x86 MacOS, you may encounter difficulties when attempting to install the dependency for moonshot-data. Please refer to this [FAQ](../faq.md#i-am-unable-to-install-pytorch) for a potential solution.

## Extra Resources

### Setting up Virtual Environment

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

### Specifying Custom Environment File
If you have a custom '<b>.env</b>' file, specify the path to the file as follows:
```
python -m moonshot -e /path/to/your/.env
```