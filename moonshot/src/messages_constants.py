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
BOOKMARK_EXPORT_BOOKMARK_VALIDATION_ERROR = "Export filename must be a non-empty string"

# ------------------------------------------------------------------------------
# BOOKMARK ARGUMENTS - from_tuple_to_dict
# ------------------------------------------------------------------------------
BOOKMARK_ARGUMENTS_FROM_TUPLE_TO_DICT_VALIDATION_ERROR = "[BookmarkArguments] Failed to convert to dictionary because of the insufficient number of values"  # noqa: E501
