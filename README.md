<div align="center">

```
  _____           _           _     __  __                       _           _   
 |  __ \         (_)         | |   |  \/  |                     | |         | |  
 | |__) | __ ___  _  ___  ___| |_  | \  / | ___   ___  _ __  ___| |__   ___ | |_ 
 |  ___/ '__/ _ \| |/ _ \/ __| __| | |\/| |/ _ \ / _ \| '_ \/ __| '_ \ / _ \| __|
 | |   | | | (_) | |  __/ (__| |_  | |  | | (_) | (_) | | | \__ \ | | | (_) | |_ 
 |_|   |_|  \___/| |\___|\___|\__| |_|  |_|\___/ \___/|_| |_|___/_| |_|\___/ \__|
                _/ |                                                             
               |__/                                                              

```
**Version 0.1.0**

A simple and modular tool to evaluate and red-team any LLM application.

[![Python 3.11](https://img.shields.io/badge/python-3.11-green)](https://www.python.org/downloads/release/python-3111/)


</div>

Moonshot is a tool designed for AI developers and security experts to evaluate and red-team any LLM/ LLM application. In this initial version, Moonshot can be used through its interative Command Line Interface, within python notebooks [(example)](https://github.com/moonshot-admin/moonshot/tree/main/examples/test-openai-gpt35.ipynb), or even seamlessly integrated into your model development workflow to to run repeatable tests.



## Getting Started
### Prerequisites
1. Python (at least version 3.11)

2. Virtual Environment (optional) - Good to have different environments to separate Python dependencies

    - Create a virtual environment:
    ```
    python -m venv venv
    ```
    - Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
### Installation
The source code is available on GitHub at: [https://github.com/moonshot-admin/moonshot](https://github.com/moonshot-admin/moonshot)
```
$ pip install moonshot
$ pip install moonshot[cli] #To enable running Moonshot using the CLI.
$ pip install moonshot[web-api] #To enable running Moonshot using the web API.
$ pip install moonshot[all] #To enable running Moonshot using the CLI and web API.
```
#### Installation from source
1. Download the source files by cloning this repository. i.e. Git clone (via SSH): 
    
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

## Running Moonshot
### Web API
To run Moonshot Web API:
```
$ python -m moonshot web_api
```

### CLI
Two modes are available on the Moonshot CLI: Command-Based Mode and Interactive Mode. 

To run Moonshot in Command-Based Mode: 
```
$ python -m moonshot cli <command>
```
To run Moonshot in Interactive Mode:
```
$ python -m moonshot cli interactive
```

Additional instructions on CLI can be found in the [documentation](https://moonshot-admin.github.io/moonshot/).

## License
Licensed under [Apache Software License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)
