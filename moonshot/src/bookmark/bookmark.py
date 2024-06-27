from datetime import datetime

from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage


class Bookmark:
    _instance = None

    def __new__(cls, db_name="bookmark"):
        if cls._instance is None:
            cls._instance = super(Bookmark, cls).__new__(cls)
            # Initialize the instance if it hasn't been done yet
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
        bookmark_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """

    sql_insert_bookmark_record = """
        INSERT INTO bookmark (
        name, prompt, response, context_strategy, prompt_template, attack_module, bookmark_time)
        VALUES (?,?,?,?,?,?,?);
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
        self.db_instance = Storage.create_database_connection(
            EnvVariables.BOOKMARK.name, db_name, "db"
        )
        Storage.create_database_table(
            self.db_instance, Bookmark.sql_create_bookmark_table
        )

    def add_bookmark(self, bookmark: BookmarkArguments) -> None:
        if bookmark.bookmark_time is None:
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
            bookmark.bookmark_time,
        )
        try:
            Storage.create_database_record(
                self.db_instance, data, Bookmark.sql_insert_bookmark_record
            )
        except Exception as e:
            print(f"Failed to add bookmark record: {e}")

    def get_all_bookmarks(self) -> list:
        list_of_bookmarks_tuples = Storage.read_database_records(
            self.db_instance,
            Bookmark.sql_select_bookmarks_record,
        )
        if list_of_bookmarks_tuples:
            list_of_bookmarks = [
                BookmarkArguments.from_tuple(bookmark_tuple).dict()
                for bookmark_tuple in list_of_bookmarks_tuples
            ]
        else:
            list_of_bookmarks = []
        return list_of_bookmarks

    def get_bookmark_by_id(self, bookmark_id: int) -> BookmarkArguments:
        if bookmark_id is not None:
            bookmark_info = Storage.read_database_record(
                self.db_instance, (bookmark_id,), Bookmark.sql_select_bookmark_record
            )
            return BookmarkArguments.from_tuple(bookmark_info)
        else:
            raise RuntimeError(
                f"[Bookmark] Failed to get database record for bookmark_id {bookmark_id}: {self.db_instance}"
            )

    def delete_bookmark(self, bookmark_id: int) -> None:
        if bookmark_id is not None:
            Storage.delete_database_record_by_id(
                self.db_instance, bookmark_id, Bookmark.sql_delete_bookmark_record
            )
            print("Bookmark record deleted")
        else:
            raise RuntimeError(
                f"[Bookmark] Failed to get database record for bookmark_id {bookmark_id}: {self.db_instance}"
            )

    def delete_all_bookmark(self) -> None:
        Storage.delete_database_record_in_table(
            self.db_instance, Bookmark.sql_delete_bookmark_records
        )
        print("All bookmark records deleted")

    def close(self) -> None:
        if self.db_instance:
            Storage.close_database_connection(self.db_instance)
