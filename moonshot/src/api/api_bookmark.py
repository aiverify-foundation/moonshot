
from moonshot.src.bookmark.bookmark_arguments import BookmarkArguments
from moonshot.src.bookmark.bookmark import Bookmark

bookmark_instance = Bookmark()

def api_insert_bookmark(bookmark_args: BookmarkArguments):
    bookmark_instance.add_bookmark(bookmark_args)

def api_get_all_bookmarks():
    return bookmark_instance.get_all_bookmarks()

def api_get_bookmark_by_id(bookmark_id: int):
    return bookmark_instance.get_bookmark_by_id(bookmark_id)

def api_delete_bookmark(bookmark_id: int):
    bookmark_instance.delete_bookmark(bookmark_id)

def api_delete_all_bookmark():
    bookmark_instance.delete_all_bookmark()
