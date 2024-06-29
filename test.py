from moonshot.src.api.api_environment_variables import api_set_environment_variables
from dotenv import dotenv_values

api_set_environment_variables(dotenv_values(".env"))

from moonshot.api import api_get_bookmark_by_id,api_export_bookmarks,api_delete_bookmark,api_insert_bookmark,api_get_all_bookmarks,api_delete_all_bookmark


# print("\n\n Initial Getting all bookmark")
# print(api_get_all_bookmarks())

# print("Adding a new bookmark record")
# api_insert_bookmark(
#     name="my bookmark 1",
#     prompt="Your prompt",
#     response="Your response",
#     context_strategy="Your context strategy",
#     prompt_template="Your prompt template",
#     attack_module="Your attack module"
# )
# print(api_get_all_bookmarks())

# print("\n\nDeleting a new bookmark record")
# api_delete_bookmark(1)
# print(api_get_all_bookmarks())

# print("\n\nGetting all bookmark")
# print(api_get_all_bookmarks())

# print("\n\nGetting 1 bookmark")
# print(api_get_bookmark_by_id(2))

# print("\n\nDeleting all")
# api_delete_all_bookmark()

# print(api_get_all_bookmarks())