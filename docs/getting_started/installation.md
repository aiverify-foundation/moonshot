# Installing Moonshot
The source code is available on GitHub at: [https://github.com/moonshot-admin/moonshot](https://github.com/moonshot-admin/moonshot).

## Installation from PyPi
*You can find the Moonshot Package [here](pypi.com).*

This project requires Python <span style="color:red;">3.11</span>
 or later. Make sure you have Python 3.11 installed on your system before proceeding with installation and usage.


To install Moonshot, there is 4 options that you can choose from.
```
$ pip install moonshot
$ pip install moonshot[cli] #To enable running Moonshot using the CLI.
$ pip install moonshot[web-api] #To enable running Moonshot using the web API.
$ pip install moonshot[all] #To enable running Moonshot using the CLI and web API.
```
Each installation command installs only the necessary dependencies required to run Moonshot based on your specific use case.

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