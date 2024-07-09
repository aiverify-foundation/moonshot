from moonshot.src.bookmark.bookmark import Bookmark
from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments

_bookmark_instance = None


def get_bookmark_instance():
    global _bookmark_instance
    if _bookmark_instance is None:
        _bookmark_instance = Bookmark()
    return _bookmark_instance


def api_insert_bookmark(
    name: str,
    prompt: str,
    response: str,
    context_strategy: str = "",
    prompt_template: str = "",
    attack_module: str = "",
    metric: str = "",
) -> dict:
    """
    Inserts a new bookmark into the database.

    This function constructs a BookmarkArguments object with the provided details and
    invokes the add_bookmark method of a Bookmark instance to persist the new bookmark.

    Args:
        name (str): The unique name of the bookmark.
        prompt (str): The associated prompt text for the bookmark.
        response (str): The corresponding response text for the bookmark.
        context_strategy (str): The strategy used for context management in the bookmark.
        prompt_template (str): The template used for generating the prompt.
        attack_module (str): The attack module linked with the bookmark.
    """
    # Create a new BookmarkArguments object
    bookmark_args = BookmarkArguments(
        id=0,  # id will be auto-generated by the database
        name=name,
        prompt=prompt,
        response=response,
        context_strategy=context_strategy,
        prompt_template=prompt_template,
        attack_module=attack_module,
        metric=metric,
        bookmark_time="",  # bookmark_time will be set to current time in add_bookmark method
    )
    return get_bookmark_instance().add_bookmark(bookmark_args)


def api_get_all_bookmarks() -> list[dict]:
    """
    Retrieves a list of all bookmarks from the database.

    Returns:
        list[dict]: A list of bookmarks, each represented as a dictionary.
    """
    return get_bookmark_instance().get_all_bookmarks()


def api_get_bookmark(bookmark_name: str) -> dict:
    """
    Retrieves the details of a specific bookmark by its name.

    Args:
        bookmark_name (int): The name of the bookmark to retrieve.

    Returns:
        dict: The bookmark details corresponding to the provided ID.
    """
    return get_bookmark_instance().get_bookmark(bookmark_name)


def api_delete_bookmark(bookmark_id: int) -> dict:
    """
    Removes a bookmark from the database using its ID.

    Args:
        bookmark_id (int): The ID of the bookmark to be removed.
    """
    return get_bookmark_instance().delete_bookmark(bookmark_id)


def api_delete_all_bookmark() -> dict:
    """
    Removes all bookmarks from the database.
    """
    return get_bookmark_instance().delete_all_bookmark()

def api_export_bookmarks(
    export_file_name: str = "bookmarks"
) -> str:
    """
    Exports bookmarks to a specified file.

    Args:
        export_file_name (str): The name of the file to export the bookmarks to.

    Returns:
        str: The filepath of where the file is written.
    """
    return get_bookmark_instance().export_bookmarks(export_file_name)
