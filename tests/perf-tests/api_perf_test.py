import asyncio
import os
import shutil

from pyinstrument import Profiler

from moonshot.api import (
    api_create_connector_from_endpoint,
    api_create_connectors_from_endpoints,
    api_create_cookbook,
    api_create_endpoint,
    api_create_recipe,
    api_create_runner,
    api_create_session,
    api_delete_attack_module,
    api_delete_context_strategy,
    api_delete_cookbook,
    api_delete_dataset,
    api_delete_endpoint,
    api_delete_metric,
    api_delete_prompt_template,
    api_delete_recipe,
    api_delete_result,
    api_delete_runner,
    api_delete_session,
    api_get_all_attack_module_metadata,
    api_get_all_attack_modules,
    api_get_all_chats_from_session,
    api_get_all_connector_type,
    api_get_all_context_strategies,
    api_get_all_context_strategy_metadata,
    api_get_all_cookbook,
    api_get_all_cookbook_name,
    api_get_all_datasets,
    api_get_all_datasets_name,
    api_get_all_endpoint,
    api_get_all_endpoint_name,
    api_get_all_metric,
    api_get_all_metric_name,
    api_get_all_prompt_template_detail,
    api_get_all_prompt_template_name,
    api_get_all_recipe,
    api_get_all_recipe_name,
    api_get_all_result,
    api_get_all_result_name,
    api_get_all_run,
    api_get_all_runner,
    api_get_all_runner_name,
    api_get_all_session_metadata,
    api_get_all_session_names,
    api_get_available_session_info,
    api_load_runner,
    api_load_session,
    api_read_cookbook,
    api_read_cookbooks,
    api_read_endpoint,
    api_read_recipe,
    api_read_recipes,
    api_read_result,
    api_read_results,
    api_read_runner,
    api_set_environment_variables,
    api_update_attack_module,
    api_update_context_strategy,
    api_update_cookbook,
    api_update_cs_num_of_prev_prompts,
    api_update_endpoint,
    api_update_metric,
    api_update_prompt_template,
    api_update_recipe,
    api_update_system_prompt,
)
from moonshot.src.utils.timeit import timeit

# Ensure the 'perf' directory exists
perf_dir = "tests/perf-tests/perf"
os.makedirs(perf_dir, exist_ok=True)


# Common function to profile an async function with arguments using pyinstrument
async def profile_async_function(func, func_name, *args, **kwargs):
    profiler = Profiler(async_mode="enabled")
    profiler.start()

    # Call the async function with provided arguments
    await func(*args, **kwargs)

    profiler.stop()

    # Save the profiling output to a file
    stats_file = os.path.join(perf_dir, f"{func_name}_profile.txt")
    with open(stats_file, "w") as f:
        f.write(profiler.output_text(unicode=True, color=False))


# Common function to profile a given function with arguments
@timeit
def profile_function(func, func_name, *args, **kwargs):
    """
    Profiles the execution of a function by measuring its runtime and resource usage.

    This function wraps the execution of a given function `func` with a profiler, which
    measures various statistics such as execution time and memory usage. The profiling
    results are then written to a text file named after the function being profiled.

    Args:
        func (Callable): The function to profile.
        func_name (str): The name of the function, used for naming the output file.
        *args: Variable length argument list to pass to the function being profiled.
        **kwargs: Arbitrary keyword arguments to pass to the function being profiled.
    """
    profiler = Profiler(async_mode="enabled")
    profiler.start()

    # Call the function with provided arguments
    func(*args, **kwargs)

    profiler.stop()

    # Save the profiling output to a file
    stats_file = os.path.join(perf_dir, f"{func_name}_profile.txt")
    with open(stats_file, "w") as f:
        f.write(profiler.output_text(unicode=True, color=False))


def profile_api_connector():
    """
    Profiles the performance of various API connector functions.

    This function profiles the performance of API connector creation and retrieval functions.
    It uses predefined example connector IDs to profile the creation of a single connector
    and multiple connectors from endpoints. It also profiles the retrieval of all connector types.
    The profiling is done by calling the `profile_function` with the appropriate API function
    and arguments.
    """
    # Example connector_id to use for profiling
    example_connector_id = "openai-gpt4"
    example_connector_ids = [
        "claude2",
        "huggingface-gpt2",
        "huggingface-llama2-13b-gptq",
        "openai-gpt4",
        "openai-gpt35-turbo-16k",
        "openai-gpt35-turbo",
        "together-llama-guard-8b-assistant",
        "together-llama3-8b-chat-hf",
    ]

    # For functions that require arguments, pass them as needed
    profile_function(
        api_create_connector_from_endpoint,
        "api_create_connector_from_endpoint",
        example_connector_id,
    )
    profile_function(
        api_create_connectors_from_endpoints,
        "api_create_connectors_from_endpoints",
        example_connector_ids,
    )
    profile_function(api_get_all_connector_type, "api_get_all_connector_type")


def profile_api_connector_endpoint():
    """
    Profiles the performance of various API connector endpoint functions.

    This function profiles the performance of API endpoint creation, reading, updating, and deletion functions.
    It uses predefined example endpoint details to profile the creation of an endpoint with specific parameters.
    It also profiles the reading of an endpoint, updating an endpoint with new URI and token,
    and finally the deletion of an endpoint.

    The profiling is done by calling the `profile_function` with the appropriate API function and arguments.
    """
    # For functions that require arguments, pass them as needed
    profile_function(
        api_create_endpoint,
        "api_create_endpoint",
        name="My New GPT4",
        connector_type="openai-connector",
        uri="1234",
        token="1234",
        max_calls_per_second=256,
        max_concurrency=1,
        params={"hello": "world"},
    )
    profile_function(api_read_endpoint, "api_read_endpoint", "my-new-gpt4")
    profile_function(
        api_update_endpoint,
        "api_update_endpoint",
        "my-new-gpt4",
        uri="4567",
        token="4567",
        params={"hello": "world1"},
    )
    profile_function(api_get_all_endpoint, "api_get_all_endpoint")
    profile_function(api_get_all_endpoint_name, "api_get_all_endpoint_name")
    profile_function(api_delete_endpoint, "api_delete_endpoint", "my-new-gpt4")


def profile_api_context_strategy():
    """
    Profiles the performance of various API context strategy functions.

    This function profiles the performance of API context strategy creation, reading, updating, and deletion functions.
    It uses predefined example context strategy details to profile the creation of a context strategy with
    specific parameters.

    It also profiles the reading of a context strategy, updating a context strategy with new parameters,
    and finally the deletion of a context strategy.

    The profiling is done by calling the `profile_function` with the appropriate API function and arguments.
    """
    source_path = "moonshot/data/context-strategy/add_previous_prompt.py"
    destination_path = "moonshot/data/context-strategy/add_previous_prompt_copy.py"
    shutil.copy(source_path, destination_path)

    profile_function(api_get_all_context_strategies, "api_get_all_context_strategies")
    profile_function(
        api_get_all_context_strategy_metadata, "api_get_all_context_strategy_metadata"
    )
    profile_function(
        api_delete_context_strategy,
        "api_delete_context_strategy",
        "add_previous_prompt_copy",
    )


def profile_api_cookbook():
    """
    Profiles the performance of various API cookbook functions.

    This function profiles the performance of API cookbook creation, reading, updating, and deletion functions.
    It uses predefined example cookbook details to profile the creation of a cookbook with specific parameters.

    It also profiles the reading of a cookbook, reading multiple cookbooks by their names, updating a cookbook
    with new parameters, and finally the deletion of a cookbook.

    The profiling is done by calling the `profile_function` with the appropriate API function and arguments.
    """
    profile_function(
        api_create_cookbook,
        "api_create_cookbook",
        name="my new cookbook",
        description="This is a cookbook that consists of a subset of Bias Benchmark for QA (BBQ) recipes for age.",
        recipes=["my-recipe1", "my-recipe2"],
    )
    profile_function(api_read_cookbook, "api_read_cookbook", "my-new-cookbook")
    profile_function(
        api_read_cookbooks,
        "api_read_cookbooks",
        ["my-new-cookbook", "my-new-cookbook", "my-new-cookbook"],
    )
    profile_function(
        api_update_cookbook,
        "api_update_cookbook",
        "my-new-cookbook",
        name="my new cookbook 1234",
        recipes=["my-recipe2", "my-recipe5"],
    )
    profile_function(api_get_all_cookbook, "api_get_all_cookbook")
    profile_function(api_get_all_cookbook_name, "api_get_all_cookbook_name")
    profile_function(api_delete_cookbook, "api_delete_cookbook", "my-new-cookbook")


def profile_api_dataset():
    """
    Profiles the performance of various API dataset functions.

    This function profiles the performance of dataset-related API functions such as retrieving all datasets,
    retrieving all dataset names, and deleting a specific dataset. It uses the `profile_function` utility
    to measure the execution time of these API calls and logs the results for analysis.
    """
    source_path = "moonshot/data/datasets/cvalues.json"
    destination_path = "moonshot/data/datasets/cvalues1234.json"
    shutil.copy(source_path, destination_path)

    profile_function(api_get_all_datasets, "api_get_all_datasets")
    profile_function(api_get_all_datasets_name, "api_get_all_datasets_name")
    profile_function(api_delete_dataset, "api_delete_dataset", "cvalues1234")


def profile_api_environment_variables():
    """
    Profiles the performance of setting environment variables through the API.

    This function profiles the performance of the `api_set_environment_variables` function,
    which is responsible for setting the environment variables for the current session.
    It uses the `profile_function` utility to measure the execution time of this API call
    and logs the results for analysis.
    """
    profile_function(
        api_set_environment_variables,
        "api_set_environment_variables",
        {
            "ATTACK_MODULES": "moonshot/data/attack-modules",
            "CONNECTORS": "moonshot/data/connectors",
            "CONNECTORS_ENDPOINTS": "moonshot/data/connectors-endpoints",
            "CONTEXT_STRATEGY": "moonshot/data/context-strategy",
            "COOKBOOKS": "moonshot/data/cookbooks",
            "DATABASES": "moonshot/data/generated-outputs/databases",
            "DATABASES_MODULES": "moonshot/data/databases-modules",
            "DATASETS": "moonshot/data/datasets",
            "IO_MODULES": "moonshot/data/io-modules",
            "METRICS": "moonshot/data/metrics",
            "PROMPT_TEMPLATES": "moonshot/data/prompt-templates",
            "RECIPES": "moonshot/data/recipes",
            "RESULTS": "moonshot/data/generated-outputs/results",
            "RESULTS_MODULES": "moonshot/data/results-modules",
            "RUNNERS": "moonshot/data/generated-outputs/runners",
            "RUNNERS_MODULES": "moonshot/data/runners-modules",
        },
    )


def profile_api_metrics():
    """
    Profiles the performance of various API metric functions.

    This function profiles the performance of metric-related API functions such as retrieving all metric names,
    deleting a specific metric, and retrieving all metrics. It uses the `profile_function` utility to measure
    the execution time of these API calls and logs the results for analysis.
    """
    source_path = "moonshot/data/metrics/bertscore.py"
    destination_path = "moonshot/data/metrics/bertscore1.py"
    shutil.copy(source_path, destination_path)

    profile_function(api_get_all_metric_name, "api_get_all_metric_name")
    profile_function(api_get_all_metric, "api_get_all_metric")
    profile_function(api_delete_metric, "api_delete_metric", "bertscore1")


def profile_api_prompt_template():
    """
    Profiles the performance of various API prompt template functions.

    This function profiles the performance of API prompt template retrieval, updating, and deletion functions.
    It uses the `profile_function` utility to measure the execution time of these API calls and logs the results
    for analysis. It includes profiling for getting all prompt template details, getting all prompt template names,
    and deleting a specific prompt template.
    """
    source_path = "moonshot/data/prompt-templates/analogical-similarity.json"
    destination_path = "moonshot/data/prompt-templates/analogical-similarity1.json"
    shutil.copy(source_path, destination_path)

    profile_function(
        api_get_all_prompt_template_detail, "api_get_all_prompt_template_detail"
    )
    profile_function(
        api_get_all_prompt_template_name, "api_get_all_prompt_template_name"
    )
    profile_function(
        api_delete_prompt_template,
        "api_delete_prompt_template",
        "analogical-similarity1",
    )


def profile_api_recipe():
    """
    Profiles the performance of various API recipe functions.

    This function profiles the performance of API recipe creation, reading, updating, and deletion functions.
    It uses predefined example recipe details to profile the creation of a recipe with specific parameters.

    It also profiles the reading of a recipe, reading multiple recipes by their names, updating a recipe with
    new parameters, and finally the deletion of a recipe.

    The profiling is done by calling the `profile_function` with the appropriate API function and arguments.
    """
    profile_function(
        api_create_recipe,
        "api_create_recipe",
        name="my new recipe",
        description=(
            "Consists of adversarially perturned and benign MNLI and MNLIMM datasets. MNLI consists is a "
            "crowd-sourced collection of sentence pairs with textual entailment annotations. Given a premise sentence "
            "and a hypothesis sentence, the task is to predict whether the premise entails the hypothesis."
        ),
        tags=["robustness"],
        categories=["new"],
        datasets=["arc-easy", "bbq-lite-age-ambiguous"],
        prompt_templates=["prompt-template1"],
        metrics=["metrics1", "metrics2"],
        attack_modules=["charswap_attack", "homoglyph_attack"],
        grading_scale={
            "A": [0, 19],
            "B": [20, 39],
            "C": [40, 59],
            "D": [60, 79],
            "E": [80, 100],
        },
    )
    profile_function(api_read_recipe, "api_read_recipe", "my-new-recipe")
    profile_function(
        api_read_recipes,
        "api_read_recipes",
        ["my-new-recipe", "advglue", "analogical-similarity"],
    )
    profile_function(
        api_update_recipe,
        "api_update_recipe",
        "my-new-recipe",
        description="my new description.",
        tags=["fairness"],
        datasets=["analogical-similarity", "bbq-lite-age-disamb"],
        prompt_templates=["prompt-template2"],
        metrics=["metrics3"],
    )
    profile_function(api_get_all_recipe, "api_get_all_recipe")
    profile_function(api_get_all_recipe_name, "api_get_all_recipe_name")
    profile_function(api_delete_recipe, "api_delete_recipe", "my-new-recipe")


def profile_api_red_teaming():
    """
    Profiles the performance of various API red teaming functions.

    This function profiles the performance of API red teaming operations such as retrieving all attack module metadata,
    retrieving all attack modules, and deleting an attack module. It uses the `profile_function` to measure the
    execution time and resource usage of these operations.

    The profiling helps in understanding the efficiency of the red teaming API functions and identifying potential
    bottlenecks or areas for optimization.
    """
    source_path = "moonshot/data/attack-modules/charswap_attack.py"
    destination_path = "moonshot/data/attack-modules/charswap_attack1.py"
    shutil.copy(source_path, destination_path)

    profile_function(
        api_get_all_attack_module_metadata, "api_get_all_attack_module_metadata"
    )
    profile_function(api_get_all_attack_modules, "api_get_all_attack_modules")
    profile_function(
        api_delete_attack_module, "api_delete_attack_module", "charswap_attack1"
    )


def profile_api_result():
    """
    Profiles the performance of various API result functions.

    This function profiles the performance of API result operations such as reading individual results,
    reading multiple results, retrieving all results, and deleting results.

    It uses the `profile_function` to measure the execution time and resource usage of these operations.

    The profiling helps in understanding the efficiency of the result API functions and identifying potential
    bottlenecks or areas for optimization.
    """
    source_path = "tests/results/my-new-runner-recipe.json"
    destination_path = (
        "moonshot/data/generated-outputs/results/my-new-runner-recipe.json"
    )
    shutil.copy(source_path, destination_path)
    source_path = "tests/results/my-new-runner-cookbook.json"
    destination_path = (
        "moonshot/data/generated-outputs/results/my-new-runner-cookbook.json"
    )
    shutil.copy(source_path, destination_path)

    profile_function(api_read_result, "api_read_result", "my-new-runner-recipe")
    profile_function(
        api_read_results,
        "api_read_results",
        ["my-new-runner-recipe", "my-new-runner-cookbook"],
    )
    profile_function(api_get_all_result, "api_get_all_result")
    profile_function(api_get_all_result_name, "api_get_all_result_name")
    profile_function(api_delete_result, "api_delete_result", "my-new-runner-recipe")
    profile_function(api_delete_result, "api_delete_result", "my-new-runner-cookbook")


def profile_api_run():
    """
    Profiles the performance of various API run functions.

    This function profiles the performance of API run operations such as creating a runner, loading a runner,
    running a benchmark recipe runner, and cancelling a run. It uses the `profile_function` to measure the
    execution time and resource usage of these operations.

    The profiling helps in understanding the efficiency of the run API functions and identifying potential
    bottlenecks or areas for optimization.
    """
    profile_function(api_get_all_run, "api_get_all_run")


def _runner_callback_fn(progress_args: dict):
    """
    Callback function to be called during runner operations to report progress.

    This function is intended to be used as a callback during long-running operations
    to provide feedback on the progress of the operation. It prints out a formatted
    message containing the progress information.

    Parameters:
    progress_args (dict): A dictionary containing progress information.
    """
    print("=" * 100)
    print("PROGRESS CALLBACK FN: ", progress_args)
    print("=" * 100)


def profile_api_runner():
    """
    Profiles the performance of various API runner functions.

    This function profiles the performance of API runner operations such as creating a runner, loading a runner,
    reading runner details, and deleting a runner. It uses the `profile_function` to measure the execution time
    and resource usage of these operations.

    The profiling helps in understanding the efficiency of the runner API functions and identifying potential
    bottlenecks or areas for optimization.
    """
    profile_function(
        api_create_runner,
        "api_create_runner",
        name="my new runner",
        endpoints=["openai-gpt35-turbo", "openai-gpt35-turbo-16k"],
        description="My New Runner...",
        progress_callback_func=_runner_callback_fn,
    )
    profile_function(
        api_load_runner,
        "api_load_runner",
        "my-new-runner",
        progress_callback_func=_runner_callback_fn,
    )
    profile_function(api_read_runner, "api_read_runner", "my-new-runner")
    profile_function(api_get_all_runner, "api_get_all_runner")
    profile_function(api_get_all_runner_name, "api_get_all_runner_name")
    profile_function(api_delete_runner, "api_delete_runner", "my-new-runner")


# Function to run the profiling for the run_red_teaming method
async def profile_run_red_teaming(runner):
    """
    Profiles the `run_red_teaming` method of a given runner.

    This function asynchronously profiles the `run_red_teaming` method, which simulates red teaming
    attack strategies against a system. It measures the execution time and resource usage of the method
    by invoking `profile_async_function`.

    Args:
        runner: The runner instance on which `run_red_teaming` will be invoked.
    """
    rt_arguments = {
        "attack_strategies": [
            {
                "attack_module_id": "sample_attack_module",
                "prompt": "hello world",
                "system_prompt": "test system prompt",
                "context_strategy_info": [
                    {
                        "context_strategy_id": "add_previous_prompt",
                        "num_of_prev_prompts": 4,
                    }
                ],
                "prompt_template_ids": ["analogical-similarity"],
            }
        ]
    }

    await profile_async_function(
        runner.run_red_teaming, "run_red_teaming", rt_arguments
    )


# Function to run the profiling for the run_cookbook method
async def profile_run_cookbook(runner):
    """
    Profiles the `run_cookbook` method of a given runner.

    This function asynchronously profiles the `run_cookbook` method, which is responsible for executing
    a series of predefined tasks known as a cookbook. It measures the execution time and resource usage
    of the method by invoking `profile_async_function`.

    Args:
        runner: The runner instance on which `run_cookbook` will be invoked.
    """
    await profile_async_function(
        runner.run_cookbooks, "run_cookbooks", ["common-risk-easy"], 2, 2
    )


# Function to run the profiling for the run_recipe method
async def profile_run_recipe(runner):
    """
    Profiles the `run_recipe` method of a given runner.

    This function asynchronously profiles the `run_recipe` method, which is responsible for executing
    a specific recipe. It measures the execution time and resource usage of the method by invoking
    `profile_async_function`.

    Args:
        runner: The runner instance on which `run_recipe` will be invoked.
    """
    await profile_async_function(
        runner.run_recipes, "run_recipes", ["bbq", "auto-categorisation"], 2, 2
    )


# This function wraps the run_cookbook_and_cancel with the profiler
async def profile_run_cookbook_and_cancel(runner):
    await profile_async_function(
        run_cookbook_and_cancel, "run_cookbook_and_cancel", runner
    )


async def run_cookbook_and_cancel(runner):
    # Run the cookbooks in a background task
    run_task = asyncio.create_task(runner.run_cookbooks(["common-risk-easy"], 2))

    # Wait for 1 second before cancelling
    await asyncio.sleep(1)
    await runner.cancel()

    # Wait for the run task to complete
    await run_task


# This function wraps the run_recipe_and_cancel with the profiler
async def profile_run_recipe_and_cancel(runner):
    await profile_async_function(run_recipe_and_cancel, "run_recipe_and_cancel", runner)


async def run_recipe_and_cancel(runner):
    # Run the recipes in a background task
    run_task = asyncio.create_task(runner.run_recipes(["cbbq-lite", "advglue-mnli"], 2))

    # Wait for 1 second before cancelling
    await asyncio.sleep(1)
    await runner.cancel()

    # Wait for the run task to complete
    await run_task


def profile_api_runner_operations(runner_id):
    runner = api_load_runner(runner_id)
    loop = asyncio.get_event_loop()

    # Run Red Teaming
    loop.run_until_complete(profile_run_red_teaming(runner))

    # Run Cookbook
    loop.run_until_complete(profile_run_cookbook(runner))

    # Run Cookbook and Cancel
    loop.run_until_complete(profile_run_cookbook_and_cancel(runner))

    # Run Recipe
    loop.run_until_complete(profile_run_recipe(runner))

    # Run Recipe and Cancel
    loop.run_until_complete(profile_run_recipe_and_cancel(runner))

    runner.close()


def profile_api_session():
    """
    Profiles the performance of various API session functions.

    This function profiles the performance of API session operations such as creating a session,
    getting all chats from a session, getting all session metadata, and deleting a session.

    It uses the `profile_function` to measure the execution time and resource usage of these operations.

    The profiling helps in understanding the efficiency of the session API functions and identifying potential
    bottlenecks or areas for optimization.
    """
    profile_function(
        api_create_session,
        "api_create_session",
        runner.id,
        runner.database_instance,
        runner.endpoints,
        {},
    )
    profile_function(
        api_get_all_chats_from_session, "api_get_all_chats_from_session", runner_id
    )
    profile_function(api_get_all_session_metadata, "api_get_all_session_metadata")
    profile_function(api_get_all_session_names, "api_get_all_session_names")
    profile_function(api_get_available_session_info, "api_get_available_session_info")
    profile_function(api_load_session, "api_load_session", runner_id)
    profile_function(
        api_update_attack_module,
        "api_update_attack_module",
        runner_id,
        "sample_attack_module",
    )
    profile_function(
        api_update_context_strategy,
        "api_update_context_strategy",
        runner_id,
        "add_previous_prompt",
    )
    profile_function(
        api_update_cs_num_of_prev_prompts,
        "api_update_cs_num_of_prev_prompts",
        runner_id,
        2,
    )
    profile_function(api_update_metric, "api_update_metric", runner_id, "advglue")
    profile_function(
        api_update_prompt_template,
        "api_update_prompt_template",
        runner_id,
        "analogical-similarity",
    )
    profile_function(
        api_update_system_prompt,
        "api_update_system_prompt",
        runner_id,
        "this is a test system prompt",
    )
    profile_function(api_delete_session, "api_delete_session", runner_id)


if __name__ == "__main__":
    # Profile a specific chunk of code​​
    # If you get "No samples were recorded. because your code executed in under 1ms, hooray!

    runner_id = "test-runner"
    runner = api_create_runner(
        name="test runner",
        endpoints=["openai-gpt35-turbo", "openai-gpt4"],
        description="Hello!",
    )
    runner.close()

    # Profile each API function
    profile_api_connector()
    profile_api_connector_endpoint()
    profile_api_context_strategy()
    profile_api_cookbook()
    profile_api_dataset()
    profile_api_environment_variables()
    profile_api_metrics()
    profile_api_prompt_template()
    profile_api_recipe()
    profile_api_red_teaming()
    profile_api_result()
    profile_api_runner()
    profile_api_runner_operations(runner_id)
    profile_api_run()
    profile_api_session()

    api_delete_runner(runner_id)
