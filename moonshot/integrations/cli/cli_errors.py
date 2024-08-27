# ------------------------------------------------------------------------------
# Benchmark - add_cookbook
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_ADD_COOKBOOK_NAME_VALIDATION = (
    "The 'name' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_COOKBOOK_DESC_VALIDATION = (
    "The 'description' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_COOKBOOK_RECIPES_VALIDATION = (
    "The 'recipes' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_COOKBOOK_RECIPES_LIST_STR_VALIDATION = (
    "The 'recipes' argument must be a list of strings after evaluation."
)

# ------------------------------------------------------------------------------
# Benchmark - list_cookbook
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_LIST_COOKBOOK_FIND_VALIDATION = (
    "The 'find' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_COOKBOOK_PAGINATION_VALIDATION = (
    "The 'pagination' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_COOKBOOK_PAGINATION_VALIDATION_1 = (
    "The 'pagination' argument must be a tuple of two integers."
)

# ------------------------------------------------------------------------------
# Benchmark - view_cookbook
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_VIEW_COOKBOOK_COOKBOOK_VALIDATION = (
    "The 'cookbook' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - run_cookbook
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_RUN_COOKBOOK_NAME_VALIDATION = (
    "The 'name' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_COOKBOOK_COOKBOOKS_VALIDATION = (
    "The 'cookbooks' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_COOKBOOK_COOKBOOKS_VALIDATION_1 = (
    "The 'cookbooks' argument must evaluate to a list of strings."
)
ERROR_BENCHMARK_RUN_COOKBOOK_ENDPOINTS_VALIDATION = (
    "The 'endpoints' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_COOKBOOK_ENDPOINTS_VALIDATION_1 = (
    "The 'endpoints' argument must evaluate to a list of strings."
)
ERROR_BENCHMARK_RUN_COOKBOOK_NUM_OF_PROMPTS_VALIDATION = (
    "The 'num_of_prompts' argument must be an integer."
)
ERROR_BENCHMARK_RUN_COOKBOOK_RANDOM_SEED_VALIDATION = (
    "The 'random_seed' argument must be an integer."
)
ERROR_BENCHMARK_RUN_COOKBOOK_SYS_PROMPT_VALIDATION = (
    "The 'system_prompt' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_COOKBOOK_RUNNER_PROC_MOD_VALIDATION = (
    "The 'runner_proc_module' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_COOKBOOK_RESULT_PROC_MOD_VALIDATION = (
    "The 'result_proc_module' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_COOKBOOK_NO_RESULT = "There are no results generated."

# ------------------------------------------------------------------------------
# Benchmark - update_cookbook
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_UPDATE_COOKBOOK_COOKBOOK_VALIDATION = (
    "The 'cookbook' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_UPDATE_COOKBOOK_UPDATE_VALUES_VALIDATION = (
    "The 'update_values' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_UPDATE_COOKBOOK_UPDATE_VALUES_VALIDATION_1 = (
    "The 'update_values' argument must evaluate to a list of tuples."
)

# ------------------------------------------------------------------------------
# Benchmark - delete_cookbook
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_DELETE_COOKBOOK_COOKBOOK_VALIDATION = (
    "The 'cookbook' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - list_datasets
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_LIST_DATASETS_FIND_VALIDATION = (
    "The 'find' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_DATASETS_PAGINATION_VALIDATION = (
    "The 'pagination' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_DATASETS_PAGINATION_VALIDATION_1 = (
    "The 'pagination' argument must be a tuple of two integers."
)

# ------------------------------------------------------------------------------
# Benchmark - view_dataset
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_VIEW_DATASET_DATASET_FILENAME_VALIDATION = (
    "The 'dataset_filename' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - delete_dataset
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_DELETE_DATASET_DATASET_VALIDATION = (
    "The 'dataset' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - list_metrics
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_LIST_METRICS_FIND_VALIDATION = (
    "The 'find' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_METRICS_PAGINATION_VALIDATION = (
    "The 'pagination' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_METRICS_PAGINATION_VALIDATION_1 = (
    "The 'pagination' argument must be a tuple of two integers."
)

# ------------------------------------------------------------------------------
# Benchmark - view_metric
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_VIEW_METRIC_METRIC_FILENAME_VALIDATION = (
    "The 'metric_filename' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - delete_metric
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_DELETE_METRIC_METRIC_VALIDATION = (
    "The 'metric' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - list_results
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_LIST_RESULTS_FIND_VALIDATION = (
    "The 'find' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_RESULTS_PAGINATION_VALIDATION = (
    "The 'pagination' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_RESULTS_PAGINATION_VALIDATION_1 = (
    "The 'pagination' argument must be a tuple of two integers."
)

# ------------------------------------------------------------------------------
# Benchmark - view_result
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_VIEW_RESULT_RESULT_FILENAME_VALIDATION = (
    "The 'result_filename' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_VIEW_RESULT_METADATA_VALIDATION = "The 'metadata' argument not found."
ERROR_BENCHMARK_VIEW_RESULT_METADATA_INVALID_VALIDATION = (
    "Unable to determine cookbook or recipe."
)

# ------------------------------------------------------------------------------
# Benchmark - delete_result
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_DELETE_RESULT_RESULT_VALIDATION = (
    "The 'result' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - list_runs
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_LIST_RUNS_FIND_VALIDATION = (
    "The 'find' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_RUNS_PAGINATION_VALIDATION = (
    "The 'pagination' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_RUNS_PAGINATION_VALIDATION_1 = (
    "The 'pagination' argument must be a tuple of two integers."
)

# ------------------------------------------------------------------------------
# Benchmark - view_run
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_VIEW_RUN_RUNNER_ID_VALIDATION = (
    "The 'runner_id' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - add_recipe
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_ADD_RECIPE_NAME_VALIDATION = (
    "The 'name' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_RECIPE_DESC_VALIDATION = (
    "The 'description' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_RECIPE_TAGS_VALIDATION = (
    "The 'tags' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_RECIPE_TAGS_LIST_STR_VALIDATION = (
    "The 'tags' argument must be a list of strings after evaluation."
)
ERROR_BENCHMARK_ADD_RECIPE_CATEGORIES_VALIDATION = (
    "The 'categories' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_RECIPE_CATEGORIES_LIST_STR_VALIDATION = (
    "The 'categories' argument must be a list of strings after evaluation."
)
ERROR_BENCHMARK_ADD_RECIPE_DATASETS_VALIDATION = (
    "The 'datasets' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_RECIPE_DATASETS_LIST_STR_VALIDATION = (
    "The 'datasets' argument must be a list of strings after evaluation."
)
ERROR_BENCHMARK_ADD_RECIPE_PROMPT_TEMPLATES_VALIDATION = (
    "The 'prompt_templates' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_RECIPE_PROMPT_TEMPLATES_LIST_STR_VALIDATION = (
    "The 'prompt_templates' argument must be a list of strings after evaluation."
)
ERROR_BENCHMARK_ADD_RECIPE_METRICS_VALIDATION = (
    "The 'metrics' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_RECIPE_METRICS_LIST_STR_VALIDATION = (
    "The 'metrics' argument must be a list of strings after evaluation."
)
ERROR_BENCHMARK_ADD_RECIPE_GRADING_SCALE_VALIDATION = (
    "The 'grading_scale' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_ADD_RECIPE_GRADING_SCALE_DICT_STR_VALIDATION = (
    "The 'grading_scale' argument must be a dictionary after evaluation."
)

# ------------------------------------------------------------------------------
# Benchmark - list_recipes
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_LIST_RECIPES_FIND_VALIDATION = (
    "The 'find' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_RECIPES_PAGINATION_VALIDATION = (
    "The 'pagination' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_LIST_RECIPES_PAGINATION_VALIDATION_1 = (
    "The 'pagination' argument must be a tuple of two integers."
)

# ------------------------------------------------------------------------------
# Benchmark - view_recipe
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_VIEW_RECIPE_RECIPE_VALIDATION = (
    "The 'recipe' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - run_recipe
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_RUN_RECIPE_NAME_VALIDATION = (
    "The 'name' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_RECIPE_RECIPES_VALIDATION = (
    "The 'recipes' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_RECIPE_RECIPES_VALIDATION_1 = (
    "The 'recipes' argument must evaluate to a list of strings."
)
ERROR_BENCHMARK_RUN_RECIPE_ENDPOINTS_VALIDATION = (
    "The 'endpoints' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_RECIPE_ENDPOINTS_VALIDATION_1 = (
    "The 'endpoints' argument must evaluate to a list of strings."
)
ERROR_BENCHMARK_RUN_RECIPE_NUM_OF_PROMPTS_VALIDATION = (
    "The 'num_of_prompts' argument must be an integer."
)
ERROR_BENCHMARK_RUN_RECIPE_RANDOM_SEED_VALIDATION = (
    "The 'random_seed' argument must be an integer."
)
ERROR_BENCHMARK_RUN_RECIPE_SYS_PROMPT_VALIDATION = (
    "The 'system_prompt' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_RECIPE_RUNNER_PROC_MOD_VALIDATION = (
    "The 'runner_proc_module' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_RECIPE_RESULT_PROC_MOD_VALIDATION = (
    "The 'result_proc_module' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_RUN_RECIPE_NO_RESULT = "There are no results generated."

# ------------------------------------------------------------------------------
# Benchmark - update_recipe
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_UPDATE_RECIPE_RECIPE_VALIDATION = (
    "The 'recipe' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_UPDATE_RECIPE_UPDATE_VALUES_VALIDATION = (
    "The 'update_values' argument must be a non-empty string and not None."
)
ERROR_BENCHMARK_UPDATE_RECIPE_UPDATE_VALUES_VALIDATION_1 = (
    "The 'update_values' argument must evaluate to a list of tuples."
)

# ------------------------------------------------------------------------------
# Benchmark - delete_recipe
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_DELETE_RECIPE_RECIPE_VALIDATION = (
    "The 'recipe' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - view_runner
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_VIEW_RUNNER_RUNNER_VALIDATION = (
    "The 'runner' argument must be a non-empty string and not None."
)

# ------------------------------------------------------------------------------
# Benchmark - delete_runner
# ------------------------------------------------------------------------------
ERROR_BENCHMARK_DELETE_RUNNER_RUNNER_VALIDATION = (
    "The 'runner' argument must be a non-empty string and not None."
)
