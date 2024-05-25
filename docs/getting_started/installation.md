# Installing Moonshot

## Installation from PyPi
*You can find the Moonshot Package [here](https://pypi.org/project/projectmoonshot-imda/).*

This project requires Python <span style="color:red;">3.11</span>
 or later. Ensure that you have Python 3.11 installed on your system before proceeding with installation and usage.
<!---
To install Moonshot, there are 4 methods that you can choose from.

```
$ pip install projectmoonshot-imda # To install Moonshot library.
$ pip install "projectmoonshot-imda[web-api]" # To enable running Moonshot using the web API.
```
-->

### Installing the Moonshot Library
The Moonshot Library allows you to interact with the Moonshot API without any additional features. This is the simplest way to get started with Moonshot if you only need to use the API. Install with:
```
$ pip install projectmoonshot-imda
```

### Enabling Moonshot Web API
The Moonshot Web API enables you to interact with the Moonshot Library through HTTP requests. The Web API accomodates building a web application or accessing the Moonshot Library from a remote machine. Install with:
```
$ pip install "projectmoonshot-imda[web-api]"
```

### Enabling Moonshot CLI
The Moonshot CLI enables you to interact with the Moonshot Library through your terminal. This allows you to run Moonshot commands directly from your terminal. 

```
$ pip install "projectmoonshot-imda[cli]"
```

### Enabling Both CLI and WebAPI
This command enales you to interact with the Moonshot Library through HTTP requests and CLI. It gives you the most flexibility, as you can interact with Moonshot through both command-line commands and HTTP requests.
```
$ pip install "projectmoonshot-imda[all]"
```

## Installation from Source
The source code is available on GitHub [here](https://github.com/moonshot-admin/moonshot).

1. Download the source files by cloning the repository:
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