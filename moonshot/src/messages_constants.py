# ------------------------------------------------------------------------------
# BOOKMARK - add_bookmark
# ------------------------------------------------------------------------------
BOOKMARK_ADD_BOOKMARK_SUCCESS = "[Bookmark] Bookmark added successfully."
BOOKMARK_ADD_BOOKMARK_ERROR = "[Bookmark] Failed to add bookmark record: {message}"
BOOKMARK_ADD_BOOKMARK_VALIDATION_ERROR = "Error inserting record into database."

# ------------------------------------------------------------------------------
# BOOKMARK - get_bookmark
# ------------------------------------------------------------------------------
BOOKMARK_GET_BOOKMARK_ERROR = "[Bookmark] No record found for bookmark name: {message}"
BOOKMARK_GET_BOOKMARK_ERROR_1 = "[Bookmark] Invalid bookmark name: {message}"

# ------------------------------------------------------------------------------
# BOOKMARK - delete_bookmark
# ------------------------------------------------------------------------------
BOOKMARK_DELETE_BOOKMARK_SUCCESS = "[Bookmark] Bookmark record deleted."
BOOKMARK_DELETE_BOOKMARK_FAIL = (
    "[Bookmark] Bookmark record not found. Unable to delete."
)
BOOKMARK_DELETE_BOOKMARK_ERROR = (
    "[Bookmark] Failed to delete bookmark record: {message}"
)
BOOKMARK_DELETE_BOOKMARK_ERROR_1 = "[Bookmark] Invalid bookmark name: {message}"

# ------------------------------------------------------------------------------
# BOOKMARK - delete_all_bookmark
# ------------------------------------------------------------------------------
BOOKMARK_DELETE_ALL_BOOKMARK_SUCCESS = "[Bookmark] All bookmark records deleted."
BOOKMARK_DELETE_ALL_BOOKMARK_ERROR = (
    "[Bookmark] Failed to delete all bookmark records: {message}"
)

# ------------------------------------------------------------------------------
# BOOKMARK - export_bookmarks
# ------------------------------------------------------------------------------
BOOKMARK_EXPORT_BOOKMARK_ERROR = "[Bookmark] Failed to export bookmarks: {message}"
BOOKMARK_EXPORT_BOOKMARK_VALIDATION_ERROR = (
    "Export filename must be a non-empty string."
)

# ------------------------------------------------------------------------------
# BOOKMARK ARGUMENTS - from_tuple_to_dict
# ------------------------------------------------------------------------------
BOOKMARK_ARGUMENTS_FROM_TUPLE_TO_DICT_VALIDATION_ERROR = "[BookmarkArguments] Failed to convert to dictionary because of the insufficient number of values."  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR - perform_retry_callback
# ------------------------------------------------------------------------------
CONNECTOR_PERFORM_RETRY_CALLBACK_ERROR = "[Connector ID: {connector_id}] Attempt {attempt_no} failed due to error: {message}"  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR - load
# ------------------------------------------------------------------------------
CONNECTOR_LOAD_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR = "[Connector] The 'ep_args' argument must be an instance of ConnectorEndpointArguments and not None."  # noqa: E501
CONNECTOR_LOAD_CONNECTOR_INSTANCE_RUNTIME_ERROR = (
    "[Connector] Failed to get connector instance: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR - create
# ------------------------------------------------------------------------------
CONNECTOR_CREATE_CONNECTOR_ENDPOINT_ARGUMENTS_VALIDATION_ERROR = "[Connector] The 'ep_args' argument must be an instance of ConnectorEndpointArguments and not None."  # noqa: E501
CONNECTOR_CREATE_ERROR = "[Connector] Failed to create connector: {message}"

# ------------------------------------------------------------------------------
# CONNECTOR - get_available_items
# ------------------------------------------------------------------------------
CONNECTOR_GET_AVAILABLE_ITEMS_ERROR = (
    "[Connector] Failed to get available connectors: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR - get_prediction
# ------------------------------------------------------------------------------
CONNECTOR_GET_PREDICTION_ARGUMENTS_GENERATED_PROMPT_VALIDATION_ERROR = "[Connector] The 'generated_prompt' argument must be an instance of ConnectorPromptArguments and not None."  # noqa: E501
CONNECTOR_GET_PREDICTION_ARGUMENTS_CONNECTOR_VALIDATION_ERROR = "[Connector] The 'connector' argument must be an instance of Connector and not None."  # noqa: E501
CONNECTOR_GET_PREDICTION_INFO = (
    "[Connector ID: {connector_id}] Predicting Prompt Index {prompt_index}."
)
CONNECTOR_GET_PREDICTION_TIME_TAKEN_INFO = "[Connector ID: {connector_id}] Prompt Index {prompt_index} took {prompt_duration}s."  # noqa: E501
CONNECTOR_GET_PREDICTION_ERROR = "[Connector ID: {connector_id}] Prompt Index {prompt_index} failed to get prediction: {message}"  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR - set_system_prompt
# ------------------------------------------------------------------------------
CONNECTOR_SET_SYSTEM_PROMPT_VALIDATION_ERROR = "[Connector] The 'system_prompt' argument must be an instance of string and not None."  # noqa: E501

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - create
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_CREATE_ERROR = (
    "[ConnectorEndpoint] Failed to create connector endpoint: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - read
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_READ_INVALID = "Invalid connector endpoint id - {ep_id}"
CONNECTOR_ENDPOINT_READ_ERROR = (
    "[ConnectorEndpoint] Failed to read connector endpoint: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - update
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_UPDATE_ERROR = (
    "[ConnectorEndpoint] Failed to update connector endpoint: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - delete
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_DELETE_ERROR = (
    "[ConnectorEndpoint] Failed to delete connector endpoint: {message}"
)

# ------------------------------------------------------------------------------
# CONNECTOR ENDPOINT - get_available_items
# ------------------------------------------------------------------------------
CONNECTOR_ENDPOINT_GET_AVAILABLE_ITEMS_ERROR = (
    "[ConnectorEndpoint] Failed to get available connector endpoints: {message}"
)
