from __future__ import annotations

from importlib.machinery import ModuleSpec
from types import ModuleType

import pytest

from moonshot.src.utils.import_modules import (
    create_module_spec,
    get_instance,
    import_module_from_spec,
)


class TestCollectionImportModules:
    """
    Test suite for testing the import_modules utility functions.

    Attributes:
        valid_init_module_file_path (str): A valid file path to an __init__.py file for testing.
        valid_module_file_path (str): A valid file path to a sample Python file for testing.
    """

    valid_init_module_file_path = "tests/unit-tests/common/samples/__init__.py"
    valid_module_file_path = "tests/unit-tests/common/samples/sample_file.py"

    # ------------------------------------------------------------------------------
    # Test create_module_spec functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "module_name, module_file_path, expected_result",
        [
            ("modulename", valid_module_file_path, True),
            ("newmodulename", valid_module_file_path, True),
            ("newmodulename", valid_init_module_file_path, True),
            (None, valid_module_file_path, None),
            ("None", valid_module_file_path, True),
            ({}, valid_module_file_path, None),
            ([], valid_module_file_path, None),
            (123, valid_module_file_path, None),
            ("modulename", None, None),
            ("modulename", "None", None),
            ("modulename", {}, None),
            ("modulename", [], None),
            ("modulename", 123, None),
        ],
    )
    def test_create_module_spec(self, module_name, module_file_path, expected_result):
        """
        Test the create_module_spec function with various inputs to ensure it returns
        a ModuleSpec object when given valid inputs, and None otherwise.

        Args:
            module_name (str | None): The name of the module to create a spec for.
            module_file_path (str | None): The file path of the module to create a spec for.
            expected_result (bool | None): The expected result of the test (True for success, None for failure).
        """
        output = create_module_spec(module_name, module_file_path)
        if expected_result:
            assert isinstance(output, ModuleSpec)
        else:
            assert output is expected_result

    # ------------------------------------------------------------------------------
    # Test import_module_from_spec functionality
    # ------------------------------------------------------------------------------
    def test_import_module_from_spec(self):
        """
        Test the import_module_from_spec function to ensure it can import a module
        from a given module specification.
        """
        module_spec = create_module_spec("module_name", self.valid_module_file_path)
        output = import_module_from_spec(module_spec)
        assert isinstance(output, ModuleType)

    @pytest.mark.parametrize(
        "module_spec, expected_result",
        [
            ("modulename", None),
            (None, None),
            ("None", None),
            ({}, None),
            ([], None),
            (123, None),
        ],
    )
    def test_import_module_from_spec_errors(self, module_spec, expected_result):
        """
        Test the import_module_from_spec function with invalid module specifications
        to ensure it handles errors correctly and returns None.

        Args:
            module_spec (str | None): The module specification to test.
            expected_result (None): The expected result of the test, which is always None for invalid inputs.
        """
        output = import_module_from_spec(module_spec)
        assert output == expected_result

    @pytest.mark.parametrize(
        "id, filepath, expected_result",
        [
            (
                "OpenAIConnector",
                valid_module_file_path,
                "<class 'OpenAIConnector.OpenAIConnector'>",
            ),
            ("newmodulename", valid_init_module_file_path, None),
            ("", valid_module_file_path, None),
            (None, valid_module_file_path, None),
            ("None", valid_module_file_path, None),
            ([], valid_module_file_path, None),
            ({}, valid_module_file_path, None),
            ("OpenAIConnector", "", None),
            ("OpenAIConnector", None, None),
            ("OpenAIConnector", "None", None),
            ("OpenAIConnector", [], None),
            ("OpenAIConnector", {}, None),
        ],
    )
    def test_get_instance(self, id, filepath, expected_result):
        """
        Test the get_instance function with various inputs to ensure it returns
        the correct class instance when given valid inputs, and None otherwise.

        Args:
            id (str | None): The identifier of the class to instantiate.
            filepath (str | None): The file path of the module containing the class.
            expected_result (str | None): The expected string representation of the instance or None.
        """
        instance = get_instance(id, filepath)
        if expected_result:
            assert str(instance) == expected_result
        else:
            assert instance is expected_result
