# Quick Start Guide (Web API)

## Setting Up

### Step 0: Creating a virtual environment
We highly recommend creating a virtual environment to avoid any conflicts in the Python libraries.

### Step 1: Install Moonshot
1. To begin, install Moonshot from the designated source (e.g., GitHub/PyPi).
```
$ git clone git@github.com:moonshot-admin/moonshot.git

OR 

$ pip install "projectmoonshot-imda[web-api]"
```

2. Install Required Dependencies
- Ensure that all necessary requirements are installed by executing the appropriate command provided in the documentation.
- If you are installing the project from GitHub, run the following command:
```
$ pip install -r requirements.txt
```

### Step 2: Environment Variables (Optional)
- You can link your own data folder with the library by running the following code snippet:
<!--Instead of using the stock test data provided by the library, you have the option to link your own data folder by running the following code to connect your file directory.-->

```json

CONNECTORS = "/path/to/your/connectors"
RECIPES = "/path/to/your/recipes"
COOKBOOKS = "/path/to/your/cookbooks"
DATASETS = "/path/to/your/datasets"
PROMPT_TEMPLATES = "/path/to/your/prompt-templates"
METRICS = "/path/to/your/metrics"
METRICS_CONFIG = "/path/to/your/metrics/metrics_config.json"
CONTEXT_STRATEGY = "/path/to/your/context-strategy"
RESULTS = "/path/to/your/results"
DATABASES = "/path/to/your/databases"
SESSIONS = "/path/to/your/sessions"

```
_Note: When changing the reference folder for data, users will no longer be able to access the stock cookbooks. To access these cookbooks, users should copy over their respctive json files and dependencies_

## Starting the Web API Server

To start the Web API server, run the following command in your console.
```
$ python -m moonshot web-api
```

To know more about the available endpoints, refer to the Web API documentation [here](/web_api/web_api_guide/).
## Setting Up Moonshot UI
The Moonshot UI is a UI extension that runs on top of the Moonshot Web API server.

### Step 0: Install Prerequisites
Ensure the following prerequisites are installed:

1. Node.js verion 20.11.1 LTS and above
2. Python version 3.11 and above
3. Moonshot Web API. Ensure the Web API server is running as well.

### Step 1: Install Moonshot UI
1. To begin, download Moonshot UI from GitHub.
```
$ git clone git@github.com:moonshot-admin/moonshot-ui.git
```
2. Install Required Dependencies
- Make sure that all necessary requirements are installed by executing the following command:
```
$ npm install
```
3. From the project root folder, execute the following command:
```
$ npm run build
```

### Step 2: Serving Moonshot UI
After the build is completed, serve the UI with this command:
```
$ npm start
```
Access the Web UI from browser `http://localhost:3000`