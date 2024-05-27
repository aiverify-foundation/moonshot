from pathlib import Path

import pytest
from pydantic import ValidationError

from moonshot.api import api_set_environment_variables
from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.storage.storage import Storage


class ObjectInstance:
    def __init__(self, obj_filepath: str):
        TestCollectionStorage.filepath = obj_filepath

    def create_file(self, obj_info: dict) -> bool:
        TestCollectionStorage.obj_info = obj_info
        return True

    def read_file_iterator(
        self, json_keys: list[str], iterator_keys: list[str]
    ) -> bool:
        TestCollectionStorage.json_keys = json_keys
        TestCollectionStorage.iterator_keys = iterator_keys
        return True

    def read_file(self) -> bool:
        return True


class TestCollectionStorage:
    filepath = ""
    obj_info = {}
    json_keys = []
    iterator_keys = []

    @pytest.fixture(autouse=True)
    def init(self):
        # Reset
        TestCollectionStorage.filepath = ""
        TestCollectionStorage.obj_info = {}
        TestCollectionStorage.json_keys = []
        TestCollectionStorage.iterator_keys = []

        api_set_environment_variables(
            {
                # "CONNECTORS": "tests/unit-tests/src/data/connectors/",
                # "CONNECTORS_ENDPOINTS": "tests/unit-tests/src/data/connectors-endpoints/",
                "DATASETS": "tests/unit-tests/src/data/datasets/",
                # "METRICS": "tests/unit-tests/src/data/metrics/",
                # "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Test create_object functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_info,obj_extension,obj_mod_type,expected_dict",
        [
            # Valid case
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            # # Parameter 1
            # (
            #     ObjectInstance,
            #     None,
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "None",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "'None' is not a recognized EnvironmentVar value.",
            #         "expected_exception": "RuntimeError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "'' is not a recognized EnvironmentVar value.",
            #         "expected_exception": "RuntimeError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     {},
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     [],
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     123,
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "modulename",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "'modulename' is not a recognized EnvironmentVar value.",
            #         "expected_exception": "RuntimeError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "datasets",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "'datasets' is not a recognized EnvironmentVar value.",
            #         "expected_exception": "RuntimeError",
            #     },
            # ),
            # # Parameter 2
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     None,
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "None",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     {},
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     [],
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     123,
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "modulename",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # # Parameter 3
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     None,
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid dictionary",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     "None",
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid dictionary",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     "",
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid dictionary",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {},
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     [],
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid dictionary",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     123,
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid dictionary",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     "modulename",
            #     "json",
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid dictionary",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # # Parameter 4
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     None,
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "None",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     {},
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     [],
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     123,
            #     "jsonio",
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "modulename",
            #     "jsonio",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # # Parameter 5
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     None,
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "None",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     {},
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     [],
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     123,
            #     {
            #         "expected_output": False,
            #         "expected_error_message": "Input should be a valid string",
            #         "expected_exception": "ValidationError",
            #     },
            # ),
            # (
            #     ObjectInstance,
            #     "DATASETS",
            #     "my_dataset",
            #     {"info": "MyTestCase"},
            #     "json",
            #     "modulename",
            #     {
            #         "expected_output": True,
            #         "expected_error_message": "",
            #         "expected_exception": "",
            #     },
            # ),
        ],
    )
    def test_create_object(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_info,
        obj_extension,
        obj_mod_type,
        expected_dict,
    ):
        """
        Test the create_object method with various invalid parameters to ensure proper handling of input validation.

        This test uses parametrization to check multiple scenarios where the create_object method
        should fail due to invalid input parameters. It verifies that the appropriate exceptions are raised
        and that the correct error messages are produced.

        Args:
            mocker: A pytest-mock fixture that provides a simple way to patch objects for testing.
            mock_result: The mock object instance to be returned by the patched method.
            obj_type (str): The type of the object to be created.
            obj_id (str): The ID of the object to be created.
            obj_info (dict): A dictionary containing the object information.
            obj_extension (str): The file extension for the object to be created.
            obj_mod_type (str): The module type for object serialization.
            expected_dict (dict): A dictionary containing the expected results of the test case, including
                                  whether the output is expected to be successful, the expected error message,
                                  and the expected exception type.

        Raises:
            ValidationError: If the input parameters fail validation checks.
            RuntimeError: If the object creation fails due to unrecognized EnvironmentVar values or
                          if the object module instance cannot be retrieved or is not callable.
        """
        mocker.patch(
            "moonshot.src.storage.storage.get_instance", return_value=mock_result
        )
        if expected_dict["expected_output"]:
            # Passed validation
            # Failed if enum value is not found
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    Storage.create_object(
                        obj_type, obj_id, obj_info, obj_extension, obj_mod_type
                    )
                assert e.value.args[0] == expected_dict["expected_error_message"]
            else:
                # Passed validation and expected outcome
                assert (
                    Storage.create_object(
                        obj_type, obj_id, obj_info, obj_extension, obj_mod_type
                    )
                    is expected_dict["expected_output"]
                )
                print(TestCollectionStorage.filepath)
                print(f"{EnvironmentVars.DATASETS[1]}/{obj_id}.{obj_extension}")
                assert (
                    TestCollectionStorage.filepath
                    == f"{EnvironmentVars.DATASETS[1]}/{obj_id}.{obj_extension}"
                )
                assert TestCollectionStorage.obj_info == obj_info
        else:
            # Failed validation
            if expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    Storage.create_object(
                        obj_type, obj_id, obj_info, obj_extension, obj_mod_type
                    )
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_info,obj_extension,obj_mod_type,expected_dict",
        [
            # Get filepath invalid response
            (
                [None, ObjectInstance],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to create object.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", ObjectInstance],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            (
                ["", ObjectInstance],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to create object.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [{}, ObjectInstance],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to create object.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [[], ObjectInstance],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to create object.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [123, ObjectInstance],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to create object.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Get instance invalid response
            (
                ["None", None],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", "None"],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", ""],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - ",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", {}],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - {}",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", []],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - []",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", 123],
                "DATASETS",
                "my_dataset",
                {"info": "MyTestCase"},
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - 123",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_create_object_exceptions(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_info,
        obj_extension,
        obj_mod_type,
        expected_dict,
    ):
        """
        Test the create_object method with various combinations of parameters to ensure proper functionality.

        This test uses parametrization to check multiple scenarios where the create_object method
        should succeed or fail based on the provided parameters. It verifies that the expected output
        matches the actual output, and in cases where exceptions are expected, it checks that the correct
        exceptions are raised with the appropriate error messages.

        Args:
            mocker: A pytest-mock fixture that provides a simple way to patch objects for testing.
            mock_result: A tuple containing the mock filepath and the mock object instance to be returned by the patched methods.
            obj_type (str): The type of the object to be created.
            obj_id (str): The ID of the object to be created.
            obj_info (dict): A dictionary containing the object information.
            obj_extension (str): The file extension for the object to be created.
            obj_mod_type (str): The module type for object serialization.
            expected_dict (dict): A dictionary containing the expected results of the test case, including
                                  whether the output is expected to be successful, the expected error message,
                                  and the expected exception type.

        Raises:
            RuntimeError: If the object creation fails due to an error in getting the object module instance or
                          if the filepath cannot be created.
        """
        mocker.patch.object(Storage, "get_filepath", return_value=mock_result[0])
        mocker.patch(
            "moonshot.src.storage.storage.get_instance", return_value=mock_result[1]
        )
        if expected_dict["expected_output"]:
            assert (
                Storage.create_object(
                    obj_type, obj_id, obj_info, obj_extension, obj_mod_type
                )
                is expected_dict["expected_output"]
            )
            assert TestCollectionStorage.filepath == mock_result[0]
            assert TestCollectionStorage.obj_info == obj_info
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    Storage.create_object(
                        obj_type, obj_id, obj_info, obj_extension, obj_mod_type
                    )
                assert e.value.args[0] == expected_dict["expected_error_message"]

    # ------------------------------------------------------------------------------
    # Test read_object_with_iterator functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_extension,obj_mod_type,json_keys,iterator_keys,expected_dict",
        [
            # Valid case
            (
                [f"{EnvironmentVars.DATASETS[1]}/my_dataset.json", ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            # Valid case with None keys
            (
                [f"{EnvironmentVars.DATASETS[1]}/my_dataset.json", ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                None,
                None,
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
        ],
    )
    def test_read_object_with_iterator(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_extension,
        obj_mod_type,
        json_keys,
        iterator_keys,
        expected_dict,
    ):
        """
        Test the read_object_with_iterator method with various combinations of parameters to ensure proper functionality.

        This test uses parametrization to check multiple scenarios where the read_object_with_iterator method
        should succeed based on the provided parameters. It verifies that the expected output matches the actual output.

        Args:
            mocker: A pytest-mock fixture that provides a simple way to patch objects for testing.
            mock_result: A tuple containing the mock filepath and the mock object instance to be returned by the patched methods.
            obj_type (str): The type of the object to be read.
            obj_id (str): The ID of the object to be read.
            obj_extension (str): The file extension for the object to be read.
            obj_mod_type (str): The module type for object serialization.
            json_keys (list): A list of keys to be used for JSON object transformation.
            iterator_keys (list): A list of keys to be used for iterating over the JSON objects.
            expected_dict (dict): A dictionary containing the expected results of the test case, including
                                  whether the output is expected to be successful.

        Raises:
            AssertionError: If the actual output does not match the expected output.
        """
        mocker.patch.object(Storage, "get_filepath", return_value=mock_result[0])
        mocker.patch(
            "moonshot.src.storage.storage.get_instance", return_value=mock_result[1]
        )
        # Passed validation and expected outcome
        assert (
            Storage.read_object_with_iterator(
                obj_type, obj_id, obj_extension, obj_mod_type, json_keys, iterator_keys
            )
            is expected_dict["expected_output"]
        )
        assert (
            TestCollectionStorage.filepath
            == f"{EnvironmentVars.DATASETS[1]}/{obj_id}.{obj_extension}"
        )
        assert TestCollectionStorage.json_keys == json_keys
        assert TestCollectionStorage.iterator_keys == iterator_keys

    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_extension,expected_dict",
        [
            # Test cases for verifying the behavior of Storage.read_object_with_iterator
            # when invalid parameters are provided for the filepath.
            # Each tuple represents a test case with the following parameters:
            # - mock_result: The mock object instance to be returned by the patched method.
            # - obj_type: The type of the object, which may be invalid.
            # - obj_id: The ID of the object, which may be invalid.
            # - obj_extension: The file extension for the object, which may be invalid.
            # - expected_dict: A dictionary containing the expected error message and exception type.
            # Parameter 1
            # Test case with obj_type as None
            (
                ObjectInstance,
                None,
                "my_dataset",
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_type as string 'None'
            (
                ObjectInstance,
                "None",
                "my_dataset",
                "json",
                {
                    "expected_error_message": "'None' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_type as an empty string
            (
                ObjectInstance,
                "",
                "my_dataset",
                "json",
                {
                    "expected_error_message": "'' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_type as an empty dictionary
            (
                ObjectInstance,
                {},
                "my_dataset",
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_type as an empty list
            (
                ObjectInstance,
                [],
                "my_dataset",
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_type as a number
            (
                ObjectInstance,
                123,
                "my_dataset",
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_type as an unrecognized string
            (
                ObjectInstance,
                "newmodule",
                "my_dataset",
                "json",
                {
                    "expected_error_message": "'newmodule' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Parameter 2
            # Test case with obj_id as None
            (
                ObjectInstance,
                "DATASETS",
                None,
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_id as string 'None'
            (
                ObjectInstance,
                "DATASETS",
                "None",
                "json",
                {
                    "expected_error_message": "No datasets found with ID: None",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_id as an empty string
            (
                ObjectInstance,
                "DATASETS",
                "",
                "json",
                {
                    "expected_error_message": "No datasets found with ID: ",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_id as an empty dictionary
            (
                ObjectInstance,
                "DATASETS",
                {},
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_id as an empty list
            (
                ObjectInstance,
                "DATASETS",
                [],
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_id as a number
            (
                ObjectInstance,
                "DATASETS",
                123,
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_id as an unrecognized string
            (
                ObjectInstance,
                "DATASETS",
                "newmodule",
                "json",
                {
                    "expected_error_message": "No datasets found with ID: newmodule",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Parameter 3
            # Test case with obj_extension as None
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                None,
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_extension as string 'None'
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                "None",
                {
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_extension as an empty string
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                "",
                {
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_extension as an empty dictionary
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                {},
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_extension as an empty list
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                [],
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_extension as a number
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                123,
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_extension as an unrecognized string
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                "newmodule",
                {
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_read_object_with_iterator_invalid_filepath(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_extension,
        expected_dict,
    ):
        """
        Test the read_object_with_iterator method with invalid parameters for the filepath.

        This test ensures that the method raises the appropriate exceptions and error messages
        when provided with invalid parameters for the object type, ID, or file extension.

        Args:
            mocker: A pytest-mock fixture that provides a simple way to patch objects for testing.
            mock_result: The mock object instance to be returned by the patched method.
            obj_type (str | None): The type of the object, which may be invalid.
            obj_id (str | None): The ID of the object, which may be invalid.
            obj_extension (str | None): The file extension for the object, which may be invalid.
            expected_dict (dict): A dictionary containing the expected error message and exception type.

        Raises:
            AssertionError: If the actual exception raised does not match the expected exception.
            RuntimeError: If the expected exception is RuntimeError and it is not raised as expected.
            ValidationError: If the expected exception is ValidationError and it is not raised as expected.
        """
        mocker.patch(
            "moonshot.src.storage.storage.get_instance", return_value=mock_result
        )
        if expected_dict["expected_exception"] == "RuntimeError":
            with pytest.raises(RuntimeError) as e:
                Storage.read_object_with_iterator(obj_type, obj_id, obj_extension)
            assert e.value.args[0] == expected_dict["expected_error_message"]

        elif expected_dict["expected_exception"] == "ValidationError":
            with pytest.raises(ValidationError) as e:
                Storage.read_object_with_iterator(obj_type, obj_id, obj_extension)
            assert len(e.value.errors()) == 1
            assert expected_dict["expected_error_message"] in e.value.errors()[0]["msg"]

        else:
            assert False

    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_extension,obj_mod_type,json_keys,iterator_keys,expected_dict",
        [
            # Get filepath invalid response
            (
                [None, ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            (
                ["", ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [{}, ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [[], ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [123, ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Get instance invalid response
            (
                ["None", None],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", "None"],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", ""],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - ",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", {}],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - {}",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", []],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - []",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", 123],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                ["name"],
                ["id"],
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - 123",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_read_object_with_iterator_exceptions(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_extension,
        obj_mod_type,
        json_keys,
        iterator_keys,
        expected_dict,
    ):
        """
        Test the read_object_with_iterator method for handling exceptions.

        This test ensures that the read_object_with_iterator method raises the expected exceptions
        and produces the correct error messages when encountering invalid input or when the system
        is unable to perform the requested operations. It uses parametrization to test a variety of
        scenarios that should result in specific exceptions being raised.

        Args:
            mocker: A pytest-mock fixture that provides a simple way to patch objects for testing.
            mock_result: A list containing the mock filepath and the mock object instance to be returned by the patched methods.
            obj_type (str): The type of the object to be read.
            obj_id (str): The ID of the object to be read.
            obj_extension (str): The file extension for the object to be read.
            obj_mod_type (str): The module type for object serialization.
            json_keys (list): A list of keys to be used for JSON object transformation.
            iterator_keys (list): A list of keys to be used for iterating over the JSON objects.
            expected_dict (dict): A dictionary containing the expected results of the test case, including
                                  whether the output is expected to be successful, the expected error message,
                                  and the expected exception type.

        Raises:
            AssertionError: If the actual output does not match the expected output.
            RuntimeError: If the expected exception is RuntimeError and it is not raised as expected.
        """
        mocker.patch.object(Storage, "get_filepath", return_value=mock_result[0])
        mocker.patch(
            "moonshot.src.storage.storage.get_instance", return_value=mock_result[1]
        )
        if expected_dict["expected_output"]:
            assert (
                Storage.read_object_with_iterator(
                    obj_type,
                    obj_id,
                    obj_extension,
                    obj_mod_type,
                    json_keys,
                    iterator_keys,
                )
                is expected_dict["expected_output"]
            )
            assert TestCollectionStorage.json_keys == json_keys
            assert TestCollectionStorage.iterator_keys == iterator_keys
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    Storage.read_object_with_iterator(
                        obj_type,
                        obj_id,
                        obj_extension,
                        obj_mod_type,
                        json_keys,
                        iterator_keys,
                    )
                assert e.value.args[0] == expected_dict["expected_error_message"]

    # ------------------------------------------------------------------------------
    # Test read_object functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_extension,obj_mod_type,expected_dict",
        [
            # Valid case
            (
                [f"{EnvironmentVars.DATASETS[1]}/my_dataset.json", ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            # Valid case with None keys
            (
                [f"{EnvironmentVars.DATASETS[1]}/my_dataset.json", ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
        ],
    )
    def test_read_object(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_extension,
        obj_mod_type,
        expected_dict,
    ):
        """
        Test the Storage.read_object method with various parameters.

        This test ensures that the read_object method returns the correct output
        and that the filepath is constructed as expected. It uses parametrization
        to test different scenarios, including valid cases with and without keys.

        Args:
            mocker: A pytest-mock fixture that provides a simple way to patch objects for testing.
            mock_result: A tuple containing the mock filepath and the mock object instance.
            obj_type (str): The type of the object to be read.
            obj_id (str): The ID of the object to be read.
            obj_extension (str): The file extension for the object to be read.
            obj_mod_type (str): The module type for object serialization.
            expected_dict (dict): A dictionary containing the expected results of the test case,
                                  including whether the output is expected to be successful,
                                  the expected error message, and the expected exception type.

        Raises:
            AssertionError: If the actual output does not match the expected output or
                            if the constructed filepath does not match the expected filepath.
        """
        mocker.patch.object(Storage, "get_filepath", return_value=mock_result[0])
        mocker.patch(
            "moonshot.src.storage.storage.get_instance", return_value=mock_result[1]
        )
        # Passed validation and expected outcome
        assert (
            Storage.read_object(obj_type, obj_id, obj_extension, obj_mod_type)
            is expected_dict["expected_output"]
        )
        assert (
            TestCollectionStorage.filepath
            == f"{EnvironmentVars.DATASETS[1]}/{obj_id}.{obj_extension}"
        )

    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_extension,expected_dict",
        [
            # Test cases for verifying the behavior of Storage.read_object_with_iterator
            # when invalid parameters are provided for the filepath.
            # Each tuple represents a test case with the following parameters:
            # - mock_result: The mock object instance to be returned by the patched method.
            # - obj_type: The type of the object, which may be invalid.
            # - obj_id: The ID of the object, which may be invalid.
            # - obj_extension: The file extension for the object, which may be invalid.
            # - expected_dict: A dictionary containing the expected error message and exception type.
            # Parameter 1
            # Test case with obj_type as None
            (
                ObjectInstance,
                None,
                "my_dataset",
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_type as string 'None'
            (
                ObjectInstance,
                "None",
                "my_dataset",
                "json",
                {
                    "expected_error_message": "'None' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_type as an empty string
            (
                ObjectInstance,
                "",
                "my_dataset",
                "json",
                {
                    "expected_error_message": "'' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_type as an empty dictionary
            (
                ObjectInstance,
                {},
                "my_dataset",
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_type as an empty list
            (
                ObjectInstance,
                [],
                "my_dataset",
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_type as a number
            (
                ObjectInstance,
                123,
                "my_dataset",
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_type as an unrecognized string
            (
                ObjectInstance,
                "newmodule",
                "my_dataset",
                "json",
                {
                    "expected_error_message": "'newmodule' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Parameter 2
            # Test case with obj_id as None
            (
                ObjectInstance,
                "DATASETS",
                None,
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_id as string 'None'
            (
                ObjectInstance,
                "DATASETS",
                "None",
                "json",
                {
                    "expected_error_message": "No datasets found with ID: None",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_id as an empty string
            (
                ObjectInstance,
                "DATASETS",
                "",
                "json",
                {
                    "expected_error_message": "No datasets found with ID: ",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_id as an empty dictionary
            (
                ObjectInstance,
                "DATASETS",
                {},
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_id as an empty list
            (
                ObjectInstance,
                "DATASETS",
                [],
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_id as a number
            (
                ObjectInstance,
                "DATASETS",
                123,
                "json",
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_id as an unrecognized string
            (
                ObjectInstance,
                "DATASETS",
                "newmodule",
                "json",
                {
                    "expected_error_message": "No datasets found with ID: newmodule",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Parameter 3
            # Test case with obj_extension as None
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                None,
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_extension as string 'None'
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                "None",
                {
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_extension as an empty string
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                "",
                {
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Test case with obj_extension as an empty dictionary
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                {},
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_extension as an empty list
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                [],
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_extension as a number
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                123,
                {
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Test case with obj_extension as an unrecognized string
            (
                ObjectInstance,
                "DATASETS",
                "my_dataset",
                "newmodule",
                {
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_read_object_invalid_filepath(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_extension,
        expected_dict,
    ):
        """
        Tests the behavior of Storage.read_object when invalid parameters are provided for the filepath.

        This test ensures that the method raises the appropriate exceptions and error messages when given invalid
        parameters for the object type, ID, and file extension.

        Args:
            mocker: The pytest-mock plugin that provides a convenient interface for mocking objects.
            mock_result: The mock object instance to be returned by the patched method.
            obj_type (str): The type of the object, which may be invalid.
            obj_id (str): The ID of the object, which may be invalid.
            obj_extension (str): The file extension for the object, which may be invalid.
            expected_dict (dict): A dictionary containing the expected error message and exception type.
        """
        mocker.patch(
            "moonshot.src.storage.storage.get_instance", return_value=mock_result
        )
        if expected_dict["expected_exception"] == "RuntimeError":
            with pytest.raises(RuntimeError) as e:
                Storage.read_object(obj_type, obj_id, obj_extension)
            assert e.value.args[0] == expected_dict["expected_error_message"]

        elif expected_dict["expected_exception"] == "ValidationError":
            with pytest.raises(ValidationError) as e:
                Storage.read_object(obj_type, obj_id, obj_extension)
            assert len(e.value.errors()) == 1
            assert expected_dict["expected_error_message"] in e.value.errors()[0]["msg"]

        else:
            assert False

    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_extension,obj_mod_type,expected_dict",
        [
            # Get filepath invalid response
            (
                [None, ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            (
                ["", ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [{}, ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [[], ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [123, ObjectInstance],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Get instance invalid response
            (
                ["None", None],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", "None"],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", ""],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - ",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", {}],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - {}",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", []],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - []",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                ["None", 123],
                "DATASETS",
                "my_dataset",
                "json",
                "jsonio",
                {
                    "expected_output": False,
                    "expected_error_message": "Unable to get defined object module instance - 123",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_read_object_exceptions(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_extension,
        obj_mod_type,
        expected_dict,
    ):
        """
        Test the read_object method for handling exceptions.

        This test ensures that the read_object method raises the expected exceptions
        and produces the correct error messages when encountering invalid input or when the system
        is unable to perform the requested operations. It uses parametrization to test a variety of
        scenarios that should result in specific exceptions being raised.

        Args:
            mocker: A pytest-mock fixture that provides a simple way to patch objects for testing.
            mock_result: A list containing the mock filepath and the mock object instance to be returned by the patched methods.
            obj_type (str): The type of the object to be read.
            obj_id (str): The ID of the object to be read.
            obj_extension (str): The file extension for the object to be read.
            obj_mod_type (str): The module type for object serialization.
            expected_dict (dict): A dictionary containing the expected results of the test case, including
                                  whether the output is expected to be successful, the expected error message,
                                  and the expected exception type.

        Raises:
            AssertionError: If the actual output does not match the expected output.
            RuntimeError: If the expected exception is RuntimeError and it is not raised as expected.
        """
        mocker.patch.object(Storage, "get_filepath", return_value=mock_result[0])
        mocker.patch(
            "moonshot.src.storage.storage.get_instance", return_value=mock_result[1]
        )
        if expected_dict["expected_output"]:
            assert (
                Storage.read_object(obj_type, obj_id, obj_extension, obj_mod_type)
                is expected_dict["expected_output"]
            )
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    Storage.read_object(obj_type, obj_id, obj_extension, obj_mod_type)
                assert e.value.args[0] == expected_dict["expected_error_message"]

    # ------------------------------------------------------------------------------
    # Test delete_object functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_extension,expected_dict",
        [
            # Valid case
            (
                f"{EnvironmentVars.DATASETS[1]}/my_dataset.json",
                "DATASETS",
                "my_dataset",
                "json",
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            # Invalid case
            (
                "",
                "DATASETS",
                "my_dataset",
                "json",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_delete_object(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_extension,
        expected_dict,
    ):
        """
        Test the delete_object method for correct behavior and exception handling.

        This test checks whether the delete_object method of the Storage class correctly deletes
        an object or raises the appropriate exceptions when deletion is not possible. It uses
        parametrization to test both valid and invalid cases.

        Args:
            mocker: A pytest-mock fixture that provides a simple way to patch objects for testing.
            mock_result (str): The mock filepath to be returned by the patched get_filepath method.
            obj_type (str): The type of the object to be deleted.
            obj_id (str): The ID of the object to be deleted.
            obj_extension (str): The file extension for the object to be deleted.
            expected_dict (dict): A dictionary containing the expected results of the test case, including
                                  whether the deletion is expected to be successful, the expected error message,
                                  and the expected exception type.

        Raises:
            AssertionError: If the actual output does not match the expected output.
            RuntimeError: If the expected exception is RuntimeError and it is not raised as expected.
        """
        mocker.patch.object(Storage, "get_filepath", return_value=mock_result)
        mocker.patch.object(Path, "unlink")

        if expected_dict["expected_output"]:
            assert Storage.delete_object(obj_type, obj_id, obj_extension) is True
        else:
            with pytest.raises(RuntimeError) as exc_info:
                Storage.delete_object(obj_type, obj_id, obj_extension)
            assert exc_info.value.args[0] == expected_dict["expected_error_message"]

    # ------------------------------------------------------------------------------
    # Test is_object_exists functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "mock_result,obj_type,obj_id,obj_extension,expected_dict",
        [
            # Valid case
            (
                f"{EnvironmentVars.DATASETS[1]}/my_dataset.json",
                "DATASETS",
                "my_dataset",
                "json",
                {
                    "expected_output": True,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            # Valid case
            (
                f"{EnvironmentVars.DATASETS[1]}/my_dataset.json",
                "DATASETS",
                "my_dataset",
                "json",
                {
                    "expected_output": False,
                    "expected_error_message": "",
                    "expected_exception": "",
                },
            ),
            # Invalid case
            (
                "",
                "DATASETS",
                "my_dataset",
                "json",
                {
                    "expected_output": False,
                    "expected_error_message": "No datasets found with ID: my_dataset",
                    "expected_exception": "RuntimeError",
                },
            ),
        ],
    )
    def test_is_object_exists(
        self,
        mocker,
        mock_result,
        obj_type,
        obj_id,
        obj_extension,
        expected_dict,
    ):
        """
        Test the Storage.is_object_exists method.

        This test ensures that the Storage.is_object_exists method correctly identifies whether an object exists
        in storage based on the object type, ID, and file extension. It uses mocking to simulate the existence
        of the object file path and its existence on the file system.

        Args:
            mocker: A pytest-mock fixture used to mock objects for testing.
            mock_result (str): The file path to be returned by the mocked Storage.get_filepath method.
            obj_type (str): The type of the object (e.g., 'DATASETS').
            obj_id (str): The ID of the object.
            obj_extension (str): The file extension of the object (e.g., 'json').
            expected_dict (dict): A dictionary containing the expected output of the test and any expected error message.

        Asserts:
            The result of Storage.is_object_exists is as expected based on the test parameters.
        """
        mocker.patch.object(Storage, "get_filepath", return_value=mock_result)
        mocker.patch.object(
            Path, "exists", return_value=expected_dict["expected_output"]
        )
        assert (
            Storage.is_object_exists(obj_type, obj_id, obj_extension)
            is expected_dict["expected_output"]
        )

    # ------------------------------------------------------------------------------
    # Test get_objects functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "obj_type,obj_extension,expected_dict",
        [
            # Valid case
            (
                "DATASETS",
                "json",
                {
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_output": [
                        "tests/unit-tests/src/importmodules/arc-easy.json"
                    ],
                },
            ),
            (
                "DATASETS",
                "py",
                {
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_output": [
                        "tests/unit-tests/src/importmodules/__init__.py",
                        "tests/unit-tests/src/importmodules/sample_file.py",
                    ],
                },
            ),
            (
                "DATASETS",
                "pdf",
                {
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_output": [],
                },
            ),
        ],
    )
    def test_get_objects(self, mocker, obj_type, obj_extension, expected_dict):
        """
        Test the retrieval of object file paths from storage.

        This test ensures that the Storage.get_objects method returns an iterator that yields the correct file paths
        for a given object type and file extension. It mocks the EnvironmentVars.get_file_directory method to return
        a predefined list of directories and then checks if the list of file paths obtained from the iterator matches
        the expected output.

        Args:
            mocker: A pytest-mock fixture used to mock objects for testing.
            obj_type (str): The type of the object whose files are to be retrieved.
            obj_extension (str): The file extension of the object files to be retrieved.
            expected_dict (dict): A dictionary containing the 'directory' key with a list of directories to be returned
                                  by the mocked method, and the 'expected_output' key with the expected list of file paths.

        Raises:
            AssertionError: If the list of file paths does not match the expected output.
        """
        mocker.patch.object(
            EnvironmentVars,
            "get_file_directory",
            return_value=expected_dict["directory"],
        )
        iterator = Storage.get_objects(obj_type, obj_extension)
        try:
            files_list = [value for value in iterator]
            assert files_list == expected_dict["expected_output"]
        except StopIteration:
            print("No more prompts")

    @pytest.mark.parametrize(
        "obj_type,obj_extension,expected_dict",
        [
            # Parameter 1
            (
                None,
                "json",
                {
                    "to_mock": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                "json",
                {
                    "to_mock": False,
                    "expected_error_message": "'None' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                "json",
                {
                    "to_mock": False,
                    "expected_error_message": "'' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                "json",
                {
                    "to_mock": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                "json",
                {
                    "to_mock": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                "json",
                {
                    "to_mock": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "newmodule",
                "json",
                {
                    "to_mock": False,
                    "expected_error_message": "'newmodule' is not a recognized EnvironmentVar value.",
                    "expected_exception": "RuntimeError",
                },
            ),
            # Parameter 2
            (
                "DATASETS",
                None,
                {
                    "to_mock": True,
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "DATASETS",
                "None",
                {
                    "to_mock": True,
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_output": [],
                    "expected_exception": "",
                },
            ),
            (
                "DATASETS",
                "",
                {
                    "to_mock": True,
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_output": [],
                    "expected_exception": "",
                },
            ),
            (
                "DATASETS",
                {},
                {
                    "to_mock": True,
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "DATASETS",
                [],
                {
                    "to_mock": True,
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "DATASETS",
                123,
                {
                    "to_mock": True,
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "DATASETS",
                "newmodule",
                {
                    "to_mock": True,
                    "directory": ["tests/unit-tests/src/importmodules/"],
                    "expected_output": [],
                    "expected_exception": "",
                },
            ),
        ],
    )
    def test_get_objects_invalid_arguments(
        self, mocker, obj_type, obj_extension, expected_dict
    ):
        """
        Test the Storage.get_objects method with invalid arguments.

        This test verifies that the Storage.get_objects method raises the appropriate exceptions or returns the correct
        output when called with invalid arguments. It uses parameterization to test a variety of invalid inputs and
        expected outcomes, including different object types, file extensions, and expected exceptions.

        Args:
            mocker: A pytest-mock fixture used to mock objects for testing.
            obj_type (str | None | dict | list | int): The type of the object whose files are to be retrieved, which can be invalid.
            obj_extension (str | None | dict | list | int): The file extension of the object files to be retrieved, which can be invalid.
            expected_dict (dict): A dictionary containing the 'to_mock' key indicating whether to mock the EnvironmentVars.get_file_directory method,
                                  the 'directory' key with a list of directories to be returned by the mocked method if applicable,
                                  the 'expected_output' key with the expected list of file paths if no exception is expected,
                                  the 'expected_error_message' key with the expected error message if an exception is expected,
                                  and the 'expected_exception' key with the name of the expected exception class.

        Raises:
            AssertionError: If the actual outcome does not match the expected outcome.
        """
        if expected_dict["to_mock"]:
            mocker.patch.object(
                EnvironmentVars,
                "get_file_directory",
                return_value=expected_dict["directory"],
            )

        if expected_dict["expected_exception"] == "RuntimeError":
            with pytest.raises(RuntimeError) as e:
                Storage.get_objects(obj_type, obj_extension)
            assert e.value.args[0] == expected_dict["expected_error_message"]

        elif expected_dict["expected_exception"] == "ValidationError":
            with pytest.raises(ValidationError) as e:
                Storage.get_objects(obj_type, obj_extension)
            assert len(e.value.errors()) == 1
            assert expected_dict["expected_error_message"] in e.value.errors()[0]["msg"]

        else:
            iterator = Storage.get_objects(obj_type, obj_extension)
            try:
                files_list = [value for value in iterator]
                assert files_list == expected_dict["expected_output"]
            except StopIteration:
                print("No more prompts")

    # ------------------------------------------------------------------------------
    # Test count_objects functionality
    # ------------------------------------------------------------------------------
