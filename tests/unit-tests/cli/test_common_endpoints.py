from argparse import Namespace
from ast import literal_eval
from unittest.mock import MagicMock, patch

import pytest
from _pytest.assertion import truncate

from moonshot.integrations.cli.common.connectors import (
    add_endpoint,
    delete_endpoint,
    list_connector_types,
    list_endpoints,
    update_endpoint,
    view_endpoint,
)

truncate.DEFAULT_MAX_LINES = 9999
truncate.DEFAULT_MAX_CHARS = 9999


class TestCollectionCliConnectors:
    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Add Endpoint
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "connector_type, name, uri, token, max_calls_per_second, max_concurrency, model, params, expected_output",
        [
            # Valid cases
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: Endpoint (test-connector) created.",
            ),
            (
                "openai-connector",
                "'test_connector'",
                "example uri",
                "example token",
                2,
                3,
                "gpt-3.5-turbo-1106",
                "{'temperature': 1.5, 'new': 'field'}",
                "[add_endpoint]: Endpoint (test-connector) created.",
            ),
            # Invalid connector_type
            (
                None,
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'connector_type' argument must be a non-empty string and not None.",
            ),
            (
                ["invalid connector type"],
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'connector_type' argument must be a non-empty string and not None.",
            ),
            (
                {"invalid connector": "type"},
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'connector_type' argument must be a non-empty string and not None.",
            ),
            (
                123,
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'connector_type' argument must be a non-empty string and not None.",
            ),
            (
                True,
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'connector_type' argument must be a non-empty string and not None.",
            ),
            # Invalid name
            (
                "openai-connector",
                None,
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                ["invalid name"],
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                {"invalid": "name"},
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                123,
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                True,
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'name' argument must be a non-empty string and not None.",
            ),
            # Invalid uri
            (
                "openai-connector",
                "'test connector'",
                None,
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'uri' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                ["invalid uri"],
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'uri' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                {"invalid": "uri"},
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'uri' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                123,
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'uri' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                True,
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'uri' argument must be a non-empty string and not None.",
            ),
            # Invalid token
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                None,
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'token' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                ["invalid token"],
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'token' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                {"invalid": "token"},
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'token' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                123,
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'token' argument must be a non-empty string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                True,
                1,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'token' argument must be a non-empty string and not None.",
            ),
            # Invalid max_calls_per_second
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                None,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_calls_per_second' argument must be a non-empty positive integer and not None.",  # noqa: E501
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                "invalid",
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_calls_per_second' argument must be a non-empty positive integer and not None.",  # noqa: E501
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                ["invalid"],
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_calls_per_second' argument must be a non-empty positive integer and not None.",  # noqa: E501
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                {"invalid"},
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_calls_per_second' argument must be a non-empty positive integer and not None.",  # noqa: E501
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                0.23,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_calls_per_second' argument must be a non-empty positive integer and not None.",  # noqa: E501
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                False,
                1,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_calls_per_second' argument must be a non-empty positive integer and not None.",  # noqa: E501
            ),
            # Invalid max_concurrency
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                None,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_concurrency' argument must be a non-empty positive integer and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                "invalid",
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_concurrency' argument must be a non-empty positive integer and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                ["invalid"],
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_concurrency' argument must be a non-empty positive integer and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                {"invalid"},
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_concurrency' argument must be a non-empty positive integer and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                0.23,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_concurrency' argument must be a non-empty positive integer and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                False,
                "gpt-3.5-turbo-1106",
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'max_concurrency' argument must be a non-empty positive integer and not None.",
            ),
            # Invalid model
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                None,
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'model' argument must be a string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                ["invalid"],
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'model' argument must be a string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                {"invalid"},
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'model' argument must be a string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                0.23,
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'model' argument must be a string and not None.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                False,
                "{'temperature': 0.5}",
                "[add_endpoint]: The 'model' argument must be a string and not None.",
            ),
            # Invalid params
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                "",
                "[add_endpoint]: The 'params' argument must be a string representation of a dictionary.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                [],
                "[add_endpoint]: The 'params' argument must be a string representation of a dictionary.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                {},
                "[add_endpoint]: The 'params' argument must be a string representation of a dictionary.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                True,
                "[add_endpoint]: The 'params' argument must be a string representation of a dictionary.",
            ),
            (
                "openai-connector",
                "'test connector'",
                "example_uri",
                "example_token",
                1,
                1,
                "gpt-3.5-turbo-1106",
                0.123,
                "[add_endpoint]: The 'params' argument must be a string representation of a dictionary.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.common.connectors.api_create_endpoint")
    def test_add_endpoint(
        self,
        mock_api_create_endpoint,
        connector_type,
        name,
        uri,
        token,
        max_calls_per_second,
        max_concurrency,
        model,
        params,
        expected_output,
        capsys,
    ):
        if "error" in expected_output:
            mock_api_create_endpoint.side_effect = Exception(
                "An error has occurred while creating endpoint."
            )
        else:
            mock_api_create_endpoint.return_value = "test-connector"

        args = Namespace(
            connector_type=connector_type,
            name=name,
            uri=uri,
            token=token,
            max_calls_per_second=max_calls_per_second,
            max_concurrency=max_concurrency,
            model=model,
            params=params,
        )

        add_endpoint(args)

        captured = capsys.readouterr()
        assert expected_output == captured.out.strip()

        if (
            isinstance(name, str)
            and name
            and isinstance(connector_type, str)
            and connector_type
            and isinstance(uri, str)
            and uri
            and isinstance(token, str)
            and token
            and isinstance(max_calls_per_second, int)
            and max_calls_per_second
            and isinstance(max_concurrency, int)
            and max_concurrency
            and isinstance(model, str)
            and model
        ):
            try:
                params_dict = literal_eval(params)
                if not (isinstance(params_dict, dict)):
                    raise ValueError(
                        "The 'params' argument must be a dictionary after evaluation."
                    )
            except Exception:
                params_dict = None
            if params_dict is not None:
                mock_api_create_endpoint.assert_called_once_with(
                    name,
                    connector_type,
                    uri,
                    token,
                    max_calls_per_second,
                    max_concurrency,
                    model,
                    params_dict,
                )
            else:
                mock_api_create_endpoint.assert_not_called()
        else:
            mock_api_create_endpoint.assert_not_called()

    # ------------------------------------------------------------------------------
    # List Endpoint with non-mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, expected_output, expected_log",
        [
            # Valid cases with no filter
            (
                None,
                None,
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                "",
            ),
            # No endpoints
            (
                None,
                None,
                [],
                None,
                "There are no endpoints found.",
            ),
            # Valid case with find
            (
                "endpoint",
                None,
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    },
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                "",
            ),
            # Valid case with find but no results
            (
                "nothingvalid",
                None,
                [],
                None,
                "There are no endpoints found.",
            ),
            # Valid case with pagination
            (
                None,
                "(1, 1)",
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                        "idx": 1,
                    }
                ],
                "",
            ),
            # Valid case with pagination but no results
            (
                "Endpoint",
                "(1, 1)",
                [],
                None,
                "There are no endpoints found.",
            ),
            # Invalid cases for find
            (
                "",
                None,
                None,
                None,
                "[list_endpoints]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                99,
                None,
                None,
                None,
                "[list_endpoints]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                {},
                None,
                None,
                None,
                "[list_endpoints]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                [],
                None,
                None,
                None,
                "[list_endpoints]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                (),
                None,
                None,
                None,
                "[list_endpoints]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                True,
                None,
                None,
                None,
                "[list_endpoints]: The 'find' argument must be a non-empty string and not None.",
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                99,
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                {},
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                [],
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                (),
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                True,
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                True,
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                "(1, 'a')",
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(1, 2, 3)",
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(1, )",
                None,
                None,
                "[list_endpoints]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(0, 1)",
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                None,
                "[list_endpoints]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(1, 0)",
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                None,
                "[list_endpoints]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(0, 0)",
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                None,
                "[list_endpoints]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(1, -1)",
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                None,
                "[list_endpoints]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(-1, 1)",
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                None,
                "[list_endpoints]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            (
                None,
                "(-1, -1)",
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                None,
                "[list_endpoints]: Invalid page number or page size. Page number and page size should start from 1.",
            ),
            # Exception case
            (
                None,
                None,
                None,
                None,
                "[list_endpoints]: An error has occurred while listing endpoints.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.common.connectors.api_get_all_endpoint")
    @patch("moonshot.integrations.cli.common.connectors._display_endpoints")
    def test_list_endpoints(
        self,
        mock_display_endpoints,
        mock_api_get_all_endpoint,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_endpoint.side_effect = Exception(
                "An error has occurred while listing endpoints."
            )
        else:
            mock_api_get_all_endpoint.return_value = api_response

        args = Namespace(find=find, pagination=pagination)

        result = list_endpoints(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if api_response and not expected_log:
            mock_display_endpoints.assert_called_once_with(api_response)
        else:
            mock_display_endpoints.assert_not_called()

    # ------------------------------------------------------------------------------
    # List Endpoint with mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, filtered_response, expected_output, expected_log",
        [
            (
                None,
                None,
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                "",
            ),
            (
                "Endpoint",
                None,
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                "",
            ),
            (
                None,
                "(0, 1)",
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                        "idx": 1,
                    }
                ],
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                        "idx": 1,
                    }
                ],
                "",
            ),
            # Case where filtered_response is None
            (
                None,
                None,
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                None,
                None,
                "There are no endpoints found.",
            ),
            # Case where filtered_response is an empty list
            (
                None,
                None,
                [
                    {
                        "id": 1,
                        "name": "endpoint1",
                        "connector_type": "openai-gpt4",
                        "uri": "test_uri",
                        "token": "test_token",
                        "max_calls_per_second": 1,
                        "max_concurrency": 1,
                        "model": "gpt-3.5-turbo-1106",
                        "params": {"temperature": 0.5},
                    }
                ],
                [],
                None,
                "There are no endpoints found.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.common.connectors.api_get_all_endpoint")
    @patch("moonshot.integrations.cli.common.connectors._display_endpoints")
    @patch("moonshot.integrations.cli.common.connectors.filter_data")
    def test_list_endpoints_filtered(
        self,
        mock_filter_data,
        mock_display_endpoints,
        mock_api_get_all_endpoints,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        capsys,
    ):
        mock_api_get_all_endpoints.return_value = api_response
        mock_filter_data.return_value = filtered_response

        args = Namespace(find=find, pagination=pagination)

        result = list_endpoints(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if filtered_response and not expected_log:
            mock_display_endpoints.assert_called_once_with(filtered_response)
        else:
            mock_display_endpoints.assert_not_called()

    # ------------------------------------------------------------------------------
    # View Endpoint
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "endpoint, api_response, expected_log",
        [
            # Valid case
            (
                "1",
                {
                    "id": 1,
                    "name": "endpoint1",
                    "connector_type": "openai-gpt4",
                    "uri": "test_uri",
                    "token": "test_token",
                    "max_calls_per_second": 1,
                    "max_concurrency": 1,
                    "model": "gpt-3.5-turbo-1106",
                    "params": {"temperature": 0.5},
                },
                "",
            ),
            # Invalid case: endpoint_id is None
            (
                None,
                None,
                "[view_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
            ),
            # Invalid case: endpoint_id is not a string
            (
                "",
                None,
                "[view_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
            ),
            (
                123,
                None,
                "[view_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
            ),
            (
                {},
                None,
                "[view_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
            ),
            (
                [],
                None,
                "[view_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
            ),
            (
                (),
                None,
                "[view_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
            ),
            (
                True,
                None,
                "[view_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
            ),
            # Exception case: api_read_endpoint raises an exception
            (
                "1",
                None,
                "[view_endpoint]: An error has occurred while reading the endpoint.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.common.connectors.api_read_endpoint")
    @patch("moonshot.integrations.cli.common.connectors._display_endpoints")
    def test_view_endpoints(
        self,
        mock_display_view_endpoint,
        mock_api_read_endpoint,
        endpoint,
        api_response,
        expected_log,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_read_endpoint.side_effect = Exception(
                "An error has occurred while reading the endpoint."
            )
        else:
            mock_api_read_endpoint.return_value = api_response

        args = Namespace(endpoint=endpoint)

        view_endpoint(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if api_response and not expected_log:
            mock_display_view_endpoint.assert_called_once_with([api_response])
        else:
            mock_display_view_endpoint.assert_not_called()

    # ------------------------------------------------------------------------------
    # Update Endpoint
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "endpoint, update_kwargs, expected_log, to_be_called",
        [
            # Valid case - Full update
            (
                "Endpoint 1",
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: Endpoint updated.",
                True,
            ),
            # Invalid case - endpoint
            (
                "",
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case - update values
            (
                "Endpoint 1",
                "['', '']",
                "[update_endpoint]: The 'update_kwargs' argument must evaluate to a list of tuples.",
                False,
            ),
            (
                "Endpoint 1",
                "[[], ()]",
                "[update_endpoint]: The 'update_kwargs' argument must evaluate to a list of tuples.",
                False,
            ),
            (
                "Endpoint 1",
                "",
                "[update_endpoint]: The 'update_kwargs' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Endpoint 1",
                None,
                "[update_endpoint]: The 'update_kwargs' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Endpoint 1",
                123,
                "[update_endpoint]: The 'update_kwargs' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Endpoint 1",
                {},
                "[update_endpoint]: The 'update_kwargs' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Endpoint 1",
                [],
                "[update_endpoint]: The 'update_kwargs' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Endpoint 1",
                (),
                "[update_endpoint]: The 'update_kwargs' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Endpoint 1",
                True,
                "[update_endpoint]: The 'update_kwargs' argument must be a non-empty string and not None.",
                False,
            ),
            # Test case: API update raises an exception
            (
                "Endpoint 1",
                "[('name', 'Updated Endpoint'), ('uri', 'Updated URI'), ('token', 'Update token'), ('max_calls_per_second', 1), ('max_concurrency', 1), ('model', 'gpt-4o'), ('params', {'hello': 'world'})]",  # noqa: E501
                "[update_endpoint]: An error has occurred while updating the endpoint.",
                True,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.common.connectors.api_update_endpoint")
    def test_update_endpoint(
        self,
        mock_api_update_endpoint,
        capsys,
        endpoint,
        update_kwargs,
        expected_log,
        to_be_called,
    ):
        if "error" in expected_log:
            mock_api_update_endpoint.side_effect = Exception(
                "An error has occurred while updating the endpoint."
            )
        else:
            mock_api_update_endpoint.return_value = "updated"

        args = Namespace(endpoint=endpoint, update_kwargs=update_kwargs)

        update_endpoint(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_update_endpoint.assert_called_once_with(
                args.endpoint, **dict(literal_eval(args.update_kwargs))
            )
        else:
            mock_api_update_endpoint.assert_not_called()

    # ------------------------------------------------------------------------------
    # Delete Endpoint
    # ------------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "endpoint, expected_log, to_be_called",
        [
            # Valid case
            ("Endpoint 1", "[delete_endpoint]: Endpoint deleted.", True),
            # Invalid case - endpoint
            (
                "",
                "[delete_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[delete_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[delete_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[delete_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[delete_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[delete_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[delete_endpoint]: The 'endpoint' argument must be a non-empty string and not None.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.common.connectors.api_delete_endpoint")
    def test_delete_endpoint(
        self, mock_api_delete_endpoint, capsys, endpoint, expected_log, to_be_called
    ):
        args = Namespace(endpoint=endpoint)

        with patch(
            "moonshot.integrations.cli.common.connectors.console.input",
            return_value="y",
        ):
            with patch(
                "moonshot.integrations.cli.common.connectors.console.print"
            ) as _:
                delete_endpoint(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_endpoint.assert_called_once_with(args.endpoint)
        else:
            mock_api_delete_endpoint.assert_not_called()

    @patch(
        "moonshot.integrations.cli.common.connectors.console.input", return_value="y"
    )
    @patch("moonshot.integrations.cli.common.connectors.api_delete_endpoint")
    def test_delete_endpoint_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.endpoint = "test_endpoint_id"

        delete_endpoint(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the endpoint (y/N)? [/]"
        )
        mock_delete.assert_called_once_with("test_endpoint_id")

    @patch(
        "moonshot.integrations.cli.common.connectors.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.common.connectors.api_delete_endpoint")
    def test_delete_endpoint_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.endpoint = "test_endpoint_id"

        delete_endpoint(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the endpoint (y/N)? [/]"
        )
        mock_delete.assert_not_called()

    @patch(
        "moonshot.integrations.cli.common.connectors.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.common.connectors.console.print")
    @patch("moonshot.integrations.cli.common.connectors.api_delete_endpoint")
    def test_delete_endpoint_cancelled_output(
        self, mock_delete, mock_print, mock_input
    ):
        args = MagicMock()
        args.endpoint = "test_endpoint_id"

        delete_endpoint(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the endpoint (y/N)? [/]"
        )
        mock_print.assert_called_once_with(
            "[bold yellow]Endpoint deletion cancelled.[/]"
        )
        mock_delete.assert_not_called()

    # ------------------------------------------------------------------------------
    # List Connector Types with non-mocked filter-data
    # ------------------------------------------------------------------------------

    @pytest.mark.parametrize(
        "find, pagination, api_response, expected_output, expected_log",
        [
            # Valid cases with no filter
            (
                None,
                None,
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                "",
            ),
            # No connector types
            (
                None,
                None,
                [],
                None,
                "There are no connector types found.",
            ),
            # Valid case with find
            (
                "connector",
                None,
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                "",
            ),
            # Valid case with find but no results
            (
                "nothingvalid",
                None,
                [],
                None,
                "There are no connector types found.",
            ),
            # Valid case with pagination
            (
                None,
                "(1, 1)",
                [
                    "connector-type-1",
                ],
                [
                    "connector-type-1",
                ],
                "",
            ),
            # Valid case with pagination but no results
            (
                "Endpoint",
                "(1, 1)",
                [],
                None,
                "There are no connector types found.",
            ),
            # Invalid cases for find
            (
                "",
                None,
                None,
                None,
                "[list_connector_types]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                99,
                None,
                None,
                None,
                "[list_connector_types]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                {},
                None,
                None,
                None,
                "[list_connector_types]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                [],
                None,
                None,
                None,
                "[list_connector_types]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                (),
                None,
                None,
                None,
                "[list_connector_types]: The 'find' argument must be a non-empty string and not None.",
            ),
            (
                True,
                None,
                None,
                None,
                "[list_connector_types]: The 'find' argument must be a non-empty string and not None.",
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                99,
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                {},
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                [],
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                (),
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                True,
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                True,
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a non-empty string and not None.",
            ),
            (
                None,
                "(1, 'a')",
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(1, 2, 3)",
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(1, )",
                None,
                None,
                "[list_connector_types]: The 'pagination' argument must be a tuple of two integers.",
            ),
            (
                None,
                "(0, 1)",
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                None,
                "[list_connector_types]: Invalid page number or page size. Page number and page size should start from 1.",  # noqa: E501
            ),
            (
                None,
                "(1, 0)",
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                None,
                "[list_connector_types]: Invalid page number or page size. Page number and page size should start from 1.",  # noqa: E501
            ),
            (
                None,
                "(0, 0)",
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                None,
                "[list_connector_types]: Invalid page number or page size. Page number and page size should start from 1.",  # noqa: E501
            ),
            (
                None,
                "(1, -1)",
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                None,
                "[list_connector_types]: Invalid page number or page size. Page number and page size should start from 1.",  # noqa: E501
            ),
            (
                None,
                "(-1, 1)",
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                None,
                "[list_connector_types]: Invalid page number or page size. Page number and page size should start from 1.",  # noqa: E501
            ),
            (
                None,
                "(-1, -1)",
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                None,
                "[list_connector_types]: Invalid page number or page size. Page number and page size should start from 1.",  # noqa: E501
            ),
            # Exception case
            (
                None,
                None,
                None,
                None,
                "[list_connector_types]: An error has occurred while listing connector types.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.common.connectors.api_get_all_connector_type")
    @patch("moonshot.integrations.cli.common.connectors._display_connector_types")
    def test_list_connector_type(
        self,
        mock_display_connector_types,
        mock_api_get_all_connector_type,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_connector_type.side_effect = Exception(
                "An error has occurred while listing connector types."
            )
        else:
            mock_api_get_all_connector_type.return_value = api_response

        args = Namespace(find=find, pagination=pagination)

        result = list_connector_types(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if api_response and not expected_log:
            mock_display_connector_types.assert_called_once_with(api_response)
        else:
            mock_display_connector_types.assert_not_called()

    # ------------------------------------------------------------------------------
    # List Endpoint with mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, filtered_response, expected_output, expected_log",
        [
            (
                None,
                None,
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                "",
            ),
            (
                "connector",
                None,
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                "",
            ),
            (
                None,
                "(2, 1)",
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                [
                    "connector-type-2",
                ],
                [
                    "connector-type-2",
                ],
                "",
            ),
            (
                None,
                "(1, 4)",
                [
                    "connector-type-1",
                    "connector-type-2",
                    "connector-type-3",
                    "connector-type-4",
                ],
                [
                    "connector-type-1",
                    "connector-type-2",
                    "connector-type-3",
                    "connector-type-4",
                ],
                [
                    "connector-type-1",
                    "connector-type-2",
                    "connector-type-3",
                    "connector-type-4",
                ],
                "",
            ),
            (
                None,
                "(2, 2)",
                [
                    "connector-type-1",
                    "connector-type-2",
                    "connector-type-3",
                    "connector-type-4",
                ],
                [
                    "connector-type-3",
                    "connector-type-4",
                ],
                [
                    "connector-type-3",
                    "connector-type-4",
                ],
                "",
            ),
            # Case where filtered_response is None
            (
                None,
                None,
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                None,
                None,
                "There are no connector types found.",
            ),
            # Case where filtered_response is an empty list
            (
                None,
                None,
                [
                    "connector-type-1",
                    "connector-type-2",
                ],
                [],
                None,
                "There are no connector types found.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.common.connectors.api_get_all_connector_type")
    @patch("moonshot.integrations.cli.common.connectors._display_connector_types")
    @patch("moonshot.integrations.cli.common.connectors.filter_data")
    def test_list_connector_types_filtered(
        self,
        mock_filter_data,
        mock_display_connector_types,
        mock_api_get_all_connector_type,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        capsys,
    ):
        mock_api_get_all_connector_type.return_value = api_response
        mock_filter_data.return_value = filtered_response

        args = Namespace(find=find, pagination=pagination)

        result = list_connector_types(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if filtered_response and not expected_log:
            mock_display_connector_types.assert_called_once_with(filtered_response)
        else:
            mock_display_connector_types.assert_not_called()
