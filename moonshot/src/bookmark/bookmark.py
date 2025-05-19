from __future__ import annotations

import textwrap
from datetime import datetime

from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class Bookmark:
    BOOKMARK_ADD_BOOKMARK_ERROR = "[Bookmark] Failed to add bookmark record: {message}"
    BOOKMARK_ADD_BOOKMARK_SUCCESS = "[Bookmark] Bookmark added successfully."
    BOOKMARK_ADD_BOOKMARK_VALIDATION_ERROR = "Error inserting record into database."
    BOOKMARK_DELETE_ALL_BOOKMARK_ERROR = (
        "[Bookmark] Failed to delete all bookmark records: {message}"
    )
    BOOKMARK_DELETE_ALL_BOOKMARK_SUCCESS = "[Bookmark] All bookmark records deleted."
    BOOKMARK_DELETE_BOOKMARK_ERROR = (
        "[Bookmark] Failed to delete bookmark record: {message}"
    )
    BOOKMARK_DELETE_BOOKMARK_ERROR_1 = "[Bookmark] Invalid bookmark name: {message}"
    BOOKMARK_DELETE_BOOKMARK_FAIL = (
        "[Bookmark] Bookmark record not found. Unable to delete."
    )
    BOOKMARK_DELETE_BOOKMARK_SUCCESS = "[Bookmark] Bookmark record deleted."
    BOOKMARK_EXPORT_BOOKMARK_ERROR = "[Bookmark] Failed to export bookmarks: {message}"
    BOOKMARK_EXPORT_BOOKMARK_VALIDATION_ERROR = (
        "Export filename must be a non-empty string."
    )
    BOOKMARK_GET_BOOKMARK_ERROR = (
        "[Bookmark] No record found for bookmark name: {message}"
    )
    BOOKMARK_GET_BOOKMARK_ERROR_1 = "[Bookmark] Invalid bookmark name: {message}"
    _instance = None

    sql_table_name = "bookmark"

    sql_create_bookmark_table = """
        CREATE TABLE IF NOT EXISTS bookmark (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        prompt TEXT NOT NULL,
        prepared_prompt TEXT NOT NULL,
        response TEXT NOT NULL,
        context_strategy TEXT,
        prompt_template TEXT,
        attack_module TEXT,
        metric TEXT,
        bookmark_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """

    sql_insert_bookmark_record = """
        INSERT INTO bookmark (
        name, prompt, prepared_prompt, response, context_strategy, prompt_template, attack_module,
        metric, bookmark_time)
        VALUES (?,?,?,?,?,?,?,?,?);
    """

    sql_select_bookmarks_record = """
        SELECT * FROM bookmark;
    """

    sql_select_bookmark_record = """
        SELECT * FROM bookmark WHERE name = ? ;
    """

    sql_delete_bookmark_records = """
        DELETE FROM bookmark;
    """

    def __new__(cls, db_name="bookmark"):
        """
        Create a new instance of the Bookmark class or return the existing instance.

        This method ensures that only one instance of the Bookmark class is created (singleton pattern).
        If an instance already exists, it returns that instance. Otherwise, it creates a new instance
        and initializes it with the provided database name.

        Args:
            db_name (str): The name of the database. Defaults to "bookmark".

        Returns:
            Bookmark: The singleton instance of the Bookmark class.
        """
        if cls._instance is None:
            cls._instance = super(Bookmark, cls).__new__(cls)
            cls._instance.__init_instance(db_name)
        return cls._instance

    def __init_instance(self, db_name: str = "bookmark") -> None:
        """
        Initialize the database instance for the Bookmark class.

        This method sets up the database connection for the Bookmark class. It creates a new database
        connection using the provided database name and checks if the required table exists. If the table
        does not exist, it creates the table.

        Args:
            db_name (str): The name of the database. Defaults to "bookmark".
        """
        self.db_instance = Storage.create_database_connection(
            EnvVariables.BOOKMARKS.name, db_name, "db"
        )

        if not Storage.check_database_table_exists(
            self.db_instance, Bookmark.sql_table_name
        ):
            Storage.create_database_table(
                self.db_instance, Bookmark.sql_create_bookmark_table
            )

    def add_bookmark(self, bookmark: BookmarkArguments) -> dict:
        """
        Add a new bookmark to the database and return the success status.

        Args:
            bookmark (BookmarkArguments): The bookmark data to add.

        Returns:
            dict: A dictionary containing the success status and a message.
        """
        bookmark.bookmark_time = datetime.now().replace(microsecond=0).isoformat(" ")

        data = (
            bookmark.name,
            bookmark.prompt,
            bookmark.prepared_prompt,
            bookmark.response,
            bookmark.context_strategy,
            bookmark.prompt_template,
            bookmark.attack_module,
            bookmark.metric,
            bookmark.bookmark_time,
        )
        try:
            results = Storage.create_database_record(
                self.db_instance, data, Bookmark.sql_insert_bookmark_record
            )
            if results is not None:
                return {
                    "success": True,
                    "message": Bookmark.BOOKMARK_ADD_BOOKMARK_SUCCESS,
                }
            else:
                raise Exception(Bookmark.BOOKMARK_ADD_BOOKMARK_VALIDATION_ERROR)
        except Exception as e:
            return {
                "success": False,
                "message": Bookmark.BOOKMARK_ADD_BOOKMARK_ERROR.format(message=str(e)),
            }

    def get_all_bookmarks(self) -> list[dict]:
        """
        Retrieve all bookmarks from the database.

        Returns:
            list[dict]: A list of all bookmarks as dictionaries.
        """
        list_of_bookmarks_tuples = Storage.read_database_records(
            self.db_instance,
            Bookmark.sql_select_bookmarks_record,
        )
        if isinstance(list_of_bookmarks_tuples, list) and all(
            isinstance(item, tuple) for item in list_of_bookmarks_tuples
        ):
            list_of_bookmarks = [
                BookmarkArguments.from_tuple_to_dict(bookmark_tuple)
                for bookmark_tuple in list_of_bookmarks_tuples
            ]
        else:
            list_of_bookmarks = []
        return list_of_bookmarks

    def get_bookmark(self, bookmark_name: str) -> dict:
        """
        Retrieve a bookmark by its unique name.

        Args:
            bookmark_name (str): The unique name for the bookmark.

        Returns:
            dict: The bookmark information as a dictionary.

        Raises:
            RuntimeError: If the bookmark cannot be found.
        """
        if isinstance(bookmark_name, str) and bookmark_name:
            bookmark_info = Storage.read_database_record(
                self.db_instance, (bookmark_name,), Bookmark.sql_select_bookmark_record
            )
            if (
                bookmark_info is not None
                and isinstance(bookmark_info, tuple)
                and all(
                    isinstance(item, str) for item in bookmark_info[1:]
                )  # Check if the rest are strings besides id
            ):
                return BookmarkArguments.from_tuple_to_dict(bookmark_info)
            else:
                raise RuntimeError(
                    Bookmark.BOOKMARK_GET_BOOKMARK_ERROR.format(message=bookmark_name)
                )
        else:
            raise RuntimeError(
                Bookmark.BOOKMARK_GET_BOOKMARK_ERROR_1.format(message=bookmark_name)
            )

    def delete_bookmark(self, bookmark_name: str) -> dict:
        """
        Delete a bookmark by its unique name.

        Args:
            bookmark_name (str): The unique name for the bookmark to be deleted.

        Returns:
            dict: A dictionary containing the success status and a message.
        """
        if isinstance(bookmark_name, str) and bookmark_name:
            try:
                bookmark_info = Storage.read_database_record(
                    self.db_instance,
                    (bookmark_name,),
                    Bookmark.sql_select_bookmark_record,
                )
                if bookmark_info is not None:
                    sql_delete_bookmark_record = textwrap.dedent(
                        f"""
                        DELETE FROM bookmark WHERE name = '{bookmark_name}';
                    """
                    )
                    Storage.delete_database_record_in_table(
                        self.db_instance, sql_delete_bookmark_record
                    )
                    return {
                        "success": True,
                        "message": Bookmark.BOOKMARK_DELETE_BOOKMARK_SUCCESS,
                    }
                else:
                    return {
                        "success": False,
                        "message": Bookmark.BOOKMARK_DELETE_BOOKMARK_FAIL,
                    }
            except Exception as e:
                return {
                    "success": False,
                    "message": Bookmark.BOOKMARK_DELETE_BOOKMARK_ERROR.format(
                        message=str(e)
                    ),
                }
        else:
            return {
                "success": False,
                "message": Bookmark.BOOKMARK_DELETE_BOOKMARK_ERROR_1.format(
                    message=bookmark_name
                ),
            }

    def delete_all_bookmark(self) -> dict:
        """
        Delete all bookmarks from the database and return the operation result.

        Returns:
            dict: A dictionary with 'success' status and 'message' containing an error message if failed.
        """
        try:
            Storage.delete_database_record_in_table(
                self.db_instance, Bookmark.sql_delete_bookmark_records
            )
            return {
                "success": True,
                "message": Bookmark.BOOKMARK_DELETE_ALL_BOOKMARK_SUCCESS,
            }
        except Exception as e:
            return {
                "success": False,
                "message": Bookmark.BOOKMARK_DELETE_ALL_BOOKMARK_ERROR.format(
                    message=str(e)
                ),
            }

    def export_bookmarks(self, export_file_name: str = "bookmarks") -> str:
        """
        Export all bookmarks to a JSON file.

        This method retrieves all bookmarks from the database, converts them to a JSON format,
        and writes them to a file in the 'moonshot-data/bookmark' directory with the provided file name.

        Args:
            export_file_name (str): The base name of the file to export the bookmarks to.
                                    The '.json' extension will be appended to this base name.

        Returns:
            str: The path to the exported JSON file containing the bookmarks.

        Raises:
            Exception: If the export file name is invalid or an error occurs during export.
        """
        if not isinstance(export_file_name, str) or not export_file_name:
            error_message = Bookmark.BOOKMARK_EXPORT_BOOKMARK_ERROR.format(
                message=Bookmark.BOOKMARK_EXPORT_BOOKMARK_VALIDATION_ERROR
            )
            logger.error(error_message)
            raise Exception(error_message)

        list_of_bookmarks_tuples = Storage.read_database_records(
            self.db_instance,
            Bookmark.sql_select_bookmarks_record,
        )

        if (
            list_of_bookmarks_tuples is not None
            and isinstance(list_of_bookmarks_tuples, list)
            and all(isinstance(item, tuple) for item in list_of_bookmarks_tuples)
        ):
            bookmarks_json = [
                BookmarkArguments.from_tuple_to_dict(bookmark_tuple)
                for bookmark_tuple in list_of_bookmarks_tuples
            ]
        else:
            bookmarks_json = []

        try:
            return Storage.create_object(
                EnvVariables.BOOKMARKS.name,
                export_file_name,
                {"bookmarks": bookmarks_json},
                "json",
            )
        except Exception as e:
            error_message = Bookmark.BOOKMARK_EXPORT_BOOKMARK_ERROR.format(
                message=str(e)
            )
            logger.error(error_message)
            raise Exception(error_message)

    def close(self) -> None:
        """
        Close the database connection and set the Bookmark instance to None.

        This method ensures that the database connection is properly closed and the singleton
        instance of the Bookmark class is reset to None, allowing for a fresh instance to be created
        if needed in the future.
        """
        if self.db_instance:
            Storage.close_database_connection(self.db_instance)

        Bookmark._instance = None
