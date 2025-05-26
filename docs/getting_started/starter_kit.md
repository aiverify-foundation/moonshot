

The Starter Kit for LLM-based App Testing (Starter-Kit) is a set of voluntary guidelines developed by IMDA that coalesce rapidly emerging best practices and methodologies for LLM App testing. It covers four key risks commonly encountered in LLM Apps today – hallucination, undesirable content, data disclosure and vulnerability to adversarial prompts. For more details, please refer to [Introduction- Benchmarks- "Starter Kit for LLM-based App Testing"]().

This section will guide you through the steps to run the benchmark testing using IMDA's Starter Kit.

1. To begin, click the “Get Started” button.

![starterkit-landing](../res/sk-landing.png)

`2. Select your custom LLM application or model endpoint and click “Next”.

![starterkit-select-model](../res/sk-select-model.png)


`3. Update endpoint - Provide your API key in the “Token” field.

![starterkit-update-endpoint](../res/sk-update-endpoint.png)


`4. For this example, select “Data Disclosure” under “IMDA Starter Kit” section. This cookbook tests applications for risk against Data disclosure.

![starterkit-select-cookbook](../res/sk-select-cookbook.png)


`5. This test requires LLM as judge. We use OpenAI’s GPT4o in this case. “Configure” and provide your API key.

![starterkit-additional-requirements](../res/sk-additional-requirements.png)

`6. Provide a unique name for this test run, choose the number of prompts and click “Run”.

![starterkit-test-config](../res/sk-test-config.png)

`7. This should start running the test against Data Disclosure.

![starterkit-test-complete](../res/sk-test-complete.png)

`8. You may choose to download the report or detailed JSON.

![starterkit-download-report](../res/sk-download-report.png)


**How to interpret results:**

- The overall rating (A–E) is assigned based on the final score, calculated based on specific metric. For example, in this screenshot, the grade given to the model is A. 
- While these can be indicative and useful for comparison—especially if you’re testing multiple apps, models, or versions—please exercise your own judgment on what’s acceptable for your use case.
- The detailed JSON result includes more information about the test run including individual responses to every single prompt/input and associated response/output including the evaluation.






