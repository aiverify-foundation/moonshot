from ast import literal_eval
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from moonshot.integrations.cli.benchmark.recipe import (
    add_recipe,
    delete_recipe,
    list_recipes,
    run_recipe,
    update_recipe,
    view_recipe,
)


class TestCollectionCliRecipe:
    api_response = [
        {
            "id": "realtime-qa",
            "name": "RealtimeQA",
            "description": "Some description.",
            "tags": ["Hallucination"],
            "categories": ["Trust & Safety"],
            "datasets": ["realtimeqa-past"],
            "prompt_templates": [],
            "metrics": ["exactstrmatch"],
            "grading_scale": {"A": [80, 100]},
            "stats": {
                "num_of_tags": 1,
                "num_of_datasets": 1,
                "num_of_prompt_templates": 0,
                "num_of_metrics": 1,
                "num_of_datasets_prompts": {"realtimeqa-past": 50},
            },
        }
    ]
    api_response_pagination = [
        {
            "id": "realtime-qa",
            "name": "RealtimeQA",
            "description": "Some description.",
            "tags": ["Hallucination"],
            "categories": ["Trust & Safety"],
            "datasets": ["realtimeqa-past"],
            "prompt_templates": [],
            "metrics": ["exactstrmatch"],
            "grading_scale": {"A": [80, 100]},
            "stats": {
                "num_of_tags": 1,
                "num_of_datasets": 1,
                "num_of_prompt_templates": 0,
                "num_of_metrics": 1,
                "num_of_datasets_prompts": {"realtimeqa-past": 50},
            },
            "idx": 1,
        }
    ]

    @pytest.fixture(autouse=True)
    def init(self):
        # Perform tests
        yield

    # ------------------------------------------------------------------------------
    # Test add_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "name, description, tags, categories, datasets, prompt_templates, metrics, grading_scale, expected_output, expected_call",
        [
            # Valid case
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: Recipe (new_recipe_id) created.",
                True,
            ),
            # Invalid case for name
            (
                None,
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                99,
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'name' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'name' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case for description
            (
                "New Recipe ID",
                None,
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'description' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'description' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                99,
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'description' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                {},
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'description' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                [],
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'description' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                (),
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'description' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                True,
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'description' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case for tags - not a list of strings
            (
                "New Recipe ID",
                "This is a test recipe.",
                "None",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a list of strings after evaluation.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "[123, 'recipe2']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a list of strings after evaluation.",
                False,
            ),
            # Invalid case for tags
            (
                "New Recipe ID",
                "This is a test recipe.",
                None,
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                99,
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                {},
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                [],
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                (),
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                True,
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'tags' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case for categories - not a list of strings
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "None",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a list of strings after evaluation.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "[123, 'category2']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a list of strings after evaluation.",
                False,
            ),
            # Invalid case for categories
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                None,
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                99,
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                {},
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                [],
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                (),
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                True,
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'categories' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case for datasets - not a list of strings
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "None",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a list of strings after evaluation.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "[123, 'dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a list of strings after evaluation.",
                False,
            ),
            # Invalid case for datasets
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                None,
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                99,
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                {},
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                [],
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                (),
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                True,
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'datasets' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case for prompt_templates - not a list of strings
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "None",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a list of strings after evaluation.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "[123, 'template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a list of strings after evaluation.",
                False,
            ),
            # Invalid case for prompt_templates
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                None,
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                99,
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                {},
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                [],
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                (),
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                True,
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'prompt_templates' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case for metrics - not a list of strings
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "None",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a list of strings after evaluation.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "[123, 'metric2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a list of strings after evaluation.",
                False,
            ),
            # Invalid case for metrics
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                None,
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                99,
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                {},
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                [],
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                (),
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                True,
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: The 'metrics' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case for grading_scale - not a dictionary
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "None",
                "[add_recipe]: The 'grading_scale' argument must be a dictionary after evaluation.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "[123, 'scale2']",
                "[add_recipe]: The 'grading_scale' argument must be a dictionary after evaluation.",
                False,
            ),
            # Invalid case for grading_scale
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                None,
                "[add_recipe]: The 'grading_scale' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "",
                "[add_recipe]: The 'grading_scale' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                99,
                "[add_recipe]: The 'grading_scale' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                {},
                "[add_recipe]: The 'grading_scale' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                [],
                "[add_recipe]: The 'grading_scale' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                (),
                "[add_recipe]: The 'grading_scale' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                True,
                "[add_recipe]: The 'grading_scale' argument must be a non-empty string and not None.",
                False,
            ),
            # Exception case
            (
                "New Recipe ID",
                "This is a test recipe.",
                "['tag1']",
                "['category1']",
                "['dataset1','dataset2']",
                "['prompt_template1','prompt_template2']",
                "['metrics1', 'metrics2']",
                "{'A': [80,100], 'B': [60,79]}",
                "[add_recipe]: An error has occurred while creating recipe.",
                True,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.recipe.api_create_recipe")
    def test_add_recipe(
        self,
        mock_api_create_recipe,
        name,
        description,
        tags,
        categories,
        datasets,
        prompt_templates,
        metrics,
        grading_scale,
        expected_output,
        expected_call,
        capsys,
    ):
        if "error" in expected_output:
            mock_api_create_recipe.side_effect = Exception(
                "An error has occurred while creating recipe."
            )
        else:
            mock_api_create_recipe.return_value = "new_recipe_id"

        class Args:
            pass

        args = Args()
        args.name = name
        args.description = description
        args.tags = tags
        args.categories = categories
        args.datasets = datasets
        args.prompt_templates = prompt_templates
        args.metrics = metrics
        args.grading_scale = grading_scale

        add_recipe(args)

        captured = capsys.readouterr()
        assert expected_output == captured.out.strip()

        if expected_call:
            mock_api_create_recipe.assert_called_once_with(
                name,
                description,
                eval(tags),
                eval(categories),
                eval(datasets),
                eval(prompt_templates),
                eval(metrics),
                eval(grading_scale),
            )
        else:
            mock_api_create_recipe.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test list_recipes functionality with non-mocked filter-data
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
            # No recipes
            (None, None, [], None, "There are no recipes found.", False),
            (
                "realtime",
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
            ("Recipe", "(1, 1)", [], None, "There are no recipes found.", False),
            # Invalid cases for find
            (
                "",
                None,
                api_response,
                None,
                "[list_recipes]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                99,
                None,
                api_response,
                None,
                "[list_recipes]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                None,
                api_response,
                None,
                "[list_recipes]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                None,
                api_response,
                None,
                "[list_recipes]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                None,
                api_response,
                None,
                "[list_recipes]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                None,
                api_response,
                None,
                "[list_recipes]: The 'find' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid cases for pagination
            (
                None,
                "",
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                99,
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                {},
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                [],
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                (),
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                True,
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "(1, 'a')",
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, 2, 3)",
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(1, )",
                api_response,
                None,
                "[list_recipes]: The 'pagination' argument must be a tuple of two integers.",
                False,
            ),
            (
                None,
                "(0, 1)",
                api_response,
                None,
                "[list_recipes]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, 0)",
                api_response,
                None,
                "[list_recipes]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(0, 0)",
                api_response,
                None,
                "[list_recipes]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(1, -1)",
                api_response,
                None,
                "[list_recipes]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, 1)",
                api_response,
                None,
                "[list_recipes]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            (
                None,
                "(-1, -1)",
                api_response,
                None,
                "[list_recipes]: Invalid page number or page size. Page number and page size should start from 1.",
                False,
            ),
            # Exception case
            (
                None,
                None,
                api_response,
                None,
                "[list_recipes]: An error has occurred while listing recipes.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.recipe.api_get_all_recipe")
    @patch("moonshot.integrations.cli.benchmark.recipe._display_recipes")
    def test_list_recipes(
        self,
        mock_display_recipes,
        mock_api_get_all_recipe,
        find,
        pagination,
        api_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_get_all_recipe.side_effect = Exception(
                "An error has occurred while listing recipes."
            )
        else:
            mock_api_get_all_recipe.return_value = api_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_recipes(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_recipes.assert_called_once_with(api_response)
        else:
            mock_display_recipes.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test list_recipes functionality with mocked filter-data
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
                "Recipe",
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
                "There are no recipes found.",
                False,
            ),
            # Case where filtered_response is an empty list
            (
                None,
                None,
                api_response,
                [],
                None,
                "There are no recipes found.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.recipe.api_get_all_recipe")
    @patch("moonshot.integrations.cli.benchmark.recipe._display_recipes")
    @patch("moonshot.integrations.cli.benchmark.recipe.filter_data")
    def test_list_recipes_filtered(
        self,
        mock_filter_data,
        mock_display_recipes,
        mock_api_get_all_recipe,
        find,
        pagination,
        api_response,
        filtered_response,
        expected_output,
        expected_log,
        to_be_called,
        capsys,
    ):
        mock_api_get_all_recipe.return_value = api_response
        mock_filter_data.return_value = filtered_response

        class Args:
            pass

        args = Args()
        args.find = find
        args.pagination = pagination

        result = list_recipes(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()
        assert result == expected_output

        if to_be_called:
            mock_display_recipes.assert_called_once_with(filtered_response)
        else:
            mock_display_recipes.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test view_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "recipe_id, api_response, expected_log, to_be_called",
        [
            # Valid case
            (
                "1",
                api_response,
                "",
                True,
            ),
            # Invalid case: recipe_id is None
            (
                None,
                api_response,
                "[view_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case: recipe_id is not a string
            (
                "",
                api_response,
                "[view_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                api_response,
                "[view_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                api_response,
                "[view_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                api_response,
                "[view_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                api_response,
                "[view_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                api_response,
                "[view_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            # Exception case: api_read_recipe raises an exception
            (
                "1",
                api_response,
                "[view_recipe]: An error has occurred while reading the recipe.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.recipe.api_read_recipe")
    @patch("moonshot.integrations.cli.benchmark.recipe._display_recipes")
    def test_view_recipe(
        self,
        mock_display_recipes,
        mock_api_read_recipe,
        recipe_id,
        api_response,
        expected_log,
        to_be_called,
        capsys,
    ):
        if "error" in expected_log:
            mock_api_read_recipe.side_effect = Exception(
                "An error has occurred while reading the recipe."
            )
        else:
            mock_api_read_recipe.return_value = api_response

        class Args:
            pass

        args = Args()
        args.recipe = recipe_id

        view_recipe(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_display_recipes.assert_called_once_with([api_response])
        else:
            mock_display_recipes.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test run_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "name, recipes, endpoints, prompt_selection_percentage, random_seed, system_prompt, \
        runner_proc_module, result_proc_module, expected_log",
        [
            # Valid case
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
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
                "['recipe1', 'recipe2']",
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
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                None,
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                123,
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                {},
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                [],
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                (),
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'name' argument must be a non-empty string and not None.",
            ),
            (
                True,
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'name' argument must be a non-empty string and not None.",
            ),
            # Invalid case: recipes is not a list of string
            (
                "Test Runner",
                "[123, 123]",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'recipes' argument must evaluate to a list of strings.",
            ),
            # Invalid case: recipes is not a string
            (
                "Test Runner",
                None,
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'recipes' argument must be a non-empty string and not None.",
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
                "[run_recipe]: The 'recipes' argument must be a non-empty string and not None.",
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
                "[run_recipe]: The 'recipes' argument must be a non-empty string and not None.",
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
                "[run_recipe]: The 'recipes' argument must be a non-empty string and not None.",
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
                "[run_recipe]: The 'recipes' argument must be a non-empty string and not None.",
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
                "[run_recipe]: The 'recipes' argument must be a non-empty string and not None.",
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
                "[run_recipe]: The 'recipes' argument must be a non-empty string and not None.",
            ),
            # Invalid case: endpoints is not a list of string
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "[123, 123]",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'endpoints' argument must evaluate to a list of strings.",
            ),
            # Invalid case: endpoints is not a string
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                None,
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                123,
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                {},
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                [],
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                (),
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                True,
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'endpoints' argument must be a non-empty string and not None.",
            ),
            # Invalid case: prompt_selection_percentage is 0
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                0,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be between 1 - 100.",
            ),
            # Invalid case: prompt_selection_percentage is -1
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                -1,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be between 1 - 100.",
            ),
            # Invalid case: prompt_selection_percentage is 101
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                101,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be between 1 - 100.",
            ),
            # Invalid case: prompt_selection_percentage is not an integer
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                None,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                "",
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                {},
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                [],
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                (),
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                True,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'prompt_selection_percentage' argument must be an integer.",
            ),
            # Invalid case: random_seed is not an integer
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                None,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                "",
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                {},
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                [],
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                (),
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'random_seed' argument must be an integer.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                True,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: The 'random_seed' argument must be an integer.",
            ),
            # Invalid case: system_prompt is None
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                None,
                "runner_module",
                "result_module",
                "[run_recipe]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                {},
                "runner_module",
                "result_module",
                "[run_recipe]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                [],
                "runner_module",
                "result_module",
                "[run_recipe]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                (),
                "runner_module",
                "result_module",
                "[run_recipe]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                True,
                "runner_module",
                "result_module",
                "[run_recipe]: The 'system_prompt' argument must be a non-empty string and not None.",
            ),
            # Invalid case: runner_proc_module is None
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                None,
                "result_module",
                "[run_recipe]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "",
                "result_module",
                "[run_recipe]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                {},
                "result_module",
                "[run_recipe]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                [],
                "result_module",
                "[run_recipe]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                (),
                "result_module",
                "[run_recipe]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                True,
                "result_module",
                "[run_recipe]: The 'runner_proc_module' argument must be a non-empty string and not None.",
            ),
            # Invalid case: result_proc_module is None
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                None,
                "[run_recipe]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "",
                "[run_recipe]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                {},
                "[run_recipe]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                [],
                "[run_recipe]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                (),
                "[run_recipe]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                True,
                "[run_recipe]: The 'result_proc_module' argument must be a non-empty string and not None.",
            ),
            # Exception case: api_create_runner raises an exception
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: An error has occurred while creating the runner.",
            ),
            # Exception case: api_load_runner raises an exception
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: An error has occurred while loading the runner.",
            ),
            # Exception case: api_get_all_runner_name raises an exception
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: An error has occurred while getting all runner names.",
            ),
            # Exception case: api_get_all_run raises an exception
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: An error has occurred while getting all runs.",
            ),
            # Exception case: no results raises an exception
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: There are no results generated.",
            ),
            # Exception case: show_recipe_results raises an exception
            (
                "Test Runner",
                "['recipe1', 'recipe2']",
                "['endpoint1', 'endpoint2']",
                10,
                42,
                "Test system prompt",
                "runner_module",
                "result_module",
                "[run_recipe]: An error has occurred while showing recipe results.",
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.recipe.api_get_all_runner_name")
    @patch("moonshot.integrations.cli.benchmark.recipe.api_load_runner")
    @patch("moonshot.integrations.cli.benchmark.recipe.api_create_runner")
    @patch("moonshot.integrations.cli.benchmark.recipe.api_get_all_run")
    @patch("moonshot.integrations.cli.benchmark.recipe._show_recipe_results")
    def test_run_recipe(
        self,
        mock_show_recipe_results,
        mock_api_get_all_run,
        mock_api_create_runner,
        mock_api_load_runner,
        mock_api_get_all_runner_name,
        name,
        recipes,
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

        elif "showing recipe results" in expected_log:
            to_trigger_called = True
            mock_api_get_all_runner_name.return_value = []
            mock_api_create_runner.return_value = AsyncMock()
            mock_api_get_all_run.return_value = [
                {"results": {"metadata": {"duration": 10}}}
            ]
            mock_show_recipe_results.side_effect = Exception(
                "An error has occurred while showing recipe results."
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
        args.recipes = recipes
        args.endpoints = endpoints
        args.prompt_selection_percentage = prompt_selection_percentage
        args.random_seed = random_seed
        args.system_prompt = system_prompt
        args.runner_proc_module = runner_proc_module
        args.result_proc_module = result_proc_module

        run_recipe(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if not expected_log or to_trigger_called:
            mock_show_recipe_results.assert_called_once()
        else:
            mock_show_recipe_results.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test update_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "recipe, update_values, expected_log, to_be_called",
        [
            # Valid case
            (
                "Recipe 1",
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: Recipe updated.",
                True,
            ),
            # Invalid case - recipe
            (
                "",
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            # Invalid case - update values
            (
                "Recipe 1",
                "",
                "[update_recipe]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Recipe 1",
                "['', '']",
                "[update_recipe]: The 'update_values' argument must evaluate to a list of tuples.",
                False,
            ),
            (
                "Recipe 1",
                "[[], ()]",
                "[update_recipe]: The 'update_values' argument must evaluate to a list of tuples.",
                False,
            ),
            (
                "Recipe 1",
                None,
                "[update_recipe]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Recipe 1",
                123,
                "[update_recipe]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Recipe 1",
                {},
                "[update_recipe]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Recipe 1",
                [],
                "[update_recipe]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Recipe 1",
                (),
                "[update_recipe]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            (
                "Recipe 1",
                True,
                "[update_recipe]: The 'update_values' argument must be a non-empty string and not None.",
                False,
            ),
            # Test case: API update raises an exception
            (
                "Recipe 1",
                "[('name', 'Updated Recipe'), ('description', 'Updated description')]",
                "[update_recipe]: An error has occurred while updating the recipe.",
                True,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.recipe.api_update_recipe")
    def test_update_recipe(
        self,
        mock_api_update_recipe,
        capsys,
        recipe,
        update_values,
        expected_log,
        to_be_called,
    ):
        if "error" in expected_log:
            mock_api_update_recipe.side_effect = Exception(
                "An error has occurred while updating the recipe."
            )
        else:
            mock_api_update_recipe.return_value = "updated"

        class Args:
            pass

        args = Args()
        args.recipe = recipe
        args.update_values = update_values

        update_recipe(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_update_recipe.assert_called_once_with(
                args.recipe, **dict(literal_eval(args.update_values))
            )
        else:
            mock_api_update_recipe.assert_not_called()

    # ------------------------------------------------------------------------------
    # Test delete_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "recipe, expected_log, to_be_called",
        [
            # Valid case
            ("Recipe 1", "[delete_recipe]: Recipe deleted.", True),
            # Invalid case - recipe
            (
                "",
                "[delete_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                None,
                "[delete_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                123,
                "[delete_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                {},
                "[delete_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                [],
                "[delete_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                (),
                "[delete_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
            (
                True,
                "[delete_recipe]: The 'recipe' argument must be a non-empty string and not None.",
                False,
            ),
        ],
    )
    @patch("moonshot.integrations.cli.benchmark.recipe.api_delete_recipe")
    def test_delete_recipe(
        self, mock_api_delete_recipe, capsys, recipe, expected_log, to_be_called
    ):
        class Args:
            pass

        args = Args()
        args.recipe = recipe

        with patch(
            "moonshot.integrations.cli.benchmark.recipe.console.input",
            return_value="y",
        ):
            with patch("moonshot.integrations.cli.benchmark.recipe.console.print"):
                delete_recipe(args)

        captured = capsys.readouterr()
        assert expected_log == captured.out.strip()

        if to_be_called:
            mock_api_delete_recipe.assert_called_once_with(args.recipe)
        else:
            mock_api_delete_recipe.assert_not_called()

    @patch("moonshot.integrations.cli.benchmark.recipe.console.input", return_value="y")
    @patch("moonshot.integrations.cli.benchmark.recipe.api_delete_recipe")
    def test_delete_recipe_confirm_yes(self, mock_delete, mock_input):
        args = MagicMock()
        args.recipe = "test_recipe_id"

        delete_recipe(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the recipe (y/N)? [/]"
        )
        mock_delete.assert_called_once_with("test_recipe_id")

    @patch("moonshot.integrations.cli.benchmark.recipe.console.input", return_value="n")
    @patch("moonshot.integrations.cli.benchmark.recipe.api_delete_recipe")
    def test_delete_recipe_confirm_no(self, mock_delete, mock_input):
        args = MagicMock()
        args.recipe = "test_recipe_id"

        delete_recipe(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the recipe (y/N)? [/]"
        )
        mock_delete.assert_not_called()

    @patch("moonshot.integrations.cli.benchmark.recipe.console.input", return_value="n")
    @patch("moonshot.integrations.cli.benchmark.recipe.console.print")
    @patch("moonshot.integrations.cli.benchmark.recipe.api_delete_recipe")
    def test_delete_recipe_cancelled_output(self, mock_delete, mock_print, mock_input):
        args = MagicMock()
        args.recipe = "test_recipe_id"

        delete_recipe(args)

        mock_input.assert_called_once_with(
            "[bold red]Are you sure you want to delete the recipe (y/N)? [/]"
        )
        mock_print.assert_called_once_with("[bold yellow]Recipe deletion cancelled.[/]")
        mock_delete.assert_not_called()
