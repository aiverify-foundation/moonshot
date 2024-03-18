# Moonshot

Moonshot is a comprehensive Large Language Model (LLM) Evaluation tool designed to address the challenge faced by developers and system owners in benchmarking large language models (LLMs) and testing their LLM applications against a baseline set of risks. It provides a platform for thorough evaluation and testing, ensuring the reliability and effectiveness of LLM applications.

## Model Connectors

Model Connectors in Moonshot enable users to integrate new models into the toolkit by connecting to their Large Language Models (LLMs) via API connectors. This feature empowers users to create and modify LLM endpoints within Moonshot, facilitating customized testing and benchmarking scenarios tailored to their specific needs.

## During a Run

During a run in Moonshot, the toolkit executes the selected Cookbook and interacts with the model endpoints chosen by the users. This process allows for the evaluation of LLM applications against predefined benchmarks and test scenarios.

## Cookbook

The Cookbook in Moonshot contains one or more recipes, each designed to generate results when selected to run with the model endpoints. It serves as a comprehensive guide for conducting evaluations and tests, offering a structured approach to assessing LLM applications' performance and addressing potential risks.

## Recipe

A Recipe in Moonshot consists of three essential components:

- Dataset: The dataset used for evaluation, providing the input data for testing LLM applications.
- Metric Mechanism: The metric mechanism defines the criteria and metrics used to assess the performance of LLM applications, ensuring consistent and objective evaluation.
- Pre-post prompt Template: The pre-post prompt template outlines the prompts provided to the LLM applications before and after the evaluation process, guiding their responses and facilitating standardized testing procedures.

## Red Teaming

Red Teaming serves as a valuable tool within the toolkit, aimed at aiding and simplifying the process of probing large language models (LLMs) to enhance the reliability and security of LLM applications. It facilitates structured testing procedures to identify vulnerabilities and improve overall system robustness.

## Session

A Session feature allows users to initiate interactions with selected models, enabling them to engage in chats and send prompts to red team the models. Sessions provide a controlled environment for conducting testing and evaluation activities, ensuring systematic and organized testing procedures.

## Chat

A Chat refers to an interaction directed to a specific model within a session, initiating the red teaming prompt process. Users can communicate with individual models, sending prompts and assessing their responses to identify potential vulnerabilities and areas for improvement in LLM applications.