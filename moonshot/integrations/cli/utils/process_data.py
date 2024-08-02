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
        # add index to every dictionary in the list
        if all(isinstance(item, dict) for item in list_of_data):
            for index, item in enumerate(list_of_data, 1):
                if isinstance(item, dict):
                    item["idx"] = index

        # get paginated data
        page_number = pagination[0]
        page_size = pagination[1]

        if page_number <= 0 or page_size <= 0:
            # print("Invalid page number or page size. Page number and page size should start from 1.")
            raise RuntimeError(
                "Invalid page number or page size. Page number and page size should start from 1."
            )

        paginated_data = get_paginated_lists(page_size, list_of_data)

        # perform index checks
        paginated_data_size = len(paginated_data)
        if page_number > paginated_data_size:
            list_of_data = paginated_data[(paginated_data_size - 1)]
        else:
            list_of_data = paginated_data[(page_number - 1)]

    return list_of_data
