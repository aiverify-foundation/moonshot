In this tutorial, we will guide you through the process of conducting Red Teaming in Project Moonshot.

As a user, you may want to test your Large Language Model (LLM) applications in adversarial scenarios to identify potential vulnerabilities. Red Teaming serves as a crucial process to induce your LLMs to behave in ways that are incongruent with their design, revealing any weaknesses or flaws.

Project Moonshot simplifies Red Teaming by providing an intuitive interface that allows for simultaneous probing of multiple LLM applications. It also equips you with Red Teaming tools like prompt templates, context strategies, and attack modules. 

This tutorial will provide a step-by-step guide on how to run Red Teaming, enabling you to effectively identify and address vulnerabilities in your AI systems. Let's get started on your first Red Teaming session.

1. Start by navigating to the 'Discover new vulnerabilities' section.

![Navigate to Discover new vulnerabilities](./res/run_rt_1.png)

2. On this page, you are prompted to select an endpoint for testing. You have the option to create a new endpoint or modify an existing one. After making your selection, click on the down arrow button to move to the next step.

![Endpoint selection page](./res/run_rt_2.png)

3. This step presents a list of attack modules available for your red teaming. For the purpose of this tutorial, select 'skip for now'.

![Attack modules selection page](./res/run_rt_3.png)

4. You are now required to complete a form on this page. After filling out the form, initiate a red teaming session by clicking on 'Start'.

![Form completion page](./res/run_rt_4.png)

5. You have now entered a session to conduct your red teaming. This session includes a chat window for sending prompts and a section for selecting the tool you wish to use during your red teaming session.

![Red teaming session page](./res/run_rt_5.png)

#### Manual Red Teaming
During manual red teaming, you have the option to utilize tools like Prompt Templates and Context Strategy. These tools assist in structuring and providing context to your prompts.

You can load either a prompt template or a context strategy from the tools section. 
After making your selection, input your prompt into the chat window. You will then observe the enhancements that have been incorporated into your prompt.
![Automated Red Teaming](./res/manual_rt.gif)

#### Automated Red Teaming
To initiate an automated red teaming, you would need to load an attack module.

Navigate to the 'Attack Module' within the tools section. Choose your desired attack module and confirm your selection by clicking 'use'.

![Load Attack Module](./res/load_am.gif)

Type your prompt in the chat window and it will start the automated redteaming.

![Automated Red Teaming](./res/auto_rt.gif)
