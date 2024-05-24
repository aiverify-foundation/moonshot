## Explaining `python -m moonshot -i moonshot-ui`

### Step 1: Install Moonshot UI
1. Downloads Moonshot UI from GitHub.
```
$ git clone git@github.com:moonshot-admin/moonshot-ui.git
```
2. Installs Required Dependencies
- Makes sure that all necessary requirements are installed by executing the following command:
```
$ npm install
```
3. From the project root folder, executes the following command:
```
$ npm run build
```

### Step 2: Serving Moonshot UI
After the build is completed, serves the UI with this command:
```
$ npm start
```
Access the Web UI from browser `http://localhost:3000`