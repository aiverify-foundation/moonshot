# ------------------------------------------------------------------------------
# BOOKMARK - add_bookmark
# ------------------------------------------------------------------------------
BOOKMARK_ADD_BOOKMARK_ERROR = (
    "[Bookmark] Couldn't add bookmark. Here's the error: {message}"
)
BOOKMARK_ADD_BOOKMARK_SUCCESS = "[Bookmark] Bookmark added successfully!"
BOOKMARK_ADD_BOOKMARK_VALIDATION_ERROR = "There was an error adding the bookmark to the database. Please check the details and try again."  # noqa: E501

# ------------------------------------------------------------------------------
# BOOKMARK - delete_all_bookmark
# ------------------------------------------------------------------------------
BOOKMARK_DELETE_ALL_BOOKMARK_ERROR = (
    "[Bookmark] Couldn't delete all bookmarks. Here's the error: {message}"
)
BOOKMARK_DELETE_ALL_BOOKMARK_SUCCESS = (
    "[Bookmark] All bookmarks were deleted successfully!"
)

# ------------------------------------------------------------------------------
# BOOKMARK - delete_bookmark
# ------------------------------------------------------------------------------
BOOKMARK_DELETE_BOOKMARK_ERROR = (
    "[Bookmark] Couldn't delete the bookmark. Here's the error: {message}"
)
BOOKMARK_DELETE_BOOKMARK_INVALID_NAME_ERROR = (
    "[Bookmark] The bookmark name provided is invalid: {message}"
)
BOOKMARK_DELETE_BOOKMARK_NOT_FOUND_ERROR = (
    "[Bookmark] Bookmark not found. Unable to delete."
)
BOOKMARK_DELETE_BOOKMARK_SUCCESS = "[Bookmark] Bookmark deleted successfully!"

# ------------------------------------------------------------------------------
# BOOKMARK - export_bookmarks
# ------------------------------------------------------------------------------
BOOKMARK_EXPORT_BOOKMARK_ERROR = (
    "[Bookmark] Couldn't export bookmarks. Here's the error: {message}"
)
BOOKMARK_EXPORT_BOOKMARK_VALIDATION_ERROR = (
    "The export filename must be a non-empty string. Please provide a valid filename."
)

# ------------------------------------------------------------------------------
# BOOKMARK - get_bookmark
# ------------------------------------------------------------------------------
BOOKMARK_GET_BOOKMARK_ERROR = "[Bookmark] No bookmark found with the name: {message}"
BOOKMARK_GET_BOOKMARK_INVALID_NAME_ERROR = (
    "[Bookmark] The bookmark name provided is invalid: {message}"
)

# ------------------------------------------------------------------------------
# BOOKMARK ARGUMENTS - from_tuple_to_dict
# ------------------------------------------------------------------------------
BOOKMARK_ARGUMENTS_FROM_TUPLE_TO_DICT_VALIDATION_ERROR = "[BookmarkArguments] Couldn't convert to dictionary due to missing values. Please ensure all required values are provided."  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR - create
# ------------------------------------------------------------------------------
CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR = "[Connector] The 'ep_args' argument must be a valid ConnectorEndpointArguments instance and not None. Please check the provided arguments."  # noqa: E501
CONNECTOR_CREATE_ERROR = (
    "[Connector] Couldn't create connector. Here's the error: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR - get_available_items
# ------------------------------------------------------------------------------
CONNECTOR_GET_AVAILABLE_ITEMS_ERROR = (
    "[Connector] Couldn't get available connectors. Here's the error: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR - get_prediction
# ------------------------------------------------------------------------------
CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR = "[Connector] The 'connector' argument must be a valid Connector instance and not None. Please check the provided connector."  # noqa: E501
CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR = "[Connector] The 'generated_prompt' argument must be a valid ConnectorPromptArguments instance and not None. Please check the provided prompt."  # noqa: E501
CONNECTOR_GET_PREDICTION_ERROR = "[Connector ID: {connector_id}] Prompt Index {prompt_index} couldn't get prediction. Here's the error: {message}"  # noqa: E501
CONNECTOR_GET_PREDICTION_INFO = (
    "[Connector ID: {connector_id}] Predicting Prompt Index {prompt_index}."
)
CONNECTOR_GET_PREDICTION_TIME_TAKEN_INFO = "[Connector ID: {connector_id}] Prompt Index {prompt_index} took {prompt_duration} seconds."  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR - load
# ------------------------------------------------------------------------------
CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR = "[Connector] The 'ep_args' argument must be a valid ConnectorEndpointArguments instance and not None. Please check the provided arguments."  # noqa: E501
CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR = (
    "[Connector] Couldn't get connector instance. Here's the error: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR - perform_retry_callback
# ------------------------------------------------------------------------------
CONNECTOR_PERFORM_RETRY_CALLBACK_ERROR = "[Connector ID: {connector_id}] Attempt {attempt_no} failed due to error: {message}"  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR - set_system_prompt
# ------------------------------------------------------------------------------
CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR = "[Connector] The 'system_prompt' argument must be a valid string and not None. Please check the provided system prompt."  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - create
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_CREATE_ERROR = "[ConnectorEndpoint] Couldn't create connector endpoint. Here's the error: {message}"

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - delete
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_DELETE_ERROR = "[ConnectorEndpoint] Couldn't delete connector endpoint. Here's the error: {message}"

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - get_available_items
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_GET_AVAILABLE_ITEMS_ERROR = "[ConnectorEndpoint] Couldn't get available connector endpoints. Here's the error: {message}"  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - read
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_READ_ERROR = (
    "[ConnectorEndpoint] Couldn't read connector endpoint. Here's the error: {message}"
)
CONNECTOR_ENDPOINT_READ_INVALID_ID_ERROR = (
    "[ConnectorEndpoint] Invalid connector endpoint ID: {ep_id}"
)

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - update
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_UPDATE_ERROR = "[ConnectorEndpoint] Couldn't update connector endpoint. Here's the error: {message}"

# ------------------------------------------------------------------------------
# PROMPT - process_prompt
# ------------------------------------------------------------------------------
PROMPT_CANCEL_WARNING = "[Prompt] Cancelling prompt... Please wait."

# ------------------------------------------------------------------------------
# PROMPT GENERATION - get_dataset_prompts
# ------------------------------------------------------------------------------
PROMPT_GENERATION_GET_DATASET_PROMPTS = "[PromptGenerator] Using {num_of_prompts} out of {total_dataset_prompts} prompts from dataset {ds_id}."  # noqa: E501

# ------------------------------------------------------------------------------
# PROMPT PROCESSOR - evaluate_metrics
# ------------------------------------------------------------------------------
PROMPT_PROCESSOR_EVALUATE_METRICS_CURRENT_METRIC_DEBUG = "[PromptProcessor] Prompt with UUID {uuid} is currently checking the metric called {metric_name}."  # noqa: E501
PROMPT_PROCESSOR_EVALUATE_METRICS_DEBUG = (
    "[PromptProcessor] Prompt with UUID {uuid} is now evaluating all the metrics."
)
PROMPT_PROCESS_EVALUATE_METRICS_EXCEPTION_ERROR = "[PromptProcessor] Oops! Something went wrong while evaluating the metrics for prompt with UUID {uuid}: {message}"  # noqa: E501

# ------------------------------------------------------------------------------
# PROMPT PROCESSOR - process_prompt
# ------------------------------------------------------------------------------
PROMPT_PROCESSOR_PROCESS_PROMPT_CANCELLED_ERROR = "[PromptProcessor] The process for the prompt with UUID {uuid} was cancelled. It didn't finish as expected."  # noqa: E501
PROMPT_PROCESSOR_PROCESS_PROMPT_EXCEPTION_ERROR = "[PromptProcessor] Oops! Something went wrong while processing the prompt with UUID {uuid}. Here's the error: {message}"  # noqa: E501

# ------------------------------------------------------------------------------
# PROMPT PROCESSOR - query_connector
# ------------------------------------------------------------------------------
PROMPT_PROCESSOR_QUERY_CONNECTOR_DEBUG = "[PromptProcessor] The prompt with UUID {uuid} is now asking the connector for information."  # noqa: E501
PROMPT_PROCESS_QUERY_CONNECTOR_EXCEPTION_ERROR = "[PromptProcessor] Oops! Something went wrong while querying the connector for prompt with UUID {uuid}: {message}"  # noqa: E501

# ------------------------------------------------------------------------------
# PROMPT PROCESSOR - set_status
# ------------------------------------------------------------------------------
PROMPT_PROCESSOR_SET_STATUS_DEBUG = "[PromptProcessor] The status of the prompt with UUID {uuid} has been updated to {new_status}."  # noqa: E501

# ------------------------------------------------------------------------------
# RUN - cancel
# ------------------------------------------------------------------------------
RUN_CANCEL_WARNING = "[Run] Cancelling the run... Please wait."

# ------------------------------------------------------------------------------
# RUN - _format_results
# ------------------------------------------------------------------------------
RUN_FORMAT_RESULTS_FORMATTING_ERROR = (
    "[Run] Couldn't format the results because of this error: {error}"
)
RUN_FORMAT_RESULTS_MODULE_INSTANCE_ERROR = (
    "[Run] Couldn't start the result module. Please check the module configuration."
)

# ------------------------------------------------------------------------------
# RUN - _initialize_run
# ------------------------------------------------------------------------------
RUN_INITIALIZE_RUN_DB_INSTANCE_NOT_INITIALISED = (
    "[Run] Couldn't create record because the database isn't set up."
)
RUN_INITIALIZE_RUN_ERROR = "[Run] Couldn't start the run due to this error: {error}"
RUN_INITIALIZE_RUN_FAILED_TO_CREATE_RECORD = (
    "[Run] Couldn't create record because it wasn't inserted."
)

# ------------------------------------------------------------------------------
# RUN - load
# ------------------------------------------------------------------------------
RUN_LOAD_DB_INSTANCE_NOT_PROVIDED = (
    "[Run] Database is missing. Please provide a valid database instance."
)
RUN_LOAD_FAILED_TO_GET_DB_RECORD = "[Run] Couldn't get record for run_id {run_id} from the database: {database_instance}"  # noqa: E501

# ------------------------------------------------------------------------------
# RUN - _load_module
# ------------------------------------------------------------------------------
RUN_LOAD_MODULE_NAME_NOT_PROVIDED = (
    "[Run] The module name for '{arg_key}' is missing. Please provide the module name."
)
RUN_LOAD_UNABLE_TO_GET_INSTANCE = "[Run] Couldn't create an instance for the module '{module_name}'. Please check the module configuration."  # noqa: E501

# ------------------------------------------------------------------------------
# RUN - _load_modules
# ------------------------------------------------------------------------------
RUN_LOAD_MODULES_LOADING_ERROR = (
    "[Run] Couldn't load the module because of this error: {error}"
)

# ------------------------------------------------------------------------------
# RUN - run
# ------------------------------------------------------------------------------
RUN_RUN_FAILED = "[Run] There was an error while executing the run process: {error}"

# ------------------------------------------------------------------------------
# RUN - _run_benchmark
# ------------------------------------------------------------------------------
RUN_RUN_BENCHMARK_MODULE_INSTANCE_ERROR = (
    "[Run] Couldn't start the runner module. Please check the module configuration."
)
RUN_RUN_BENCHMARK_PROCESSING_ERROR = (
    "[Run] There was an error while running the benchmark: {error}"
)

# ------------------------------------------------------------------------------
# RUN PROGRESS - get_all_runs
# ------------------------------------------------------------------------------
RUN_GET_ALL_RUNS_LOAD_DB_INSTANCE_NOT_PROVIDED = (
    "[RunProgress] Couldn't update progress because the database isn't set up properly."
)

# ------------------------------------------------------------------------------
# RUN PROGRESS - notify_progress
# ------------------------------------------------------------------------------
RUN_NOTIFY_PROGRESS_DB_INSTANCE_NOT_PROVIDED = (
    "[RunProgress] Can't notify progress because the database is missing."
)

# ------------------------------------------------------------------------------
# TASK GENERATOR - create_tasks
# ------------------------------------------------------------------------------
TASK_GENERATOR_CREATE_TASKS_DEBUG = (
    "[TaskGenerator] Starting to create benchmarking tasks."
)
TASK_GENERATOR_CREATE_TASKS_INVALID_TASKS_PROMPTS_EXCEPTION_ERROR = (
    "[TaskGenerator] No tasks were created or there are no task prompts available."
)

# ------------------------------------------------------------------------------
# TASK GENERATOR - generate_tasks
# ------------------------------------------------------------------------------
TASK_GENERATOR_GENERATE_TASKS_INVALID_COOKBOOK_EXCEPTION_ERROR = (
    "[TaskGenerator] There was an issue with the cookbook '{cookbook_name}': {message}"
)
TASK_GENERATOR_GENERATE_TASKS_INVALID_RECIPE_EXCEPTION_ERROR = (
    "[TaskGenerator] There was an issue with the recipe '{recipe_name}': {message}"
)

# ------------------------------------------------------------------------------
# TASK PROCESSOR - generate_prompts
# ------------------------------------------------------------------------------
TASK_PROCESSOR_GENERATE_PROMPTS_DEBUG = (
    "[TaskProcessor] Task with UUID {uuid} is in the process of creating prompts."
)

# ------------------------------------------------------------------------------
# TASK PROCESSOR - process_prompts
# ------------------------------------------------------------------------------
TASK_PROCESSOR_PROCESS_PROMPTS_DEBUG = (
    "[TaskProcessor] Task with UUID {uuid} is currently processing the prompts."
)
TASK_PROCESSOR_PROCESS_PROMPTS_TASK_PROMPT_GENERATOR_NOT_PROVIDED = (
    "[TaskProcessor] Can't process prompts because the prompt generator is missing."
)

# ------------------------------------------------------------------------------
# TASK PROCESSOR - process_task
# ------------------------------------------------------------------------------
TASK_PROCESSOR_PROCESS_TASK_CANCELLED_ERROR = (
    "[TaskProcessor] Task with UUID {uuid} was cancelled unexpectedly."
)
TASK_PROCESSOR_PROCESS_TASK_EXCEPTION_ERROR = (
    "[TaskProcessor] Task with UUID {uuid} encountered an error: {message}"
)

# ------------------------------------------------------------------------------
# TASK PROCESSOR - set_status
# ------------------------------------------------------------------------------
TASK_PROCESSOR_SET_STATUS_DEBUG = (
    "[TaskProcessor] Task with UUID {uuid} status has been updated to {new_status}."
)
