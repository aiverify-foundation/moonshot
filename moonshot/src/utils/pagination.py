def get_paginated_lists(page_size: int, list_of_items: list) -> list:
    """
    Splits a list of items into a list of lists, each containing a maximum of `page_size` items.

    Args:
        page_size (int): The number of items per page.
        list_of_items (list): The list of items to be paginated.

    Returns:
        list: A list of lists, where each sublist contains up to `page_size` items.

    Raises:
        RuntimeError: If `page_size` is not provided or is invalid.
    """

    if not page_size:
        raise RuntimeError("Unable to get page_size for pagination.")

    # Break list_of_items into a list of lists, each of size page_size
    paginated_items = [
        list_of_items[i : i + page_size]
        for i in range(0, len(list_of_items), page_size)
    ]

    return paginated_items
