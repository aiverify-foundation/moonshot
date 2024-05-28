# Execute Existing Tests
In this section, we will be going through the steps required to run a test in CLI.

To run a test, you will need:

- **Connector Endpoint** - a configuration file to connect to your desired LLM endpoint
- **Cookbook/Recipe** - benchmarks you want to run TODO

For the following steps, they will be done in interactive mode in CLI. To activate interactive mode, enter `python -m moonshot cli interactive`

### Select a Connector Endpoint
If we do not have a connector endpoint you need, check out the guide [here](connecting_endpoints.md) to create one yourself.


### Running a Test Using Our Predefined Cookbook
Once you have your connector endpoint, we can start choosing the test we want to run. 

1. To view all the cookbooks available, enter `list_cookbooks`. You will see a list of available cookbooks:

    ![list of cookbooks](cli_images/cookbooks.png)

2. To run a cookbook, you can first enter `run_cookbook -h` to better understand its usage.
    - Example: `run_cookbook "my new cookbook runner" "['common-risk-easy']" "['my-openai-connector']" -n 1 -r 2 -s "This is a customised system prompt"`: 

        - Runner ID (`id` in `list_runners`): my-new-cookbook-runner (Enter `list_runners` to view the runners available. If you do not want to use an existing runner or do not have a runner yet, the `run_cookbook` command will create a runner for you using a slugified ID.)
        - ID of the cookbook (`ID` in `list_cookbooks`): `common-risk-easy`
        - ID of your connector endpoint (`Id` column in `list_endpoints`): `my-openai-connector` 
        - Number of prompts (Optional TODO): `1` 
        - Random seed (Optional TODO): `2`
        - System prompt (Optional system prompt which overwrites our default system prompt): `This is a customised system prompt`

    > **_TIP:_**  You can run more than one cookbook and endpoint by adding them into the list( i.e. `"['common-risk-easy','common-risk-hard']"`)

3. Run your cookbook with the `run_cookbook` command. You should see a table of results from your run:

    ![cookbook run results](cli_images/cookbook_run.png)


### Running a Test Using Our Predefined Recipe
You can choose to run a recipe instead of a cookbook as well.

1. To view all the recipes available, enter `list_recipes`. You will see a list of available recipes:

    ![list of recipes](cli_images/recipes.png)


2. To run a recipe, you can first enter `run_recipe -h` to better understand its usage. For example, to run a recipe with the following configuration:

    - Runner ID (`id` in `list_runners`): my-new-recipe-runner (Enter `list_runners` to view the runners available. If you do not want to use an existing runner or do not have a runner yet, the `run_recipe` command will create a runner for you using a slugified ID.)
    - ID of the recipes (`ID` in `list_recipes`): `auto-categorisation` and `winobias`
    - Name of your connector endpoint (`Id` column in `list_endpoints`): `my-openai-connector` 
    - Number of prompts (TODO): `1` 
    - Random seed (TODO): `2`
    - System prompt: `This is a customised system prompt`
    - Runner and result proc (TODO)

    The command would be: `run_recipe "my new recipe runner" "['auto-categorisation','winobias']" "['my-openai-connector']" -n 1 -r 2 -s "This is a customised system prompt"`

3. Run your recipe with the `run_recipe` command. You should see a table of results from your run:

    ![recipe run results](cli_images/recipe_run.png)
