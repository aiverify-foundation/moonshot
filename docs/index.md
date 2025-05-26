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

We recommend using [the Starter Kit cookbooks](./detailed_guide/starter_kit_cookbooks.md) in conjunction with the Starter Kit document for an effective understanding of considerations like test applicability, how to interpret the results, and so on. 

Further details on the available tests, and upcoming updates are available in the respective risk sections. 

## Red Teaming
Red teaming is the adversarial prompting of LLM applications to induce them to behave in a manner incongruent with their design. This process is crucial to identify vulnerabilities in AI systems. Moonshot simplifies the process of red teaming by providing an easy to use interface that allows for the simultaneous probing of multiple LLM applications, and equipping you with red teaming utilities like prompt templates, context strategies and attack modules.

### Automated Red Teaming
As red teaming conventionally relies on human ingenuity, it is hard to scale. Moonshot has developed some attack modules based on research-backed techniques that will enable you to automatically generate adversarial prompts.

Learn more about components of Moonshot in the [next section](./components.md).