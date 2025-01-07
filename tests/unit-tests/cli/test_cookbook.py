from ast import literal_eval
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from moonshot.integrations.cli.benchmark.cookbook import (
    add_cookbook,
    delete_cookbook,
    list_cookbooks,
    run_cookbook,
    update_cookbook,
    view_cookbook,
)


class TestCollectionCliCookbook:
    api_response = [
        {
            "id": 1,
            "name": "Cookbook 1",
            "description": "Desc 1",
            "recipes": ["recipe1"],
            "tags": ['test-tag'],
            "categories": ['test-cat']
        }
    ]
    api_response_pagination = [
        {
            "id": 1,
            "name": "Cookbook 1",
            "description": "Desc 1",
            "recipes": ["recipe1"],
            "tags": ['test-tag'],
            "categories": ['test-cat'],
            "idx": 1,
        }
    ]

    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Test add_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "name, description, recipes, categories, tags, expected_output",
        [
            # Valid case
            (
                "Test Cookbook",
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",
                "[add_cookbook]: Cookbook (new_cookbook_id) created.",
            ),
            (
                "Another Cookbook",
                "Another description.",
                "['recipe3']",
                "['test_category']",
                "['test_tag']",  
                "[add_cookbook]: Cookbook (new_cookbook_id) created.",
            ),
            # Invalid case for name
            (
                None,
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",
                "[add_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                "",
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                99,
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                {},
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                [],
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                (),
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                True,
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            # Invalid case for description
            (
                "Test Cookbook",
                None,
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'description' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                "",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'description' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                99,
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'description' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                {},
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'description' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                [],
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'description' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                (),
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'description' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                True,
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'description' argument must be a non-empty string and not None.",
            ),
            # Invalid case for recipes - not a list of strings
            (
                "Test Cookbook",
                "This is a test cookbook.",
                "None",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a list of strings after evaluation.",
            ),
            (
                "Test Cookbook",
                "This is a test cookbook.",
                "[123, 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a list of strings after evaluation.",
            ),
            # Invalid case for recipes
            (
                "Test Cookbook",
                "This is a test cookbook.",
                None,
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                "This is a test cookbook.",
                "",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                "This is a test cookbook.",
                99,
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                "This is a test cookbook.",
                {},
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                "This is a test cookbook.",
                [],
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                "This is a test cookbook.",
                (),
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a non-empty string and not None.",
            ),
            (
                "Test Cookbook",
                "This is a test cookbook.",
                True,
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: The 'recipes' argument must be a non-empty string and not None.",
            ),
            # Exception case
            (
                "Test Cookbook",
                "This is a test cookbook.",
                "['recipe1', 'recipe2']",
                "['test_category']",
                "['test_tag']",                
                "[add_cookbook]: An error has occurred while creating cookbook.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_create_cookbook")
    def test_add_cookbook(
        self,
        mock_api_create_cookbook,
        name,
        description,
        recipes,
        categories,
        tags,
        expected_output,
        capsys,
    ):
        if "error" in expected_output:
            mock_api_create_cookbook.side_effect = Exception(
                "An error has occurred while creating cookbook."
            )
        else:
            mock_api_create_cookbook.return_value = "new_cookbook_id"

        class Args:
            pass

        args = Args()
        args.name = name
        args.description = description
        args.recipes = recipes
        args.categories = categories
        args.tags = tags

        add_cookbook(args)

        captured = capsys.readouterr()
        assert expected_output == captured.out.strip()

        if (
            isinstance(name, str)
            and name
            and isinstance(description, str)
            and description
            and isinstance(recipes, str)
            and recipes
        ):
            try:
                recipes_list = literal_eval(recipes)
                if not (
                    isinstance(recipes_list, list)
                    and all(isinstance(recipe, str) for recipe in recipes_list)
                ):
                    raise ValueError(
                        "The 'recipes' argument must be a list of strings after evaluation."
                    )
            except Exception:
                recipes_list = None
            if recipes_list is not None:
                mock_api_create_cookbook.assert_called_once_with(
                    name, description, recipes_list
                )
            else:
                mock_api_create_cookbook.assert_not_called()
        else:
            mock_api_create_cookbook.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test list_cookbooks functionality with non-mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, expected_output, expected_log, to_be_called",
        [
            # Valid cases
            (
                None,
                None,
                api_response,
                api_response,
                "",
                True,
            ),
            # No cookbooks
            (None, None, [], None, "There are no cookbooks found.", False),
            (
                "Cookbook",
                None,
                api_response,
                api_response,
                "",
                True,
            ),
            (
                None,
                "(1, 1)",
                api_response,
                api_response_pagination,
                "",
                True,
            ),
            ("Cookbook", "(1, 1)", [], None, "There are no cookbooks found.", False),
            # Invalid cases for find
            (
                "",
                None,
                api_response,
                None,
                "[list_cookbooks]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                99,
                None,
                api_response,
                None,
                "[list_cookbooks]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                None,
                api_response,
                None,
                "[list_cookbooks]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                None,
                api_response,
                None,
                "[list_cookbooks]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                None,
                api_response,
                None,
                "[list_cookbooks]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                None,
                api_response,
                None,
                "[list_cookbooks]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                99,
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                {},
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                [],
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                (),
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "(1, 'a')",
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, 2, 3)",
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, )",
                api_response,
                None,
                "[list_cookbooks]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                None,
                "[list_cookbooks]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, 0)",
                api_response,
                None,
                "[list_cookbooks]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(0, 0)",
                api_response,
                None,
                "[list_cookbooks]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, -1)",
                api_response,
                None,
                "[list_cookbooks]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, 1)",
                api_response,
                None,
                "[list_cookbooks]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, -1)",
                api_response,
                None,
                "[list_cookbooks]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            # Exception case
            (
                None,
                None,
                api_response,
                None,
                "[list_cookbooks]: An error has occurred while listing cookbooks.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_get_all_cookbook")
    @patch("moonshot.integrations.cli.benchmark.cookbook._display_cookbooks")
    def test_list_cookbooks(
        self,
        mock_display_cookbooks,
        mock_api_get_all_cookbook,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_cookbook.side_effect = Exception(
                "An error has occurred while listing cookbooks."
            )
        else:
            mock_api_get_all_cookbook.return_value = api_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_cookbooks(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_cookbooks.assert_called_once_with(api_response)
        else:
            mock_display_cookbooks.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test list_cookbooks functionality with mocked filter-data
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "find, pagination, api_response, filtered_response, expected_output, expected_log, to_be_called",
        [
            (
                None,
                None,
                api_response,
                api_response_pagination,
                api_response_pagination,
                "",
                True,
            ),
            (
                "Cookbook",
                None,
                api_response,
                api_response_pagination,
                api_response_pagination,
                "",
                True,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                api_response_pagination,
                api_response_pagination,
                "",
                True,
            ),
            # Case where filtered_response is None
            (
                None,
                None,
                api_response,
                None,
                None,
                "There are no cookbooks found.",
                False,
            ),
            # Case where filtered_response is an empty list
            (
                None,
                None,
                api_response,
                [],
                None,
                "There are no cookbooks found.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_get_all_cookbook")
    @patch("moonshot.integrations.cli.benchmark.cookbook._display_cookbooks")
    @patch("moonshot.integrations.cli.benchmark.cookbook.filter_data")
    def test_list_cookbooks_filtered(
        self,
        mock_filter_data,
        mock_display_cookbooks,
        mock_api_get_all_cookbook,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        mock_api_get_all_cookbook.return_value = api_response
        mock_filter_data.return_value = filtered_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_cookbooks(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_cookbooks.assert_called_once_with(filtered_response)
        else:
            mock_display_cookbooks.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test view_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cookbook_id, api_response, expected_log, to_be_called",
        [
            # Valid case
            (
                "1",
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                    "categories": "['test_category']",
                    "tags": "['test_tag']",                                    
                },
                "",
                True,
            ),
            # Invalid case: cookbook_id is None
            (
                None,
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                    "categories": "['test_category']",
                    "tags": "['test_tag']",                         
                },
                "[view_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case: cookbook_id is not a string
            (
                "",
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                    "categories": "['test_category']",
                    "tags": "['test_tag']",                         
                },
                "[view_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                },
                "[view_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                },
                "[view_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                },
                "[view_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                },
                "[view_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                },
                "[view_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            # Exception case: api_read_cookbook raises an exception
            (
                "1",
                {
                    "id": 1,
                    "name": "Cookbook 1",
                    "description": "Desc 1",
                    "recipes": ["recipe1"],
                },
                "[view_cookbook]: An error has occurred while reading the cookbook.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_read_cookbook")
    @patch("moonshot.integrations.cli.benchmark.cookbook._display_view_cookbook")
    def test_view_cookbook(
        self,
        mock_display_view_cookbook,
        mock_api_read_cookbook,
        cookbook_id,
        api_response,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_read_cookbook.side_effect = Exception(
                "An error has occurred while reading the cookbook."
            )
        else:
            mock_api_read_cookbook.return_value = api_response

        class Args:
            pass

        args = Args()
        args.cookbook = cookbook_id

        view_cookbook(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_display_view_cookbook.assert_called_once_with(api_response)
        else:
            mock_display_view_cookbook.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test run_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "name, cookbooks, endpoints, prompt_selection_percentage, random_seed, system_prompt, \
        runner_proc_module, result_proc_module, expected_log",
        [
            # Valid case
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "",
                "runner_module",
                "result_module",
                "",
            ),
            # Invalid case: name
            (
                "",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                None,
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                123,
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                {},
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                [],
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                (),
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                True,
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'name' argument must be a non-empty string and not None.",
            ),
            # Invalid case: cookbooks is not a list of string
            (
                "Test Runner",
                "[123, 123]",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'cookbooks' argument must evaluate to a list of strings.",
            ),
            # Invalid case: cookbooks is not a string
            (
                "Test Runner",
                None,
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'cookbooks' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'cookbooks' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                123,
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'cookbooks' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                {},
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'cookbooks' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                [],
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'cookbooks' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                (),
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'cookbooks' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                True,
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'cookbooks' argument must be a non-empty string and not None.",
            ),
            # Invalid case: endpoints is not a list of string
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "[123, 123]",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'endpoints' argument must evaluate to a list of strings.",
            ),
            # Invalid case: endpoints is not a string
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                None,
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                123,
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                {},
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                [],
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                (),
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                True,
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            # Invalid case: prompt_selection_percentage is 0
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                0,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be between 1 - 100.",
            ),
            # Invalid case: prompt_selection_percentage is -1
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                -1,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be between 1 - 100.",
            ),
            # Invalid case: prompt_selection_percentage is 101
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                101,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be between 1 - 100.",
            ),
            # Invalid case: prompt_selection_percentage is not an integer
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                None,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                "",
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                {},
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                [],
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                (),
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                True,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            # Invalid case: random_seed is not an integer
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                None,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                "",
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                {},
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                [],
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                (),
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                True,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'random_seed' argument must be an integer.",
            ),
            # Invalid case: system_prompt is None
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                None,
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                {},
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                [],
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                (),
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                True,
                "runner_module",
                "result_module",
                "[run_cookbook]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            # Invalid case: runner_proc_module is None
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                None,
                "result_module",
                "[run_cookbook]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "",
                "result_module",
                "[run_cookbook]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                {},
                "result_module",
                "[run_cookbook]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                [],
                "result_module",
                "[run_cookbook]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                (),
                "result_module",
                "[run_cookbook]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                True,
                "result_module",
                "[run_cookbook]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            # Invalid case: result_proc_module is None
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                None,
                "[run_cookbook]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "",
                "[run_cookbook]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                {},
                "[run_cookbook]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                [],
                "[run_cookbook]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                (),
                "[run_cookbook]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                True,
                "[run_cookbook]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            # Exception case: api_create_runner raises an exception
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: An error has occurred while creating the runner.",
            ),
            # Exception case: api_load_runner raises an exception
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: An error has occurred while loading the runner.",
            ),
            # Exception case: api_get_all_runner_name raises an exception
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: An error has occurred while getting all runner names.",
            ),
            # Exception case: api_get_all_run raises an exception
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: An error has occurred while getting all runs.",
            ),
            # Exception case: no results raises an exception
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: There are no results generated.",
            ),
            # Exception case: show_cookbook_results raises an exception
            (
                "Test Runner",
                "['cookbook1', 'cookbook2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_cookbook]: An error has occurred while showing cookbook results.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_get_all_runner_name")
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_load_runner")
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_create_runner")
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_get_all_run")
    @patch("moonshot.integrations.cli.benchmark.cookbook._show_cookbook_results")
    def test_run_cookbook(
        self,
        mock_show_cookbook_results,
        mock_api_get_all_run,
        mock_api_create_runner,
        mock_api_load_runner,
        mock_api_get_all_runner_name,
        name,
        cookbooks,
        endpoints,
        prompt_selection_percentage,
        random_seed,
        system_prompt,
        runner_proc_module,
        result_proc_module,
        expected_log,
        capsys,
    ):
        to_trigger_called = False

        if "getting all runner names" in expected_log:
            mock_api_get_all_runner_name.side_effect = Exception(
                "An error has occurred while getting all runner names."
            )

        elif "creating the runner" in expected_log:
            mock_api_get_all_runner_name.return_value = []
            mock_api_create_runner.side_effect = Exception(
                "An error has occurred while creating the runner."
            )

        elif "loading the runner" in expected_log:
            mock_api_get_all_runner_name.return_value = ["test-runner"]
            mock_api_load_runner.side_effect = Exception(
                "An error has occurred while loading the runner."
            )

        elif "getting all runs" in expected_log:
            mock_api_get_all_runner_name.return_value = []
            mock_api_create_runner.return_value = AsyncMock()
            mock_api_get_all_run.side_effect = Exception(
                "An error has occurred while getting all runs."
            )

        elif "showing cookbook results" in expected_log:
            to_trigger_called = True
            mock_api_get_all_runner_name.return_value = []
            mock_api_create_runner.return_value = AsyncMock()
            mock_api_get_all_run.return_value = [
                {"results": {"metadata": {"duration": 10}}}
            ]
            mock_show_cookbook_results.side_effect = Exception(
                "An error has occurred while showing cookbook results."
            )

        elif "no results" in expected_log:
            mock_api_get_all_runner_name.return_value = []
            mock_api_create_runner.return_value = AsyncMock()
            mock_api_get_all_run.return_value = [
                {"someresults": {"metadata": {"duration": 10}}}
            ]

        else:
            mock_api_create_runner.return_value = AsyncMock()
            mock_api_load_runner.return_value = AsyncMock()
            mock_api_get_all_runner_name.return_value = []
            mock_api_get_all_run.return_value = [
                {"results": {"metadata": {"duration": 10}}}
            ]

        class Args:
            pass

        args = Args()
        args.name = name
        args.cookbooks = cookbooks
        args.endpoints = endpoints
        args.prompt_selection_percentage = prompt_selection_percentage
        args.random_seed = random_seed
        args.system_prompt = system_prompt
        args.runner_proc_module = runner_proc_module
        args.result_proc_module = result_proc_module

        run_cookbook(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if not expected_log or to_trigger_called:
            mock_show_cookbook_results.assert_called_once()
        else:
            mock_show_cookbook_results.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test update_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cookbook, update_values, expected_log, to_be_called",
        [
            # Valid case
            (
                "Cookbook 1",
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: Cookbook updated.",
                True,
            ),
            # Invalid case - cookbook
            (
                "",
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case - update values
            (
                "Cookbook 1",
                "",
                "[update_cookbook]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Cookbook 1",
                "['', '']",
                "[update_cookbook]: The 'update_values' argument must evaluate to a list of tuples.",
                False,
            ),
            (
                "Cookbook 1",
                "[[], ()]",
                "[update_cookbook]: The 'update_values' argument must evaluate to a list of tuples.",
                False,
            ),
            (
                "Cookbook 1",
                None,
                "[update_cookbook]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Cookbook 1",
                123,
                "[update_cookbook]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Cookbook 1",
                {},
                "[update_cookbook]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Cookbook 1",
                [],
                "[update_cookbook]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Cookbook 1",
                (),
                "[update_cookbook]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Cookbook 1",
                True,
                "[update_cookbook]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            # Test case: API update raises an exception
            (
                "Cookbook 1",
                "[('name', 'Updated Cookbook'), ('description', 'Updated description')]",
                "[update_cookbook]: An error has occurred while updating the cookbook.",
                True,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_update_cookbook")
    def test_update_cookbook(
        self,
        mock_api_update_cookbook,
        capsys,
        cookbook,
        update_values,
        expected_log,
        to_be_called,
    ):
        if "error" in expected_log:
            mock_api_update_cookbook.side_effect = Exception(
                "An error has occurred while updating the cookbook."
            )
        else:
            mock_api_update_cookbook.return_value = "updated"

        class Args:
            pass

        args = Args()
        args.cookbook = cookbook
        args.update_values = update_values

        update_cookbook(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_update_cookbook.assert_called_once_with(
                args.cookbook, **dict(literal_eval(args.update_values))
            )
        else:
            mock_api_update_cookbook.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test delete_cookbook functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "cookbook, expected_log, to_be_called",
        [
            # Valid case
            ("Cookbook 1", "[delete_cookbook]: Cookbook deleted.", True),
            # Invalid case - cookbook
            (
                "",
                "[delete_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[delete_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[delete_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[delete_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[delete_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[delete_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[delete_cookbook]: The 'cookbook' argument must be a non-empty string and not None.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_delete_cookbook")
    def test_delete_cookbook(
        self, mock_api_delete_cookbook, capsys, cookbook, expected_log, to_be_called
    ):
        class Args:
            pass

        args = Args()
        args.cookbook = cookbook

        with patch(
            "moonshot.integrations.cli.benchmark.cookbook.console.input",
            return_value="y",
        ):
            with patch("moonshot.integrations.cli.benchmark.cookbook.console.print"):
                delete_cookbook(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_cookbook.assert_called_once_with(args.cookbook)
        else:
            mock_api_delete_cookbook.assert_not_called()

    @patch(
        "moonshot.integrations.cli.benchmark.cookbook.console.input", return_value="y"
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_delete_cookbook")
    def test_delete_cookbook_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.cookbook = "test_cookbook_id"

        delete_cookbook(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the cookbook (y/N)? [/]"
        )
        mock_delete.assert_called_once_with("test_cookbook_id")

    @patch(
        "moonshot.integrations.cli.benchmark.cookbook.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_delete_cookbook")
    def test_delete_cookbook_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.cookbook = "test_cookbook_id"

        delete_cookbook(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the cookbook (y/N)? [/]"
        )
        mock_delete.assert_not_called()

    @patch(
        "moonshot.integrations.cli.benchmark.cookbook.console.input", return_value="n"
    )
    @patch("moonshot.integrations.cli.benchmark.cookbook.console.print")
    @patch("moonshot.integrations.cli.benchmark.cookbook.api_delete_cookbook")
    def test_delete_cookbook_cancelled_output(
        self, mock_delete, mock_print, mock_input
    ):
        args = MagicMock()
        args.cookbook = "test_cookbook_id"

        delete_cookbook(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the cookbook (y/N)? [/]"
        )
        mock_print.assert_called_once_with(
            "[bold yellow]Cookbook deletion cancelled.[/]"
        )
        mock_delete.assert_not_called()
