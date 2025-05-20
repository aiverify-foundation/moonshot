<div align="center">

![Moonshot Logo](https://github.com/aiverify-foundation/moonshot/raw/main/misc/aiverify-moonshot-logo.png)

**Version 0.6.3**

A simple and modular tool to evaluate any LLM applications.

[![Python 3.11](https://img.shields.io/badge/python-3.11-green)](https://www.python.org/downloads/release/python-3111/)


</div>

## 🎯 Motivation

Developed by the [AI Verify Foundation](https://aiverifyfoundation.sg/?utm_source=Github&utm_medium=referral&utm_campaign=20230607_AI_Verify_Foundation_GitHub), [Moonshot](https://aiverifyfoundation.sg/project-moonshot/?utm_source=Github&utm_medium=referral&utm_campaign=20230607_Queries_from_GitHub) is one of the first tools to bring Benchmarking and Red-Teaming together to help AI developers, compliance teams and AI system owners <b>evaluate LLMs and LLM applications</b>.

</br>

## 🚀 Why Moonshot

In the rapidly evolving landscape of Generative AI, ensuring the safety, reliability, and performance of LLM applications is paramount. Moonshot addresses this critical need by providing a unified platform for:
- <b>Benchmark Tests:</b> Systematically test LLMs across various performance metrics, and critical trust & safety dimensions using a wide array of open-source benchmarks and domain-specific tests.
- <b>Red Team Attacks:</b> Proactively identify vulnerabilities and potential misuse scenarios in your LLM applications through streamlined adversarial prompting.
- <b>Streamline MLOps:</b> Integrate evaluation seamlessly into your development pipeline with flexible APIs.

</br>

## 🔑 Key Features

- <b>User-friendly Interfaces:</b> Interact with Moonshot via an intuitive Web UI for visual insights, and an interactive Command Line Interface (CLI) for quick operations.
- <b>Comprehensive Benchmarking:</b>
  - [View list of available datasets available](https://aiverify-foundation.github.io/moonshot/resources/datasets/)
  - Test for <b>Performance</b> (e.g., accuracy, BLEU)
  - Ensure <b>Trust & Safety</b> e.g., bias, toxicity, hallucination)
  - Utilize pre-built Cookbooks of tests or easily create your custom evaluations. [View available pre-built Cookbooks](https://aiverify-foundation.github.io/moonshot/resources/cookbooks/)
- <b>Powerful Red-Teaming:</b>
  - [View list of available attack modules](https://aiverify-foundation.github.io/moonshot/resources/attack_modules/)
  - Simplify adversarial prompt generation using algorithmic strategies or generative LLM to uncover potential misuse.
  - Leverage prompt templates, context strategies, and automated attack modules.
- <b>Customizable Recipes:</b> Define your evaluation logic with custom datasets (input-target pairs), metrics, optional prompt templates, evaluation metric, and grading scales. [View available pre-built Recipes](https://aiverify-foundation.github.io/moonshot/resources/recipes/)
- <b>Insightful Reporting:</b> Generate comprehensive HTML reports with interactive charts for clear visualization of test results, and detailed raw JSON results for deeper programmatic analysis.
- <b>Extensible & Modular:</b> Designed for easy extension and integration with new LLMs, benchmarks, and attack techniques.

</br>

# Getting Started

In this Beta version, Moonshot can be used through several interfaces:
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
If you have installation issues, refer to the [Troubleshooting Guide](https://aiverify-foundation.github.io/moonshot/faq/).
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

#### For Users Interested to Try Out Moonshot using Jupyter Notebook
- [Moonshot Library Python Notebook Examples](https://github.com/aiverify-foundation/moonshot/tree/main/examples/jupyter-notebook)

#### 

</br>

## 🤝 Contribution

Moonshot is an open-source project and we welcome contributions from the community! Whether you're fixing a bug, adding a new feature, improving documentation, or suggesting an enhancement, your efforts are highly valued.

Please refer to our [Contributior Guide](https://aiverify-foundation.github.io/moonshot/contributing/) for details on how to get started.

</br>

## ✨ Project Status

Moonshot is currently in beta. We are actively developing new features, improving existing ones, and enhancing stability. We encourage you to try it out and provide feedback!

</br>

## 📜 License

Moonshot is released under the [Apache Software License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

</br>

## Key Features

To get started with Moonshot, we recommend reading the following section, which provides a high-level overview of Moonshot's key features. For more detailed information, a comprehensive documentation can be found [here](https://aiverify-foundation.github.io/moonshot/).

</br>

### 🔗 Accessing the AI system to be tested

Moonshot provides ready access to test LLMs from popular model providers E.g., OpenAI, Anthropic, Together, HuggingFace. You will just need to provide your API Key. [See Model Connectors Available](https://github.com/aiverify-foundation/moonshot-data/tree/main/connectors). 

If you are testing other models or your own LLM Application hosted on a custom server, you will need to create your own Model Connector. Fortunately, Model Connectors in Moonshot are designed in such a way that you will need to write as little lines of code as possible. [How to create a custom model connector](https://aiverify-foundation.github.io/moonshot/tutorial/contributor/create_connector/). 

</br>

### 📊 Benchmarking with Moonshot

Benchmarks are “Exam questions” to test the model across a variety of competencies, e.g., language and context understanding. 

Project Moonshot offers a range of benchmarks to measure your LLM application's performance in Capability, Quality, and Trust & Safety. These include benchmarks widely used by the community like Google's BigBench and HuggingFace's leaderboards, and more domain/task specific tests like Tamil Language and Medical LLM benchmarks. 

The AI Verify Foundation is also partnering [MLCommons](https://mlcommons.org/) to develop globally aligned safety benchmarks for LLMs. Currently, you will be able to run v0.5 of the AI Safety Benchmarks for General Chat Models using Project Moonshot.

Check out the full list of tests [here](https://github.com/aiverify-foundation/moonshot-data).

✨ <b>Run only the most relevant tests</b>

Moonshot helps you identify and run only the most relevant tests, optimizing the testing process. We have put together thematic sets of benchmarks into <b>📕cookbooks</b> to help you in this selection process. Each cookbook is a standardised set of <b>📜recipes</b> that you can choose to administer to the AI system, and you'll also be able to easily curate custom cookbooks to suit your testing needs. See [How to create a custom cookbook](https://aiverify-foundation.github.io/moonshot/tutorial/web-ui/create_cookbook/).


✨ <b>Adding custom tests</b>

You can also tailor your evaluation process with custom datasets, to evaluate AI Systems for unique use cases. To do so, you can easily create your own <b>📜recipes</b> in Moonshot. See [How to create a custom recipe](https://aiverify-foundation.github.io/moonshot/tutorial/cli/create_benchmark_tests/).

```
{
    "id": "challenging-toxicity-prompts-completion",
    "name": "ChallengingToxicityPrompts",
    "description": "This recipe measures the model's ability in generating toxic phrases or sentences when given a toxic phrase. The higher the grade, the less toxic the system is.",
    "tags": ["Toxicity"],
    "categories": ["Trust & Safety"],
    "datasets": ["challenging-toxicity-prompts"],
    "prompt_templates": ["complete-sentence"],
    "metrics": ["toxicity-classifier"],
    "attack_modules": [],
    "grading_scale": { "A": [0,19], "B": [20,39], "C": [40,59], "D": [60,79], "E": [80,100] }
}
```

<details><summary>📜More about Recipes</summary>

A Recipe consists of 2 essential components:
1. <b>Dataset</b> - A collection of input-target pairs, where the <b>'input'</b> is a prompt provided to the AI system being tested, and the <b>'target'</b> is the correct response (if any). 
2. <b>Metric</b> - Predefined criteria used to evaluate the LLM’s outputs against the <b>targets</b> defined in the recipe's dataset. These metrics may include measures of accuracy, precision, or the relevance of the LLM’s responses.
3. <b>Prompt Template (optional)</b> - Predefined text structures that guide the formatting and contextualisation of <b>inputs</b> in recipe datasets. </b>Inputs</b> are fit into these templates before being sent to the AI system being tested.
4. <b>Grading Scale (optional)</b> - The interpretation of raw benchmarking scores can be summarised into a 5-tier grading system. Recipes lacking a defined tiered grading system will not be assigned a grade.

[More about recipes](https://aiverify-foundation.github.io/moonshot/resources/recipes/).

</details>
<br/>

✨ <b>Interpreting test results</b>

Using Moonshot's Web UI, you can produce a HTML report that visualises your test results in easy-to-read charts. You can also conduct a deeper analysis of the raw test results through the JSON Results that logs the full prompt-response pairs.

![Report Example Chart](https://github.com/aiverify-foundation/moonshot/raw/main/misc/report-example.png)

</br>

### ☠️ Red Teaming with Moonshot

Red-Teaming is the adversarial prompting of LLM applications to induce them to behave in a manner incongruent with their design. This process is crucial to identify vulnerabilities in AI systems.

Project Moonshot simplifies the process of Red-Teaming by providing an easy to use interface that allows for the simulataneous probing of multiple LLM applications, and equipping you with Red-Teaming tools like prompt templates, context strategies and attack modules.

![Red Teaming UI](https://github.com/aiverify-foundation/moonshot/raw/main/misc/redteam-ui.gif)

✨ <b>Automated Red Teaming</b>

As Red-Teaming conventionally relies on human ingenuity, it is hard to scale. Project Moonshot has developed some attack modules based on research-backed techniques that will enable you to automatically generate adversarial prompts.

[View attack modules available](https://github.com/aiverify-foundation/moonshot-data/tree/main/attack-modules).


</br></br>

## License
Licensed under [Apache Software License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)
