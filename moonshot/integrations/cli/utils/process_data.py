from moonshot.src.utils.find_feature import find_keyword
from moonshot.src.utils.pagination import get_paginated_lists


def filter_data(
    list_of_data: list, keyword: str = "", pagination: tuple = ()
) -> list | None:
    """
    Filters and paginates a list of data.

    Args:
        list_of_data (list): The list of data to be filtered and paginated.
        keyword (str, optional): The keyword to filter the data. Defaults to "".
        pagination (tuple, optional): A tuple containing the page number and page size. Defaults to ().

    Returns:
        list | None: The filtered and paginated list of data, or None if no data matches the criteria.
    """
    # if there is a find keyword
    if keyword:
        list_of_data = find_keyword(keyword, list_of_data)
        if not list_of_data:
            return

    # if pagination is required
    if pagination:
        page_number, page_size = pagination

        if page_number <= 0 or page_size <= 0:
            raise RuntimeError(
                "Invalid page number or page size. Page number and page size should start from 1."
            )

        # An empty filtered result has no last page to fall back to.
        if not list_of_data:
            return []

        # Preserve CLI row numbering without mutating the source records.
        if all(isinstance(item, dict) for item in list_of_data):
            list_of_data = [
                {**item, "idx": index}
                for index, item in enumerate(list_of_data, 1)
            ]

        paginated_data = get_paginated_lists(page_size, list_of_data)

        # Preserve the existing behavior of selecting the last available
        # page when the requested page number exceeds the result count.
        list_of_data = paginated_data[min(page_number, len(paginated_data)) - 1]

    return list_of_data
