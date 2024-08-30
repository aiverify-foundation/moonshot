# Running Benchmarks

1. Before you can start running benchmarks, provide the following info. These will be included in the report generated at the end of the run. 


    | Name        |Description   | Example          |
    |-------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
    | **Name** (Required)     | A unique name for you to identify this benchmark run by| `GPT4 vs Claude on safety benchmarks`  |
    | **Description** | Describe the purpose and scope of this benchmark run. | Comparing GPT4 and Claude to determine which model is safer as a chatbot |
    | **Run a smaller set** | The number of prompts per dataset, as specified in the recipe, to be run. Indicating 0 will run the full set. <br> <span style="font-size: 12px"><i>* Before running the full recommended set, you may want to run a smaller number of prompts from each recipe to do a sanity check.</i><span> | 5 |

2. Click ‘Run’ to start running the benchmarks. 

    ![Benchmark Initialisation](./imgs/run_benchmark(11).png)

3. You can click on ‘See Details’ to recap on what is currently being run. 

    ![Progress of Benchmark](./imgs/view_run_details(12).png)

4. A report will be generated once the run is completed. Meanwhile, you can:

    - Start Red Teaming to discover new vulnerabilities   
    - Create a custom cookbook by curating your own set of recipes   
    - Go back to home  

5. To view the progress of the run, click on the bell icon, then select the specific benchmark run.

    ![Progress of Multiple Runs](./imgs/run_progress(13).png)

6. Once run is completed, you can click on ‘View Report’ 

    ![View Report](./imgs/view_report(14).png)

7. One report will be generated for each endpoint tested. Click on the dropdown to toggle the report displayed. You can also download the HTML report and the detailed results as a JSON file. 

    ![Download Benchmark Report](./imgs/download_report(15).png)

8. You can also view the details of previous runs through: 
    1. Click on ‘history’ icon, then ‘View Past Runs’ 
    2. Click on ‘benchmarking’ icon, then ‘View Past Runs’ 