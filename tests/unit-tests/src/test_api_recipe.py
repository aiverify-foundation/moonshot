import os
import shutil

import pytest
from pydantic import ValidationError

from moonshot.api import (
    api_create_recipe,
    api_delete_recipe,
    api_get_all_recipe,
    api_get_all_recipe_name,
    api_read_recipe,
    api_read_recipes,
    api_set_environment_variables,
    api_update_recipe,
)


class TestCollectionApiRecipe:
    @pytest.fixture(autouse=True)
    def init(self):
        # Set environment variables for recipe paths
        api_set_environment_variables(
            {
                "METRICS": "tests/unit-tests/src/data/metrics/",
                "PROMPT_TEMPLATES": "tests/unit-tests/src/data/prompt-templates/",
                "RECIPES": "tests/unit-tests/src/data/recipes/",
                "DATASETS": "tests/unit-tests/src/data/datasets/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )

        # Copy sample recipe and dataset files for testing
        shutil.copyfile(
            "tests/unit-tests/common/samples/arc.json",
            "tests/unit-tests/src/data/recipes/arc.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/arc-easy.json",
            "tests/unit-tests/src/data/datasets/arc-easy.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/mcq-template.json",
            "tests/unit-tests/src/data/prompt-templates/mcq-template.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/analogical-similarity.json",
            "tests/unit-tests/src/data/prompt-templates/analogical-similarity.json",
        )
        shutil.copyfile(
            "tests/unit-tests/common/samples/exactstrmatch.py",
            "tests/unit-tests/src/data/metrics/exactstrmatch.py",
        )

        # Setup complete, proceed with tests
        yield

        # Cleanup: Remove test recipe files
        recipe_paths = [
            "tests/unit-tests/src/data/recipes/arc.json",
            "tests/unit-tests/src/data/datasets/arc.json",
            "tests/unit-tests/src/data/datasets/arc-easy.json",
            "tests/unit-tests/src/data/datasets/cache.json",
            "tests/unit-tests/src/data/recipes/my-new-rec-ipe-1-23.json",
            "tests/unit-tests/src/data/recipes/my-new-recipe-1.json",
            "tests/unit-tests/src/data/recipes/my-new-recipe.json",
            "tests/unit-tests/src/data/recipes/none.json",
            "tests/unit-tests/src/data/prompt-templates/mcq-template.json",
            "tests/unit-tests/src/data/prompt-templates/analogical-similarity.json",
            "tests/unit-tests/src/data/metrics/exactstrmatch.py",
        ]
        for recipe_path in recipe_paths:
            if os.path.exists(recipe_path):
                os.remove(recipe_path)

    # ------------------------------------------------------------------------------
    # Test api_create_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "input_args, expected_dict",
        [
            # Valid case
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {"expected_output": True, "expected_id": "my-new-recipe"},
            ),
            (
                {
                    "name": "my new recipe 1",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {"expected_output": True, "expected_id": "my-new-recipe-1"},
            ),
            (
                {
                    "name": "my_new-rec ipe 1@.!23",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {"expected_output": True, "expected_id": "my-new-rec-ipe-1-23"},
            ),
            (
                {
                    "name": "None",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": True,
                    "expected_id": "none",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {"expected_output": True, "expected_id": "my-new-recipe"},
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": [],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {"expected_output": True, "expected_id": "my-new-recipe"},
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {"expected_output": True, "expected_id": "my-new-recipe"},
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {"expected_output": True, "expected_id": "my-new-recipe"},
            ),
            # Invalid cases for name
            (
                {
                    "name": "",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "",
                    "expected_error_message": "String should have at least 1 character",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": None,
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": [],
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": {},
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": 123,
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for description
            (
                {
                    "name": "my-new-recipe",
                    "description": None,
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": [],
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": {},
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": 123,
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for tags
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": "",
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": None,
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food", 123],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for categories
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": "",
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": None,
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness", 123],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for datasets
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": {},
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": None,
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy", 123],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": [],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "List should have at least 1 item after validation, not 0",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for prompt_templates
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": {},
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": None,
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity", 123],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for metrics
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": {},
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": None,
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch", 123],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": [],
                    "grading_scale": {},
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "List should have at least 1 item after validation, not 0",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases for grading_scale
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": None,
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": "None",
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": [],
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": "",
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {
                    "name": "my-new-recipe",
                    "description": "My new Recipe!",
                    "tags": ["food"],
                    "categories": ["fairness"],
                    "datasets": ["arc-easy"],
                    "prompt_templates": ["analogical-similarity"],
                    "metrics": ["exactstrmatch"],
                    "grading_scale": "None",
                },
                {
                    "expected_output": False,
                    "expected_id": "my-new-recipe",
                    "expected_error_message": "Input should be a valid dictionary",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_create_recipe(self, input_args, expected_dict):
        """
        Test the api_create_recipe function with various input arguments and expected outcomes.

        This test uses parametrized input arguments and expected dictionaries to validate both successful
        recipe creation and proper handling of invalid inputs through exceptions.

        Args:
            input_args (dict): A dictionary containing the input parameters to the api_create_recipe function.
            expected_dict (dict): A dictionary containing the expected result of the test case. This includes
                                  the expected output, expected ID, expected error message, and expected exception.

        The test cases include:
        - Valid cases with proper input arguments that should result in successful recipe creation.
        - Invalid cases with improper input arguments that should raise specific exceptions with appropriate error messages.
        """
        if expected_dict["expected_output"]:
            # Test valid cases where recipe creation should succeed.
            assert (
                api_create_recipe(
                    input_args["name"],
                    input_args["description"],
                    input_args["tags"],
                    input_args["categories"],
                    input_args["datasets"],
                    input_args["prompt_templates"],
                    input_args["metrics"],
                    input_args["grading_scale"],
                )
                == expected_dict["expected_id"]
            )
        else:
            # Test invalid cases where recipe creation should fail and raise an exception.
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_create_recipe(
                        input_args["name"],
                        input_args["description"],
                        input_args["tags"],
                        input_args["categories"],
                        input_args["datasets"],
                        input_args["prompt_templates"],
                        input_args["metrics"],
                        input_args["grading_scale"],
                    )
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_create_recipe(
                        input_args["name"],
                        input_args["description"],
                        input_args["tags"],
                        input_args["categories"],
                        input_args["datasets"],
                        input_args["prompt_templates"],
                        input_args["metrics"],
                        input_args["grading_scale"],
                    )
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                # If an unexpected exception is specified, fail the test.
                assert False

    # ------------------------------------------------------------------------------
    # Test api_read_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "recipe_id,expected_dict",
        [
            # Valid case
            (
                "arc",
                {
                    "expected_output": {
                        "id": "arc",
                        "name": "ARC",
                        "description": "To measure model's ability in answering genuine grade-school level, multiple-choice science questions on the easy and challenge sets. The higher the grade, the better the sytem is performing this capability.",
                        "tags": [],
                        "categories": ["Capability"],
                        "datasets": ["arc-easy"],
                        "prompt_templates": ["mcq-template"],
                        "metrics": ["exactstrmatch"],
                        "grading_scale": {
                            "A": [80, 100],
                            "B": [60, 79],
                            "C": [40, 59],
                            "D": [20, 39],
                            "E": [0, 19],
                        },
                        "stats": {
                            "num_of_tags": 0,
                            "num_of_datasets": 1,
                            "num_of_prompt_templates": 1,
                            "num_of_metrics": 1,
                            "num_of_datasets_prompts": {"arc-easy": 1},
                        },
                    }
                },
            ),
            # Invalid cases
            (
                "vanilla-cake",
                {
                    "expected_output": False,
                    "expected_error_message": "No recipes found with ID: vanilla-cake",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "Recipe ID is empty.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "expected_output": False,
                    "expected_error_message": "No recipes found with ID: None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_read_recipe(self, recipe_id: str, expected_dict: dict):
        """
        Test the api_read_recipe function.

        This test function is parameterized to handle multiple test cases for the api_read_recipe function.
        It tests both valid and invalid inputs, checking for the correct output or exception as expected.

        Args:
            recipe_id (str): The recipe ID to read.
            expected_dict (dict): A dictionary containing the expected output or the expected error message and exception.

        Raises:
            AssertionError: If the actual output or exception does not match the expected value.
        """
        if expected_dict["expected_output"]:
            response = api_read_recipe(recipe_id)
            assert response == expected_dict["expected_output"]
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_read_recipe(recipe_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_read_recipe(recipe_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_read_recipes functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "recipe_ids,expected_dict",
        [
            # Valid case
            (
                ["arc"],
                {
                    "expected_output": [
                        {
                            "id": "arc",
                            "name": "ARC",
                            "description": "To measure model's ability in answering genuine grade-school level, multiple-choice science questions on the easy and challenge sets. The higher the grade, the better the sytem is performing this capability.",
                            "tags": [],
                            "categories": ["Capability"],
                            "datasets": ["arc-easy"],
                            "prompt_templates": ["mcq-template"],
                            "metrics": ["exactstrmatch"],
                            "grading_scale": {
                                "A": [80, 100],
                                "B": [60, 79],
                                "C": [40, 59],
                                "D": [20, 39],
                                "E": [0, 19],
                            },
                            "stats": {
                                "num_of_tags": 0,
                                "num_of_datasets": 1,
                                "num_of_prompt_templates": 1,
                                "num_of_metrics": 1,
                                "num_of_datasets_prompts": {"arc-easy": 1},
                            },
                        }
                    ]
                },
            ),
            (
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "List should have at least 1 item after validation, not 0",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid cases
            (
                "vanilla-cake",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid list",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                ["vanilla-cake"],
                {
                    "expected_output": False,
                    "expected_error_message": "No recipes found with ID: vanilla-cake",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [""],
                {
                    "expected_output": False,
                    "expected_error_message": "Recipe ID is empty.",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [None],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                ["None"],
                {
                    "expected_output": False,
                    "expected_error_message": "No recipes found with ID: None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                [{}],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [[]],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [123],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_read_recipes(self, recipe_ids: list[str], expected_dict: dict):
        if expected_dict["expected_output"]:
            response = api_read_recipes(recipe_ids)
            assert response == expected_dict["expected_output"]
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_read_recipes(recipe_ids)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_read_recipes(recipe_ids)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_update_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "recipe_id,recipe_dict,expected_dict",
        [
            # Valid case
            (
                "arc",
                {
                    "name": "Delicious Chocolate Cake",
                },
                {"expected_output": True},
            ),
            # Case: Update with valid key that exists in the recipe
            (
                "arc",
                {
                    "name": "Super Delicious Chocolate Cake",
                },
                {"expected_output": True},
            ),
            # Case: Update with multiple valid keys
            (
                "arc",
                {
                    "name": "Super Delicious Chocolate Cake",
                    "description": "medium",
                    "tags": ["medium"],
                },
                {"expected_output": True},
            ),
            (
                "arc",
                {
                    "nonexistent_key": "value",
                    "name": "Numeric ID Cake",
                },
                {"expected_output": True},
            ),
            # Invalid cases
            (
                "vanilla-cake",
                {
                    "name": "Vanilla Dream Cake",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Recipe with ID 'vanilla-cake' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "name": "No ID Cake",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Recipe with ID '' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "name": "Null ID Cake",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "name": "String None ID Cake",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Recipe with ID 'None' does not exist",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "name": "Dict ID Cake",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                {
                    "name": "List ID Cake",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "name": "Numeric ID Cake",
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            # Invalid keys to update
            (
                "arc",
                {
                    "name": None,
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "arc",
                {
                    "name": {},
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "arc",
                {
                    "name": [],
                },
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_update_recipe(
        self, recipe_id: str, recipe_dict: dict, expected_dict: dict
    ):
        """
        Test the API update recipe functionality.

        This test checks if the API update recipe behaves as expected when provided with
        different inputs and expected outcomes. It tests for both successful updates and
        various error scenarios.

        Args:
            recipe_id (str): The recipe ID to update.
            recipe_dict (dict): A dictionary containing the update data.
            expected_dict (dict): A dictionary containing the expected result of the update,
                                  including the expected output, error message, and exception.

        Raises:
            AssertionError: If the actual response or error does not match the expected outcome.
        """
        if expected_dict["expected_output"]:
            response = api_update_recipe(recipe_id, **recipe_dict)
            assert (
                response == expected_dict["expected_output"]
            ), "The response does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_update_recipe(recipe_id, **recipe_dict)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_update_recipe(recipe_id, **recipe_dict)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False, "Expected exception not provided in test case."

    # ------------------------------------------------------------------------------
    # Test api_delete_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "recipe_id,expected_dict",
        [
            # Valid case
            ("arc", {"expected_output": True}),
            # Invalid cases
            (
                "apple-pie",
                {
                    "expected_output": False,
                    "expected_error_message": "No recipes found with ID: apple-pie",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                "",
                {
                    "expected_output": False,
                    "expected_error_message": "No recipes found with ID: ",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                None,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                "None",
                {
                    "expected_output": False,
                    "expected_error_message": "No recipes found with ID: None",
                    "expected_exception": "RuntimeError",
                },
            ),
            (
                {},
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                [],
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
            (
                123,
                {
                    "expected_output": False,
                    "expected_error_message": "Input should be a valid string",
                    "expected_exception": "ValidationError",
                },
            ),
        ],
    )
    def test_api_delete_recipe(self, recipe_id: str, expected_dict: dict):
        """
        Test the deletion of a recipe.

        This test function verifies that the api_delete_recipe function behaves as expected when provided with a recipe ID.
        It checks if the function returns the correct response or raises the expected exceptions with the appropriate error messages.

        Args:
            recipe_id (str): The ID of the recipe to be deleted.
            expected_dict (dict): A dictionary containing the expected outcomes of the test, which includes:
                - 'expected_output': The expected result from the api_delete_recipe function.
                - 'expected_error_message': The expected error message if an exception is raised.
                - 'expected_exception': The type of exception expected to be raised.

        Raises:
            AssertionError: If the actual function output or raised exception does not match the expected results.
        """
        if expected_dict["expected_output"]:
            response = api_delete_recipe(recipe_id)
            assert (
                response == expected_dict["expected_output"]
            ), "The response from api_delete_recipe does not match the expected output."
        else:
            if expected_dict["expected_exception"] == "RuntimeError":
                with pytest.raises(RuntimeError) as e:
                    api_delete_recipe(recipe_id)
                assert e.value.args[0] == expected_dict["expected_error_message"]

            elif expected_dict["expected_exception"] == "ValidationError":
                with pytest.raises(ValidationError) as e:
                    api_delete_recipe(recipe_id)
                assert len(e.value.errors()) == 1
                assert (
                    expected_dict["expected_error_message"]
                    in e.value.errors()[0]["msg"]
                )

            else:
                assert False

    # ------------------------------------------------------------------------------
    # Test api_get_all_recipe functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_recipe(self):
        """
        Test the api_get_all_recipe function.

        This test verifies that the api_get_all_recipe function returns the correct list of recipes,
        and that each recipe has a valid 'created_date' field. The 'created_date' field is not compared
        in the recipe data comparison.
        """
        expected_recipes = [
            {
                "id": "arc",
                "name": "ARC",
                "description": "To measure model's ability in answering genuine grade-school level, multiple-choice science questions on the easy and challenge sets. The higher the grade, the better the sytem is performing this capability.",
                "tags": [],
                "categories": ["Capability"],
                "datasets": ["arc-easy"],
                "prompt_templates": ["mcq-template"],
                "metrics": ["exactstrmatch"],
                "grading_scale": {
                    "A": [80, 100],
                    "B": [60, 79],
                    "C": [40, 59],
                    "D": [20, 39],
                    "E": [0, 19],
                },
                "stats": {
                    "num_of_tags": 0,
                    "num_of_datasets": 1,
                    "num_of_prompt_templates": 1,
                    "num_of_metrics": 1,
                    "num_of_datasets_prompts": {"arc-easy": 1},
                },
            }
        ]

        actual_recipes = api_get_all_recipe()
        assert len(actual_recipes) == len(
            expected_recipes
        ), "The number of recipes returned does not match the expected count."

        for recipe in actual_recipes:
            assert (
                recipe in expected_recipes
            ), f"The recipe data {recipe} does not match any expected recipe."

    # ------------------------------------------------------------------------------
    # Test api_get_all_recipe_name functionality
    # ------------------------------------------------------------------------------
    def test_api_get_all_recipe_name(self):
        """
        Test the api_get_all_recipe_name function.

        This test ensures that the api_get_all_recipe_name function returns a list containing the correct recipe names.
        """
        expected_recipe_names = ["arc"]

        recipe_names_response = api_get_all_recipe_name()
        assert len(recipe_names_response) == len(
            expected_recipe_names
        ), "The number of recipe names returned does not match the expected count."
        for recipe_name in recipe_names_response:
            assert (
                recipe_name in expected_recipe_names
            ), f"Recipe name '{recipe_name}' is not in the list of expected recipe names."
