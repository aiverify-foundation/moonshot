import os
import shutil

# Global variable to store the path to the temporary folder
TEMP_FOLDER_PATH = None


def create_temp_dir(temp_file_path: str):
    """
    Create a temporary directory at the specified path.

    This function sets a global variable with the path to the temporary directory
    and creates the directory if it does not already exist.

    Args:
        temp_file_path (str): The file path where the temporary directory will be created.
    """
    global TEMP_FOLDER_PATH
    TEMP_FOLDER_PATH = temp_file_path
    if not os.path.exists(TEMP_FOLDER_PATH):
        os.makedirs(TEMP_FOLDER_PATH)


def copy_file(file_path: str) -> str:
    """
    Copy a file to the temporary directory.

    This function copies a file from the given file path to the temporary directory
    set by the create_temp_dir function. It raises an error if the temporary directory
    path is not set before calling this function.

    Args:
        file_path (str): The path of the file to be copied.

    Returns:
        str: The path to the copied file in the temporary directory.

    Raises:
        ValueError: If the temporary folder path is not set.
    """
    if TEMP_FOLDER_PATH is None:
        raise ValueError(
            "Temporary folder path is not set. Call create_temp_dir first."
        )

    # Define the destination path for the copied file
    dest_path = os.path.join(TEMP_FOLDER_PATH, os.path.basename(file_path))

    # Copy the file to the destination
    shutil.copy(file_path, dest_path)

    return dest_path
