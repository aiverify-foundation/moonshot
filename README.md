<div align="center">

![Moonshot Logo](https://github.com/aiverify-foundation/moonshot/raw/main/misc/aiverify-moonshot-logo.png)

**Version 0.7.4**

A simple and modular tool to evaluate any LLM-based AI systems.

[![Python 3.11](https://img.shields.io/badge/python-3.11-green)](https://www.python.org/downloads/release/python-3111/)


</div>

## 🎯 Motivation

Developed by the [AI Verify Foundation](https://aiverifyfoundation.sg/), [Moonshot](https://aiverifyfoundation.sg/project-moonshot/) is a tool to bring Benchmarking and Red-Teaming together to help AI developers, compliance teams evaluate LLM-based Apps and LLMs.

</br>

## 🚀 Why Moonshot

In the rapidly evolving landscape of Generative AI, ensuring safety, reliability, and performance of LLM applications is paramount. Moonshot addresses this critical need by providing a unified platform for:
- <b>Benchmark Tests:</b> Systematically test LLM Apps or LLMs across critical trust & safety risks using a wide array of open-source benchmark dataset and metrics, including guided workflows to implement <b>IMDA's Starter Kit for LLM-based App Testing</b>.
- <b>Red Team Attacks:</b> Proactively identify vulnerabilities and potential misuse scenarios in your LLM applications through streamlined adversarial prompting.

</br>

## 🔑 Key Features

- <b>User-friendly Interfaces:</b> Interact with Moonshot via an intuitive Web UI for visual insights, and an interactive Command Line Interface (CLI) for quick operations.
- <b>Comprehensive Benchmarking:</b>
  - [View list of available datasets available](https://aiverify-foundation.github.io/moonshot/resources/datasets/)
  - Test for <b>Performance</b> (e.g., accuracy, BLEU)
  - Ensure <b>Trust & Safety</b> e.g., bias, toxicity, hallucination)
  - Utilize built-in workflow to implement IMDA's Starter Kit for LLM-based App Testing. [View available pre-built Cookbooks](https://aiverify-foundation.github.io/moonshot/resources/cookbooks/)
- <b>Powerful Red-Teaming:</b>
  - [View list of available attack modules](https://aiverify-foundation.github.io/moonshot/resources/attack_modules/)
  - Simplify adversarial prompt generation using algorithmic strategies or generative LLM to uncover potential misuse.
  - Leverage prompt templates, context strategies, and automated attack modules.
- <b>Customizable Recipes:</b> Build your own benchmark tests with custom datasets (input-target pairs), prompt templates (optional), evaluation metric, and grading scales. [View available pre-built Recipes](https://aiverify-foundation.github.io/moonshot/resources/recipes/)
- <b>Insightful Reporting:</b> Use our HTML reports with interactive charts for clear visualization of test results, and download detailed raw JSON results for deeper programmatic analysis.
- <b>Extensible & Modular:</b> Designed for easy extension and integration with new LLM applications, benchmarks, and attack techniques.

</br>

# Getting Started

Moonshot can be used through several interfaces:
- User-friendly Web UI - [Web UI User Guide](https://aiverify-foundation.github.io/moonshot/user_guide/web_ui/web_ui_guide/)
- Interactive Command Line Interface - [CLI User Guide](https://aiverify-foundation.github.io/moonshot/user_guide/cli/connecting_endpoints/)
- Seamless Integration into your MLOps workflow via Moonshot Library APIs or Moonshot Web APIs - [Notebook Examples](https://github.com/aiverify-foundation/moonshot/tree/main/examples/jupyter-notebook), [Web API Docs](https://aiverify-foundation.github.io/moonshot/api_reference/web_api_swagger/)

</br>

## 💻 Let's Go!

This section will guide you through getting Moonshot up and running.

</br>

### ✅ Prerequisites
1. <b>Python:</b> [Version 3.11](https://www.python.org/downloads/) is required. 

2. <b>Git Version Control:</b> [Git](https://github.com/git-guides/install-git) is essential for cloning the repository.

3. <b>(Optional) Virtual Environment:</b> Highly recommended to manage dependencies.

    ```
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    source venv/bin/activate
    ```
4. If you plan to install our Web UI, you will also need [Node.js version 20.11.1 LTS](https://nodejs.org/en/blog/release/v20.11.1) and above
</br>

### ⬇️ Installation

You can install Moonshot in various ways depending on your needs

<b>1. Using `pip` (Recommended for most users)</b>

```
# Install Project Moonshot's Python Library, which includes Moonshot's full functionalities (Library APIs, CLI and Web APIs)
pip install "aiverify-moonshot[all]"

# Clone and install test assets and Web UI
python -m moonshot -i moonshot-data -i moonshot-ui
```
⚠️ You will need to have test assets from [moonshot-data](https://github.com/aiverify-foundation/moonshot-data) before you can run any tests.

🖼️ If you plan to install our Web UI, you will also need [moonshot-ui](https://github.com/aiverify-foundation/moonshot-ui)

Check out our [Installation Guide](https://aiverify-foundation.github.io/moonshot/getting_started/quick_install/) for more details.

</br>

<b>2. From Source Code (For developers and contributors)</b>

```
# To install from source code (Full functionalities)
git clone git@github.com:aiverify-foundation/moonshot.git
cd moonshot
pip install -r requirements.txt
```
If you have installation issues, please take a look at the [Troubleshooting Guide](https://aiverify-foundation.github.io/moonshot/faq/).
<details>
<summary><b>Other installation options</b></summary>
Here's a summary of other installation commands available:

```
# To install Moonshot library APIs only
pip install aiverify-moonshot

# To install Moonshot library APIs and Web APIs only
pip install "aiverify-moonshot[web-api]"

# To install Moonshot library APIs and CLI only
pip install "aiverify-moonshot[cli]"
```
Check out our [Installation Guide](https://aiverify-foundation.github.io/moonshot/getting_started/quick_install/) for more details.
</details>

</br>

### 🏃‍♀️ Run Moonshot

#### Running the Web UI
```
python -m moonshot web
```
Open [http://localhost:3000/](http://localhost:3000/) in a browser and you should see this homepage:

![Moonshot UI Home](https://github.com/aiverify-foundation/moonshot/raw/main/misc/ui-homepage.png)

Refer to this [guide](https://aiverify-foundation.github.io/moonshot/user_guide/web_ui/moonshot_interface/homepage/) to discover the rich features available in Moonshot Web UI

</br>

#### Running the Interactive CLI
```
python -m moonshot cli interactive
```
![Moonshot cli](https://github.com/aiverify-foundation/moonshot/raw/main/misc/cli-homepage.png)

Refer to this [Command List](https://aiverify-foundation.github.io/moonshot/user_guide/cli/cli_command_list/) to discover the list of CLI commands for Moonshot

</br></br>

# 📚 Documentation & User Guides

For detailed information on configuring, using, and extending Moonshot, please refer to our comprehensive documentation:

#### Guides for Moonshot Web UI
- [Getting Started with Moonshot Web UI](https://aiverify-foundation.github.io/moonshot/user_guide/web_ui/web_ui_guide/)
- [Creating Your Custom Cookbook via Moonshot Web UI](https://aiverify-foundation.github.io/moonshot/tutorial/web-ui/create_cookbook/)
- [Creating Your Custom Connector Endpoint via Moonshot Web UI](https://aiverify-foundation.github.io/moonshot/tutorial/web-ui/create_endpoint/)
- [Running Benchmark Test on Moonshot Web UI](https://aiverify-foundation.github.io/moonshot/getting_started/first_test/)
- [Running Red Teaming on Moonshot Web UI](https://aiverify-foundation.github.io/moonshot/tutorial/web-ui/redteam/)

#### Guides for Moonshot Interactive CLI
- [Getting Started with Moonshot Interactive CLI](https://aiverify-foundation.github.io/moonshot/user_guide/cli/connecting_endpoints/)
- [Creating Your Custom Benchmark Tests for Your RAG Apps via Moonshot Interactive CLI](https://aiverify-foundation.github.io/moonshot/tutorial/cli/create_benchmark_tests/)
- [Creating Your Custom Connector Endpoint via Moonshot Interactive CLI](https://aiverify-foundation.github.io/moonshot/tutorial/cli/create_endpoint/)
- [Running Benchmark Test on Moonshot Interactive CLI](https://aiverify-foundation.github.io/moonshot/tutorial/cli/run_benchmark_tests/)
- [Running Red Teaming on Moonshot Interactive CLI](https://aiverify-foundation.github.io/moonshot/tutorial/cli/run_red_teaming/)

#### For Users Interested in trying Out Moonshot using Jupyter Notebook
- [Moonshot Library Python Notebook Examples](https://github.com/aiverify-foundation/moonshot/tree/main/examples/jupyter-notebook)

#### 

</br>

## 🤝 Contribution

Moonshot is an open-source project, and we welcome contributions from the community! Whether fixing a bug, adding a new feature, improving documentation, or suggesting an enhancement, your efforts are highly valued.

Please refer to our [Contributor Guide](https://aiverify-foundation.github.io/moonshot/contributing/) for details on how to get started.

</br>

## ✨ Project Status

Moonshot is currently in beta. We are actively developing new features, improving existing ones, and enhancing stability. We encourage you to try it out and provide feedback!

</br>

## 📜 License

Moonshot is released under the [Apache Software License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

</br>
