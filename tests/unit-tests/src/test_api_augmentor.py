import pytest
import shutil
import os

from pydantic import ValidationError
from unittest.mock import patch, MagicMock

from moonshot.api import (
    api_augment_dataset,
    api_augment_recipe,
    api_set_environment_variables,
)
class TestCollectionApiAugmentor:
    @pytest.fixture(autouse=True)
    def init(self):
        # Initialize environment variables and copy sample files for testing
        api_set_environment_variables(
            {
                "ATTACK_MODULES": "tests/unit-tests/src/data/attack-modules/",
                "RECIPES": "tests/unit-tests/src/data/recipes/",
                "METRICS": "tests/unit-tests/src/data/metrics/",
                "DATASETS": "tests/unit-tests/src/data/datasets/",
                "IO_MODULES": "tests/unit-tests/src/data/io-modules/",
            }
        )
    
        shutil.copyfile(
            "tests/unit-tests/common/samples/small-test-dataset.json",
            "tests/unit-tests/src/data/datasets/small-test-dataset.json",
        )

        shutil.copyfile(
            "tests/unit-tests/common/samples/test-recipe.json",
            "tests/unit-tests/src/data/recipes/test-recipe.json",
        )

        shutil.copyfile(
            "tests/unit-tests/common/samples/exactstrmatch.py",
            "tests/unit-tests/src/data/metrics/exactstrmatch.py",
        )
        yield

        run_data_files = [
            "tests/unit-tests/src/data/datasets/small-test-dataset.json",
            "tests/unit-tests/src/data/datasets/small-test-dataset-attack-module.json",
            "tests/unit-tests/src/data/recipes/test-recipe.json",
            "tests/unit-tests/src/data/recipes/test-recipe-attack-module.json",
            "tests/unit-tests/src/data/metrics/exactstrmatch.py",
        ]
        for run_data_file in run_data_files:
            if os.path.exists(run_data_file):
                os.remove(run_data_file)

    # ------------------------------------------------------------------------------
    # Test api_augment_dataset functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "dataset_id, attack_module_id, expected_response",
        [   
            # Success Scenario
            ("small-test-dataset", "attack_module", "small-test-dataset-attack-module"),
            # Empty Dataset
            ("", "attack_module", ValueError),
            # Empty Attack Module
            ("small-test-dataset", "", ValueError),
            # Empty Both
            ("", "", ValueError),
            # None Dataset
            (None, "attack_module", ValueError),
            # None Attack Module
            ("small-test-dataset", None, ValueError),
            # Both None
            (None, None, ValueError),
            # Invalid Dataset
            ("missing-dataset", "attack_module", RuntimeError),
            # Invalid Attack Module TODO scenario only valid after merging with attack module
            # ("small-test-dataset", "missing-attack_module", RuntimeError),
        ]
    )
    def test_api_augment_dataset(self, dataset_id, attack_module_id, expected_response):
        if expected_response is RuntimeError:
            expected_messages = [
                "No datasets found with ID:",
                "Dataset ID is empty",
            ]
            with pytest.raises(RuntimeError) as excinfo:
                api_augment_dataset(dataset_id, attack_module_id)
            assert any(msg in str(excinfo.value) for msg in expected_messages)
        elif expected_response is ValueError:
            with pytest.raises(ValueError) as excinfo:
                api_augment_dataset(dataset_id, attack_module_id)
            print(f"Caught ValueError: {excinfo.value}")
            assert str(excinfo.value) == "dataset_id and attack_module_id must not be None"
        else:
            result = api_augment_dataset(dataset_id, attack_module_id)
            assert result == expected_response


    # ------------------------------------------------------------------------------
    # Test api_augment_recipe functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "recipe_id, attack_module_id, expected_response",
        [   
            # Success Scenario
            ("test-recipe", "attack_module", "test-recipe-attack-module"),
            # Empty Recipe
            ("", "attack_module", ValueError),
            # Empty Attack Module
            ("test-recipe", "", ValueError),
            # Empty Both
            ("", "", ValueError),
            # None Recipe
            (None, "attack_module", ValueError),
            # None Attack Module
            ("small-test-dataset", None, ValueError),
            # Both None
            (None, None, ValueError),
            # Invalid Recipe
            ("missing-recipe", "attack_module", RuntimeError),
            # Invalid Attack Module TODO scenario only valid after merging with attack module
            # ("small-test-dataset", "missing-attack_module", RuntimeError),
        ]
    )
    def test_api_augment_recipe(self, recipe_id, attack_module_id, expected_response):
        if expected_response is RuntimeError:
            expected_messages = [
                "No recipes found with ID:",
                "Recipe ID is empty",
            ]
            with pytest.raises(RuntimeError) as excinfo:
                api_augment_recipe(recipe_id, attack_module_id)
            assert any(msg in str(excinfo.value) for msg in expected_messages)
        elif expected_response is ValueError:
            with pytest.raises(ValueError) as excinfo:
                api_augment_recipe(recipe_id, attack_module_id)
            print(f"Caught ValueError: {excinfo.value}")
            assert str(excinfo.value) == "recipe_id and attack_module_id must not be None"
        else:
            result = api_augment_recipe(recipe_id, attack_module_id)
            assert result == expected_response