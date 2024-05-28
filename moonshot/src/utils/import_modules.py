import importlib.util
import inspect
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Any


def create_module_spec(module_name: str, module_file_path: str) -> None | ModuleSpec:
    """
    A helper method to create module specifications if it does not exist

    Args:
        module_name (str): Input module name to be imported
        module_file_path (str): Input module file path to be imported

    Returns:
        None | ModuleSpec: Generated module specifications for importing or error
    """
    try:
        if (
            module_name is None
            or not isinstance(module_name, str)
            or module_file_path is None
            or not isinstance(module_file_path, str)
        ):
            return None

        module_spec = importlib.util.find_spec(module_name)
        if module_spec is None:
            # Create a module spec since it is not available
            module_spec = importlib.util.spec_from_file_location(
                module_name, module_file_path
            )

        return module_spec

    except ValueError:
        # Unable to find spec from this file to create
        return None


def import_module_from_spec(module_spec: ModuleSpec) -> ModuleType | None:
    """
    A helper method to import python module using module specifications

    Args:
        module_spec (ModuleSpec): A generated module specifications for the module to be imported

    Returns:
        ModuleType | None: An imported module
    """
    if module_spec is None or not isinstance(module_spec, ModuleSpec):
        return None

    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def get_instance(id: str, filepath: str) -> Any:
    """
    A helper method to get an instance of a class from a module

    Args:
        id (str): The name of the module and the class to be instantiated
        filepath (str): The path to the module file

    Returns:
        Any: An instance of the class if found, else None
    """
    # Create the module specification
    module_spec = create_module_spec(
        id,
        filepath,
    )

    # Check if the module specification exists
    if module_spec:
        # Import the module
        module = import_module_from_spec(module_spec)

        # Iterate through the attributes of the module
        for attr in dir(module):
            # Get the attribute object
            obj = getattr(module, attr)

            # Check if the attribute is a class and has the same module name as the id
            if (
                inspect.isclass(obj)
                and "None" not in obj.__module__
                and obj.__module__ == id
            ):
                return obj

    # Return None if no instance of the class is found
    return None
