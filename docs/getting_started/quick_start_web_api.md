# Quick Start Guide (Web API)

## Setting Up

### Step 0: Creating virtual environment
If you have not created a virtual environment, we suggest creating one to avoid any conflicts in the Python libraries.

### Step 1: Install Moonshot
1. To begin, install Moonshot from the designated source (e.g., GitHub/pypi).
```
$ git clone git@github.com:moonshot-admin/moonshot.git

OR 

$ pip install "projectmoonshot-imda[web-api]"
```

2. Install Required Dependencies
- Make sure that all necessary requirements are installed by executing the appropriate command provided in the documentation.
- If you are installing the project from GitHub, run the following command:
```
$ pip install -r requirements.txt
```

### Step 2: Environment Variables (Optional)
- If you prefer to use your own datasets instead of the default data provided by the library, you can create a `.env` file with the necessary values in the directory where you are running the moonshot command.

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

## Starting the Web API Server

To start the Web API server, all you have to do is run this code in your console.
```
$ python -m moonshot web-api
```

To know more about the available endpoints. Please refer to the Web-API documentation [here](/web_api/web_api_guide/).
## Setting Up the UI

### Step 1: Install Moonshot UI
1. To begin, install Moonshot UI from GitHub.
```
$ git clone git@github.com:moonshot-admin/moonshot-ui.git
```
2. Install Required Dependencies
- Make sure that all necessary requirements are installed by executing the appropriate command provided in the documentation.
```
$ npm install
```
3. From the project root folder, build the project
```
$ npm run build
```

### Step 2: Starting Web UI
After the build build step is completed, start the Web UI with this command
```
$ npm start
```
Access the Web UI from browser `http://localhost:3000`