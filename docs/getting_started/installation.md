# Installing Moonshot
The source code is available on GitHub at: [https://github.com/moonshot-admin/moonshot](https://github.com/moonshot-admin/moonshot).

## Installation from PyPi
*You can find the Moonshot Package [here](https://pypi.org/project/projectmoonshot-imda/).*

This project requires Python <span style="color:red;">3.11</span>
 or later. Make sure you have Python 3.11 installed on your system before proceeding with installation and usage.

To install Moonshot, there are 4 methods that you can choose from.

```
$ pip install projectmoonshot-imda # To install Moonshot library.
$ pip install "projectmoonshot-imda[web-api]" # To enable running Moonshot using the web API.
```

### Installing the Moonshot Library
The command `$ pip install projectmoonshot-imda` installs the basic Moonshot library. This allows you to interact with the Moonshot API without any additional features. This is the simplest way to get started with Moonshot if you only need to use the API.

### Enabling Moonshot Web API
The command `$ pip install "projectmoonshot-imda[web-api]"` installs the Moonshot library and also enables the web API. This allows you to interact with Moonshot through HTTP requests, which can be useful if you're building a web application or if you need to access Moonshot from a remote machine.

## Installation from Source
1. Download the source files by cloning this repositiry. i.e. Git clone (via SSH):
```
$ git clone git@github.com:moonshot-admin/moonshot.git
```
2. Change directory to project's root directory:
```
$ cd moonshot
``` 
3. Install the required packages:
```
$ pip install -r requirements.txt
```