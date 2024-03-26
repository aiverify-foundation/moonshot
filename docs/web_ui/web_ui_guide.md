# Getting Started with Moonshot Web UI

| Prerequisite                           |
|----------------------------------------|
| Node.js version 20.11.1 LTS and above  |
| Python version 3.11 and above           |
| Moonshot Web API Python module - projectmoonshot-imda version 0.3.0 |

# Setting up Moonshot Web UI
Before proceeding with the installation of Moonshot Web UI, ensure that you have already set up Moonshot Web API. You can find the instruction on running Moonshot Web API [here](/getting_started/quick_start_web_api).

## Installing Moonshot Web UI
The Moonshot Web UI is an interface that allow you to interact with the Moonshot Tool.

- You can install  Moonshot Web UI by cloning from the [GitHub Repository](https://github.com/moonshot-admin/moonshot-ui).
```
git clone git@github.com:moonshot-admin/moonshot-ui.git
```

- To enter the project root, run this command after running the git clone command: 
```
cd moonshot-ui
```

- After cloning the repository, you will need to create a `.env` file with this variable in the project root.
```json
# This should be the URL of the Moonshot Web Api module which was started in the previous section.
# Check the startup logs to determine the hostname and port number.

MOONSHOT_API_URL=http://127.0.0.1:5000
```

## Building Moonshot Web UI
Once you have installed the Web Ui and created the `.env` configuration file. You would be required to build the project from the Web UI root folder.
```
npm run build
```

## Running Moonshot Web UI
After the build step is completed, start the Web UI with this command
```
npm start
```

Access the Web UI from browser `http://localhost:3000`