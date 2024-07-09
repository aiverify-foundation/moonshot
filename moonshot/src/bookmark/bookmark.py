from datetime import datetime

from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage


class Bookmark:
    _instance = None

    def __new__(cls, db_name="bookmark"):
        """
        Create a new instance of the Bookmark class or return the existing instance.

        Args:
            db_name (str): The name of the database.

        Returns:
            Bookmark: The singleton instance of the Bookmark class.
        """
        if cls._instance is None:
            cls._instance = super(Bookmark, cls).__new__(cls)
            cls._instance.__init_instance(db_name)
        return cls._instance

    sql_create_bookmark_table = """
        CREATE TABLE IF NOT EXISTS bookmark (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        prompt TEXT NOT NULL,
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
        name, prompt, response, context_strategy, prompt_template, attack_module,
        metric, bookmark_time)
        VALUES (?,?,?,?,?,?,?,?);
    """

    sql_select_bookmarks_record = """
        SELECT * FROM bookmark;
    """

    sql_select_bookmark_record = """
        SELECT * FROM bookmark WHERE id = ? ;
    """

    sql_delete_bookmark_record = """
        DELETE FROM bookmark WHERE id = ?;
    """

    sql_delete_bookmark_records = """
        DELETE FROM bookmark;
    """

    def __init_instance(self, db_name) -> None:
        """
        Initialize the database instance for the Bookmark class.

        Args:
            db_name (str): The name of the database.
        """
        self.db_instance = Storage.create_database_connection(
            EnvVariables.BOOKMARK.name, db_name, "db"
        )
        Storage.create_database_table(
            self.db_instance, Bookmark.sql_create_bookmark_table
        )

    def add_bookmark(self, bookmark: BookmarkArguments) -> dict:
        """
        Add a new bookmark to the database and return the success status.

        Args:
            bookmark (BookmarkArguments): The bookmark data to add.

        Returns:
            bool: True if the bookmark was added successfully, False otherwise.
        """
        if not bookmark.bookmark_time:
            bookmark.bookmark_time = (
                datetime.now().replace(microsecond=0).isoformat(" ")
            )
        data = (
            bookmark.name,
            bookmark.prompt,
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
                return {"success": True, "message": "Bookmark added successfully."}
            else:
                raise Exception("Error inserting record into database.")
        except Exception as e:
            error_message = f"Failed to add bookmark record: {e}"
            return {"success": False, "message": error_message}

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
        if list_of_bookmarks_tuples:
            list_of_bookmarks = [
                BookmarkArguments.from_tuple_to_dict(bookmark_tuple)
                for bookmark_tuple in list_of_bookmarks_tuples
            ]
        else:
            list_of_bookmarks = []
        return list_of_bookmarks

    def get_bookmark_by_id(self, bookmark_id: int) -> dict:
        """
        Retrieve a bookmark by its unique ID.

        Args:
            bookmark_id (int): The unique identifier for the bookmark.

        Returns:
            dict: The bookmark information as a dictionary.

        Raises:
            RuntimeError: If the bookmark cannot be found.
        """
        if bookmark_id is not None:
            bookmark_info = Storage.read_database_record(
                self.db_instance, (bookmark_id,), Bookmark.sql_select_bookmark_record
            )
            if bookmark_info is not None:
                return BookmarkArguments.from_tuple_to_dict(bookmark_info)
            else:
                raise RuntimeError(
                    f"[Bookmark] No record found for bookmark ID {bookmark_id}"
                )
        else:
            raise RuntimeError(f"[Bookmark] Invalid bookmark ID: {bookmark_id}")

    def delete_bookmark(self, bookmark_id: int) -> dict:
        """
        Delete a bookmark by its unique ID.

        Args:
            bookmark_id (int): The unique identifier for the bookmark to be deleted.
        """
        if bookmark_id is not None:
            try:
                Storage.delete_database_record_by_id(
                    self.db_instance, bookmark_id, Bookmark.sql_delete_bookmark_record
                )
                return {"success": True, "message": "Bookmark record deleted."}
            except Exception as e:
                error_message = f"Failed to delete bookmark record: {e}"
                return {"success": False, "message": error_message}
        else:
            error_message = f"[Bookmark] Invalid bookmark ID: {bookmark_id}"
            return {"success": False, "message": error_message}

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
            return {"success": True, "message": "All bookmark records deleted."}
        except Exception as e:
            error_message = f"Failed to delete all bookmark records: {e}"
            return {"success": False, "message": error_message}

    def export_bookmarks(
        self, write_file: bool = False, export_file_name: str = "bookmarks"
    ) -> list[dict]:
        """
        Export all bookmarks to a JSON file or external storage.

        Args:
            export_file_name (str): The name of the file to export the bookmarks to.
            write_file (bool): Whether to write the bookmarks to a file.

        Returns:
            list[dict]: A list of all bookmarks as dictionaries.
        """
        list_of_bookmarks_tuples = Storage.read_database_records(
            self.db_instance,
            Bookmark.sql_select_bookmarks_record,
        )

        bookmarks_json = [
            BookmarkArguments.from_tuple_to_dict(bookmark_tuple)
            for bookmark_tuple in list_of_bookmarks_tuples
        ]

        if write_file:
            Storage.create_object(
                EnvVariables.BOOKMARK.name,
                export_file_name,
                {"bookmarks": bookmarks_json},
                "json",
            )

        return bookmarks_json

    def close(self) -> None:
        """
        Close the database connection.
        """
        if self.db_instance:
            Storage.close_database_connection(self.db_instance)
