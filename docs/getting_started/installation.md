Skip to content
Navigation Menu
moonshot-admin
/
moonshot

Type / to search

Code
Issues
3
Pull requests
4
Actions
Projects
Security
Insights
Open a pull request
Create a new pull request by comparing changes across two branches. If you need to, you can also . Learn more about diff comparisons here.
 
...
 
  Able to merge. These branches can be automatically merged.
@imda-normanchia
Add a title
Deployment

Add a description
Comment
 
Add your description here...
 
Remember, contributions to this repository should follow our GitHub Community Guidelines.
️
Reviewers
No reviews—at least 1 approving review is required.
Assignees
No one—
Labels
None yet
Projects
None yet
Milestone
No milestone
Development
Use Closing keywords in the description to automatically close issues

Helpful resources
GitHub Community Guidelines
 3 commits
 4 files changed
 2 contributors
Commits on May 24, 2024
shift nltk import

Norman Chia authored and Norman Chia committed yesterday
deploy stuff

Norman Chia authored and Norman Chia committed yesterday
Commits on May 25, 2024
temporary version number

Norman Chia committed 1 minute ago
 Showing  with 11 additions and 69 deletions.
 4 changes: 2 additions & 2 deletions4  
README.md
 56 changes: 0 additions & 56 deletions56  
docs/getting_started/installation.md
@@ -1,56 +0,0 @@
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
  2 changes: 1 addition & 1 deletion2  
moonshot/__main__.py
@@ -5,7 +5,6 @@
import subprocess
import os
import threading 
import nltk
from dotenv import dotenv_values
from moonshot.api import api_set_environment_variables
"""
@@ -91,6 +90,7 @@ def moonshot_data_installation():
        # Install the requirements if they exist
        if os.path.exists("requirements.txt"):
            run_subprocess(["pip", "install", "-r", "requirements.txt"], check=True)
            import nltk
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('averaged_perceptron_tagger')
  18 changes: 8 additions & 10 deletions18  
pyproject.toml
@@ -4,7 +4,7 @@ build-backend = "hatchling.build"

[project]
name = "aiverify-moonshot"
version = "0.1.0"
version = "0.1.7"
authors = [
    { name="The Moonshot Team", email="our.moonshot.team@gmail.com" }
]
@@ -40,15 +40,14 @@ cli = [
    "rich==13.7.1",
]
all = [
    "projectmoonshot-imda[web-api]",
    "projectmoonshot-imda[cli]",
    "aiverify-moonshot[web-api]",
    "aiverify-moonshot[cli]",
]

[tool.hatch.build.targets.sdist]
artifacts = [
    "moonshot/data/connectors-endpoints/test-openai-endpoint.json"
]
exclude = [
  "assets/",
  "ci/",
  "docs/",
  "examples/",
  "misc/",
@@ -58,10 +57,9 @@ exclude = [

[tool.hatch.build.targets.wheel]
packages = ["moonshot"]
artifacts = [
    "moonshot/data/connectors-endpoints/test-openai-endpoint.json"
]
exclude = [
  "assets/",
  "ci/",
  "docs/",
  "examples/",
  "misc/",
@@ -80,7 +78,7 @@ allow-direct-references = true

[tool.poetry]
name = "aiverify-moonshot"
version = "0.1.0"
version = "0.1.7"
description = "A simple and modular tool to evaluate and red-team any LLM application."
authors = ["The Moonshot Team <our.moonshot.team@gmail.com>"]
readme = "README.md"
Footer
© 2024 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
loaded diff for docs/getting_started/installation.md 