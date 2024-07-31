from .... import api as moonshot_api
from ..schemas.bookmark_create_dto import BookmarkCreateDTO, BookmarkPydanticModel
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from .utils.file_manager import copy_file


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
            prepared_prompt=bookmark_data.prepared_prompt,
            response=bookmark_data.response,
            context_strategy=bookmark_data.context_strategy,
            prompt_template=bookmark_data.prompt_template,
            attack_module=bookmark_data.attack_module,
            metric=bookmark_data.metric,
        )

        return result

    @exception_handler
    def get_all_bookmarks(self, name: str | None = None) -> list[BookmarkPydanticModel]:
        """
        Retrieves all bookmarks or a specific bookmark by its name.

        Args:
            name (str | None, optional): The name of the bookmark to retrieve. If None, all bookmarks are retrieved.

        Returns:
            list[BookmarkPydanticModel]: A list of bookmark models.
        """
        retn_bookmark: list[BookmarkPydanticModel] = []

        if name:
            bookmarks = [moonshot_api.api_get_bookmark(name)]
        else:
            bookmarks = moonshot_api.api_get_all_bookmarks()

        for bookmark in bookmarks:
            retn_bookmark.append(BookmarkPydanticModel(**bookmark))
        return retn_bookmark

    @exception_handler
    def delete_bookmarks(self, all: bool = False, name: str | None = None) -> dict:
        """
        Deletes a single bookmark by its name or all bookmarks if the 'all' flag is set to True and returns
        a boolean indicating the success of the operation.

        Args:
            all (bool, optional): If True, all bookmarks will be deleted. Defaults to False.
            name (str | None, optional): The name of the bookmark to delete. If 'all' is False, 'name' must be provided.

        Returns:
            dict: True if the deletion was successful, False otherwise.
        """
        if all:
            result = moonshot_api.api_delete_all_bookmark()
        elif name is not None:
            result = moonshot_api.api_delete_bookmark(name)
        else:
            raise ValueError("Either 'all' must be True or 'name' must be provided.")

        if not result["success"]:
            raise Exception(
                result["message"], "delete_bookmarks", "DeleteBookmarkError"
            )

        return result

    @exception_handler
    def export_bookmarks(self, export_file_name: str = "bookmarks") -> str:
        """
        Exports bookmarks to a file or returns them as a list of dictionaries.

        Args:
            write_file (bool, optional): If True, bookmarks will be written to a file. Defaults to False.
            export_file_name (str, optional): The name of the file to write bookmarks to. Defaults to "bookmarks".

        Returns:
            list[dict]: A list of bookmarks as dictionaries.
        """

        new_file_path = moonshot_api.api_export_bookmarks(export_file_name)

        return copy_file(new_file_path)
