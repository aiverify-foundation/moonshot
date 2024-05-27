# Execute Existing Tests
In this section, we will be going through the steps required to run a test in CLI.

To run a test, you will need:

- **Endpoint Connector** - a configuration file to connect to your desired LLM endpoint
- **Cookbook/Recipe** - benchmarks you want to run TODO

For the following steps, they will be done in interactive mode in CLI. To activate interactive mode, enter `python -m moonshot cli interactive`
### Create an Endpoint Connector
1. To view all the endpoint connectors available, enter `list_endpoints`. If there is already an endpoint connector you want to use, you can skip to this TODO section. You will see a list of available endpoints:

    ![list of endpoints](cli_images/endpoints.png)

2. To understand more about creating an Endpoint Connector, enter `add_endpoint -h`. For example, to create an endpoint connector with the following configuration:

    - Connector type: `openai-connector` (Enter `list_connector_types -h` to view the connector types available)
    - Name of your endpoint connenctor (unique identifier): `my-openai-connector`
    - URI: `myendpointuri` (can set this to a random string like `none` if it is not required by your endpoint connector)
    - API token: `thisismysecretapitoken`
    - Max number of calls made to the endpoint per second: `2`
    - Max concurrency of the endpoint:`10`
    - Other parameters that this endpoint may need:
        - Temperature: 0.5
    
    The command would be: `add_endpoint openai-connector 'my-openai-connector' myendpointuri mythisismysecretapitoken 2 10 "{'temperature': 0.5}"`

3. After you've entered the command, you should the following if the endpoint connector is created successfully. Use `the view_endpoint` command to view your newly created endpoint connector:

    ![endpoint connected](cli_images/endpoint_created.png)


### Running a Test Using Our Predefined Cookbook
<!-- Moonshot comes with a list of cookbooks and recipes. A recipe contains one or more benchmark datasets and evaluation metrics. A cookbook contains one or more recipes. To execute an existing test, we can select either a recipe or cookbook.

In this tutorial, we will run a cookbook called leaderboard-cookbook. This cookbook contains a set of popular benchmarks (e.g., mmlu) that can be used to assess the capability of the model.

For the purpose of this tutorial, we will configure our runner to run 1 prompt from every recipe in this cookbook -->
Once your endpoint connector is created, we can start choosing the test we want to run. 

1. To view all the cookbooks available, enter `list_cookbooks`. You will see a list of available cookbooks:
    ![list of cookbooks](cli_images/cookbooks.png)

2. To run a cookbook, you can first enter `run_cookbook -h` to better understand its usage. For example, to run a cookbook with the following configuration:

    - Runner ID (`id` in `list_runners`): my-new-cookbook-runner (Enter `list_runners` to view the runners available. If you do not want to use an existing runner or do not have a runner yet, the `run_cookbook` command will create a runner for you using a slugified ID.)
    - ID of the cookbook (`ID` in `list_cookbooks`): `common-risk-easy`
    - Name of your endpoint connector (`Id` column in `list_endpoints`): `my-openai-connector` 
    - Number of prompts (TODO): `1` 
    - Random seed (TODO): `2`
    - System prompt: `This is a customised system prompt`
    - Runner and result proc (TODO)

    The command would be: `run_cookbook "my new cookbook runner" "['common-risk-easy']" "['my-openai-connector']" -n 1 -r 2 -s "This is a customised system prompt"`
    > **_NOTE:_**  You can run more than one cookbook and endpoint by adding them into the list( i.e. `"['common-risk-easy','common-risk-hard']"`)

3. Run your cookbook with the `run_cookbook` command. You should see a table of results from your run:
    ![cookbook run results](cli_images/cookbook_run.png)


### Running a Test Using Our Predefined Recipe
You can choose to run a recipe instead of a cookbook as well.

1. To view all the recipes available, enter `list_recipes`. You will see a list of available recipes:
    ![list of recipes](cli_images/recipes.png)


2. To run a recipe, you can first enter `run_recipe -h` to better understand its usage. For example, to run a recipe with the following configuration:

    - Runner ID (`id` in `list_runners`): my-new-recipe-runner (Enter `list_runners` to view the runners available. If you do not want to use an existing runner or do not have a runner yet, the `run_recipe` command will create a runner for you using a slugified ID.)
    - ID of the recipes (`ID` in `list_recipes`): `auto-categorisation` and `winobias`
    - Name of your endpoint connector (`Id` column in `list_endpoints`): `my-openai-connector` 
    - Number of prompts (TODO): `1` 
    - Random seed (TODO): `2`
    - System prompt: `This is a customised system prompt`
    - Runner and result proc (TODO)

    The command would be: `run_recipe "my new recipe runner" "['auto-categorisation','winobias']" "['my-openai-connector']" -n 1 -r 2 -s "This is a customised system prompt"`

3. Run your recipe with the `run_recipe` command. You should see a table of results from your run:
    ![recipe run results](cli_images/recipe_run.png)
