# Moonshot

Developed by the [AI Verify Foundation](https://aiverifyfoundation.sg/?utm_source=Github&utm_medium=referral&utm_campaign=20230607_AI_Verify_Foundation_GitHub), [Moonshot](https://github.com/aiverify-foundation/moonshot/pull/new/update_readme_link) is one of the first tools to bring benchmarking and red teaming together to help AI developers, compliance teams and AI system owners test and evaluate their LLMs and LLM applications.

## What does Moonshot do?

Moonshot provides ready access to test LLMs from popular model providers e.g., OpenAI, Anthropic, Together, HuggingFace. You will just need to provide your API Key.

If you are testing other models or your own LLM application hosted on a custom server, you will need to create your own Model Connector. Fortunately, Model Connectors in Moonshot are designed in such a way that you will need to write as few lines of code as possible.

### Benchmark

Benchmarks are “exam questions” to test the model across a variety of competencies, e.g., language and context understanding.

Moonshot offers a range of benchmarks to measure your LLM application's performance in the categories of Capability, Quality, and Trust & Safety. These include benchmarks widely used by the community like Google's BigBench and HuggingFace's leaderboards, and more domain/task specific tests like Tamil Language and Medical LLM benchmarks.

### Red Teaming

Red teaming is the adversarial prompting of LLM applications to induce them to behave in a manner incongruent with their design. This process is crucial to identify vulnerabilities in AI systems.

Moonshot simplifies the process of red teaming by providing an easy to use interface that allows for the simultaneous probing of multiple LLM applications, and equipping you with red teaming utilities like prompt templates, context strategies and attack modules.

#### Automated Red Teaming

As red teaming conventionally relies on human ingenuity, it is hard to scale. Moonshot has developed some attack modules based on research-backed techniques that will enable you to automatically generate adversarial prompts.

## Glossary
Here are some common terms that may be used in this documentation:

| Term | Description |
| --- | ---|
| Connector | A **Connector** in Moonshot enables users to integrate new models into the toolkit by connecting to their Large Language Models (LLMs) via API connectors.  |
| Cookbook | A **Cookbook** in Moonshot contains one or more recipes, each designed to generate results when selected to run with the model endpoints. It serves as a comprehensive guide for conducting evaluations and tests, offering a structured approach to assessing LLM applications' performance and addressing potential risks. |
| Recipe | A **Recipe** in Moonshot brings together 3 essential components. A recipe can contain one or more datasets, prompt templates and metrics.  |
| Datasets | **Datasets** consist of a collection of input-target pairs, where the 'input' is a prompt provided to the LLM (being tested), and the 'target' is the correct response or ground truth. | 
| Session | A **Session** feature allows users to initiate interactions with selected models, enabling them to engage in chats and send prompts to red team the models.  | 
| Chat | A **Chat** refers to an interaction directed to a specific model within a session, initiating the red teaming prompt process. Users can communicate with individual models, sending prompts and assessing their responses to identify potential vulnerabilities and areas for improvement in LLM applications. | 
