
from importlib.machinery import ModuleSpec
from types import ModuleType

import pytest

from moonshot.src.utils.import_modules import create_module_spec, import_module_from_spec


class TestCollectionImportModules:
    @pytest.mark.parametrize(
        "module_name, module_file_path, expected_result",
        [
            ("modulename", "tests/importmodules/example_serializer.py", True),
            ("newmodulename", "tests/importmodules/example_serializer.py", True),
            (None, "tests/importmodules/example_serializer.py", None),
            ("None", "tests/importmodules/example_serializer.py", True),
            ({}, "tests/importmodules/example_serializer.py", None),
            ([], "tests/importmodules/example_serializer.py", None),
            (123, "tests/importmodules/example_serializer.py", None),
            ("modulename", None, None),
            ("modulename", "None", None),
            ("modulename", {}, None),
            ("modulename", [], None),
            ("modulename", 123, None),
        ],
    )
    def test_create_module_spec(self, module_name, module_file_path, expected_result):
        """
        Tests that it can create module spec
        """
        output = create_module_spec(module_name, module_file_path)
        if expected_result:
            assert isinstance(output, ModuleSpec)
        else:
            assert output == expected_result

    def test_import_module_from_spec(self):
        """
        Tests that it can import modules from spec
        """
        module_spec = create_module_spec(
            "module_name", "tests/importmodules/example_serializer.py"
        )
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
        Tests that it can create module spec
        """
        output = import_module_from_spec(module_spec)
        if expected_result:
            assert isinstance(output, ModuleType)
        else:
            assert output == expected_result
