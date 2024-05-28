
In this tutorial, we will guide you through the process of running a benchmark test in Project Moonshot. 

As a user, you may want to assess your Large Language Model (LLM) application's performance across various competencies such as language and context understanding. Benchmarks serve as "exam questions" for your model, providing a comprehensive evaluation of its capabilities.

Project Moonshot offers a wide range of benchmarks, including widely recognized ones like Google's BigBench and HuggingFace's leaderboards, as well as more domain/task-specific tests like Tamil Language and Medical LLM benchmarks.

This tutorial will provide a step-by-step guide on how to run these benchmark tests, enabling you to measure your LLM application's performance in Capability, Quality, and Trust & Safety. Let's get started on running your first benchmark test.

1. Begin by navigating to the 'Evaluate against standard tests' section.
![Navigate to Evaluate against standard tests](./res/run_bm_1.png)

2. Here, a list of recommended cookbooks has been pre-selected for you. Feel free to select or deselect any cookbook that you wish to run. Once you've made your selection, click the down arrow button to proceed to the next step.
![Select or deselect cookbooks](./res/run_bm_2.png)

3. This page displays the total number of prompts that will be tested based on the cookbooks you've selected. To view all available cookbooks, click on 'these cookbooks'.
![View total number of prompts](./res/run_bm_3.png)

4. On this page, all cookbooks are sorted by their category. To select a cookbook, click on the corresponding checkbox. For more information about a cookbook, click on 'About'. Once you've finished, click 'OK'.
![View and select cookbooks](./res/run_bm_4.png)

5. You will be redirected back to the page showing the total number of prompts. To proceed to the next step, click the down arrow button.
![Proceed to the next step](./res/run_bm_5.png)

6. Here, you are required to select an endpoint for testing. If needed, you can create a new endpoint or edit an existing one on this page. After selecting an endpoint, click on the down arrow button to proceed to the next step.
![Select an endpoint](./res/run_bm_6.png)

    !!!warning
        Before proceeding, please ensure that you have your Together Llama Guard 7B Assistant endpoint token set up. This is necessary to run the MLCommon cookbook.

7. On this page, you need to fill out the form. If you wish to test a smaller dataset, replace the value in the 'Run a smaller set' field. By default, the value is 0, which means the entire cookbook will be run. By entering a value, you can specify the number of prompts to be tested from each recipe. Once you've completed the form, click on 'Run' to start the test.
![Fill out the form and start the test](./res/run_bm_7.png)

8. The benchmark test is now running. You can click on 'see details' to view the endpoints and cookbooks that are currently running. If you wish to exit an ongoing run, click on 'cancel'.
![View test details or cancel the run](./res/run_bm_8.png)

9. You can safely close the window while the benchmark is running; it will continue to operate in the background. To check the status of your run, click on the bell icon. If you wish to view more details about the run, simply click on the run itself.
![View test](./res/run_bm_9.png)

10. After the benchmark test has finished, you can access the results by clicking on 'View Report'.
![View report](./res/run_bm_10.png)
