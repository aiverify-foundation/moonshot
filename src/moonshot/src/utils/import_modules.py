import importlib.util
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Union


def create_module_spec(
    module_name: str, module_file_path: str
) -> Union[None, ModuleSpec]:
    """
    A helper method to create module specifications if it does not exist

    Args:
        module_name (str): Input module name to be imported
        module_file_path (str): Input module file path to be imported

    Returns:
        Union[None, ModuleSpec]: Generated module specifications for importing or error
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


def import_module_from_spec(module_spec: ModuleSpec) -> Union[ModuleType, None]:
    """
    A helper method to import python module using module specifications

    Args:
        module_spec (ModuleSpec): A generated module specifications for the module to be imported

    Returns:
        Union[ModuleType, None]: An imported module
    """
    if module_spec is None or not isinstance(module_spec, ModuleSpec):
        return None

    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module
