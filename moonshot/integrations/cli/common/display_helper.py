def display_view_list_format(title: str, items: list) -> str:
    """
    Format a list of items for display.

    This function takes a title and a list of items and formats them into a string suitable for display.
    Each item in the list is displayed on a new line with an index number. If the list is empty, it returns
    the title with 'nil'.

    Args:
        title (str): The title to display above the list.
        items (list): A list of items to be formatted.

    Returns:
        str: The formatted list as a string.
    """
    if items:
        return f"[blue]{title}[/blue]:" + "".join(
            f"\n{i + 1}. {item}" for i, item in enumerate(items)
        )
    else:
        return f"[blue]{title}[/blue]: nil"


def display_view_str_format(title: str, item: str) -> str:
    """
    Format a string item for display with a title.

    This function takes a title and a string item and formats them into a string suitable for display.
    If the item is not an empty string, it is displayed next to the title with a blue color for the title.
    If the item is an empty string, 'nil' is displayed next to the title.

    Args:
        title (str): The title to display next to the item.
        item (str): The string item to be formatted.

    Returns:
        str: The formatted string with the title and item.
    """
    if item:
        return f"[blue]{title}[/blue]: {item}"
    else:
        return f"[blue]{title}[/blue]: nil"
