#

![moonshot logo](./res/aiverify-moonshot-logo.png)

# Introduction

Developed by the [AI Verify Foundation](https://aiverifyfoundation.sg/),  Moonshot is a tool to bring benchmarking and red teaming together to help AI developers, compliance teams test and evaluate their LLMs and LLM applications.

# What does Moonshot do?

Moonshot provides capabilities to test custom LLM applications or LLMs from popular model providers e.g., OpenAI, Anthropic, Together, HuggingFace. You will just need to provide your API Key.
If you are testing other models or your own LLM application hosted on a custom server, you will need to create your own Model Connector. Fortunately, Model Connectors in Moonshot are designed in such a way that you will need to write as few lines of code as possible.


## Benchmarks
Benchmarks are “exam questions” to test the model across a variety of competencies, e.g., language and context understanding.
Moonshot offers a range of benchmarks to measure your LLM application's performance in the categories of Capability, Quality, and Trust & Safety. These include benchmarks widely used by the community like Google's BigBench and HuggingFace's leaderboards, and more domain/task specific tests like Tamil Language and Medical LLM benchmarks.


### Starter Kit for LLM-based App Testing

The Starter Kit for LLM-based App Testing (Starter-Kit) is a set of voluntary guidelines developed by IMDA that coalesce rapidly emerging best practices and methodologies for LLM App testing. It covers four key risks commonly encountered in LLM Apps today – hallucination, undesirable content, data disclosure and vulnerability to adversarial prompts.


The Starter Kit includes two parts:

1. Testing guidance: Practical learnings from The Global AI Assurance Pilot, Industry workshops and inputs from the Cyber Security Agency of Singapore (CSA) and the Government Technology Agency of Singapore  (GovTech), who have developed and conducted AI tests for government  agencies and the industry. 

2. Recommended tests: An evolving list of benchmark tests, which are being incorporated here on Moonshot iteratively. The next few sections include guidance on running some of the publicly available tests. 

We recommend using the Starter Kit cookbooks in conjunction with the Starter Kit document for an effective understanding of considerations like test applicability, how to interpret the results, and so on. 

Further details on the available tests, and upcoming updates are available in the respective risk sections. 


**Starter Kit Cookbooks**

Currently, each risk area has a cookbook associated with it: 

- [Hallucination Cookbook](https://github.com/aiverify-foundation/moonshot-data/blob/main/cookbooks/hallucination.json)
- [Undesirable Content Cookbook](https://github.com/aiverify-foundation/moonshot-data/blob/main/cookbooks/undesirable-content.json)
- [Data Disclosure Cookbook](https://github.com/aiverify-foundation/moonshot-data/blob/main/cookbooks/data-disclosure.json)
- [Adversarial Prompts Cookbook](https://github.com/aiverify-foundation/moonshot-data/blob/main/cookbooks/adversarial-attacks.json)

The starter kit cookbooks follow the same structure as other cookbooks - for a refresher on cookbooks, recipes, datasets and metrics, please visit [the components of moonshot section here](components.md).


<!-- ![starterkit-components](./res/starter-kit-components.png) -->
<!-- ![starterkit-components](./res/starter-kit-components.png) -->

![starterkit-components](./res/starter-kit-components.png)

**Hallucination cookbook**

A set of tests that assess factual accuracy, namely general knowledge across different domains (e.g. math, law, sociology) and local facts about Singapore, such as iconic places and political history. Answers are expected to be multiple-choice or short-form. Currently, this cookbook includes the following tests:

| Test | Description | Expected format for the test (prompt/response) | Number of prompts |
|------|-------------|--------|-------------------|
| [**MMLU**](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/mmlu.json) | Measures ability to answer accurately across 57 tasks including elementary mathematics, US history, computer science, law, and more. The higher the grade, the better the system performs. | MCQ question with categorical response | 17,487 |
| [**Facts About Singapore**](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/singapore-facts.json) | Tests knowledge related to Singapore across 7 topics including political history, public housing, transport etc. Curated in-house | True/False and MCQ format with categorical response | 276 |

*Coming soon*

*Upcoming tests to be included in this cookbook include SimpleQA, CNN/DailyMail and others.*


**Undesirable content**

A set of tests that assess tendency to generate undesirable content, meaning content that inflicts harm on individuals, communities, or the public interest, such as socially harmful or legally prohibited content. It includes tests relating to toxicity, information on committing crimes, etc.

| Test | Description | Expected format for the test (prompt/response) | Number of prompts |
|------|-------------|-----------------------------------------------|-------------------|
| **[MLCommons AILuminate - Violent Crimes](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/mlc-vcr-en.json)** | Measures ability to respond without enabling, encouraging, or endorsing the commission of violent crimes. A high grade indicates that the system under test handles the response well. | Conversation questions/ instruction with open-ended responses, which are assessed using LLM-as-a-judge. For the current cookbook implementation, GPT4o as LLM-as-a-judge and there is a requirement to provide an OpenAI API key to run the recipe/cookbook. Please refer to the FAQ section for more details | 100 |
| **[MLCommons AILuminate - Non Violent Crimes](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/mlc-nvc.json)** | Measures ability to respond without enabling, encouraging, or endorsing the commission of non violent crimes. A high grade indicates that the system under test handles the response well. | Conversation questions/ instruction with open-ended responses, which are assessed using LLM-as-a-judge. For the current cookbook implementation, GPT4o as LLM-as-a-judge and there is a requirement to provide an OpenAI API key to run the recipe/cookbook. Please refer to the FAQ section for more details | 100 |
| **[Singapore Safety Questions](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/singapore-safety.json)** | Tests ability to respond safely to prompts related to culturally and legally sensitive situations in Singapore | Open-ended, assessed using llamaguardannotator | 59 |
| **[Real Toxicity Prompts](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/real-toxicity-prompts-completion.json)** | Measures ability to identify toxic sentences. The higher the grade, the less toxic the system is. | Open-ended, assess using toxicity classifier | 198,884 |

*Coming soon*

*Upcoming tests to be included in this cookbook include MLCommons AILuminate Hate, XSTest and others.*


**Data disclosure**

A set of tests that assess the tendency to disclose information that is commonly considered to be sensitive or aid requests to obtain such information in an unauthorised manner. It covers a variety of sensitive information types in realistic conversational style over various sentence formats.

| Test | Description | Expected format for the test (prompt/response) | Number of prompts |
|------|-------------|-----------------------------------------------|-------------------|
| **[MLCommons AILuminate - Privacy](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/mlc-prv-en.json)** | Same approach as violent crimes | Conversation questions/ instruction with open-ended responses, which are assessed using LLM-as-a-judge. For the current cookbook implementation, GPT4o as LLM-as-a-judge and there is a requirement to provide an OpenAI API key to run the recipe/cookbook. Please refer to the FAQ section for more details | 100 |

*Coming soon*

*Upcoming tests to be included in this cookbook include XSTest, SorryBench and others.*


**Adversarial Prompts Cookbook**

Tests for susceptibility to producing unsafe outputs (which may include incorrect content, undesirable content and/or sensitive information) when presented with intentional prompt attacks. It covers a range of prompt attack techniques across different risk categories.

| Test | Description | Expected format for the test (prompt/response) | Number of prompts |
|------|-------------|-----------------------------------------------|-------------------|
| **[CyberSecEval - Prompt Injections 3](https://github.com/aiverify-foundation/moonshot-data/blob/main/recipes/cyberseceval-en.json)** | Measures model's susceptibility to prompt injections, adapted from Purple Llama CyberSecEval benchmark NOTE: This test would soon be upgraded to match the CyberSecEval Prompt Injections v4 from PurpleLlama | Conversation questions/ instruction with open-ended responses, which are assessed using LLM-as-a-judge. For the current cookbook implementation, GPT4o as LLM-as-a-judge and there is a requirement to provide an OpenAI API key to run the recipe/cookbook. Please refer to the FAQ section for more details | 251 |


*Coming soon*

*Upcoming tests to be included in this cookbook include Cyberseceval 4 (version upgrade, Microsoft BIPIA and others.*

Refer to [getting started guide here](./getting_started/starter_kit.md) on how to run these tests for your model/application.

## Red Teaming
Red teaming is the adversarial prompting of LLM applications to induce them to behave in a manner incongruent with their design. This process is crucial to identify vulnerabilities in AI systems. Moonshot simplifies the process of red teaming by providing an easy to use interface that allows for the simultaneous probing of multiple LLM applications, and equipping you with red teaming utilities like prompt templates, context strategies and attack modules.

### Automated Red Teaming
As red teaming conventionally relies on human ingenuity, it is hard to scale. Moonshot has developed some attack modules based on research-backed techniques that will enable you to automatically generate adversarial prompts.

Learn more about components of Moonshot in the [next section](./components.md).