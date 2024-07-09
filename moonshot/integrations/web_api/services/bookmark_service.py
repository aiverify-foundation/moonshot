from .... import api as moonshot_api
from ..schemas.bookmark_create_dto import BookmarkCreateDTO, BookmarkPydanticModel
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class BookmarkService(BaseService):
    @exception_handler
    def insert_bookmark(self, bookmark_data: BookmarkCreateDTO) -> dict:
        """
        Inserts a new bookmark into the system.

        Args:
            bookmark_data (BookmarkCreateDTO): The data transfer object containing bookmark details.
        """
        result = moonshot_api.api_insert_bookmark(
            name=bookmark_data.name,
            prompt=bookmark_data.prompt,
            response=bookmark_data.response,
            context_strategy=bookmark_data.context_strategy,
            prompt_template=bookmark_data.prompt_template,
            attack_module=bookmark_data.attack_module,
        )

        return result

    @exception_handler
    def get_all_bookmarks(self, id: int | None = None) -> list[BookmarkPydanticModel]:
        """
        Retrieves all bookmarks or a specific bookmark by its ID.

        Args:
            id (int | None, optional): The ID of the bookmark to retrieve. If None, all bookmarks are retrieved.

        Returns:
            list[BookmarkPydanticModel]: A list of bookmark models.
        """
        retn_bookmark: list[BookmarkPydanticModel] = []

        if id:
            bookmarks = [moonshot_api.api_get_bookmark_by_id(id)]
        else:
            bookmarks = moonshot_api.api_get_all_bookmarks()

        for bookmark in bookmarks:
            retn_bookmark.append(BookmarkPydanticModel(**bookmark))
        return retn_bookmark

    @exception_handler
    def delete_bookmarks(self, all: bool = False, id: int | None = None) -> dict:
        """
        Deletes bookmarks from the system either by ID or all bookmarks if specified.

        Args:
            all (bool, optional): If True, all bookmarks will be deleted. Defaults to False.
            id (int | None, optional): The ID of the bookmark to delete.
        """
        if all:
            result = moonshot_api.api_delete_all_bookmark()
        elif id is not None:
            result = moonshot_api.api_delete_bookmark(id)
        else:
            raise ValueError("Either 'all' must be True or 'id' must be provided.")

        if not result["success"]:
            raise Exception(
                result["message"], "delete_bookmarks", "DeleteBookmarkError"
            )

        return result

    @exception_handler
    def export_bookmarks(
        self, write_file: bool = False, export_file_name: str = "bookmarks"
    ) -> list[dict]:
        """
        Exports bookmarks to a file or returns them as a list of dictionaries.

        Args:
            write_file (bool, optional): If True, bookmarks will be written to a file. Defaults to False.
            export_file_name (str, optional): The name of the file to write bookmarks to. Defaults to "bookmarks".

        Returns:
            list[dict]: A list of bookmarks as dictionaries.
        """
        return moonshot_api.api_export_bookmarks(write_file, export_file_name)
