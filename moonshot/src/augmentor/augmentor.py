# from moonshot.api import api_read_recipe,api_create_recipe,api_create_datasets,api_read_dataset
from slugify import slugify

from moonshot.src.datasets.dataset import Dataset
from moonshot.src.datasets.dataset_arguments import DatasetArguments
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.recipes.recipe_arguments import RecipeArguments


class Augmentor:
    @staticmethod
    def augment_recipe(recipe_id: str, attack_module: str) -> str:
        """
        Augments a recipe using the specified attack module.

        Args:
            recipe_id (str): The ID of the recipe to be augmented.
            attack_module (str): The attack module to use for augmentation.

        Returns:
            str: The ID of the newly created augmented recipe.
        """
        selected_recipe = Recipe.read(recipe_id)
        datasets = selected_recipe.datasets
        augmented_datasets_id = []

        for dataset in datasets:
            augmented_datasets_id.append(
                Augmentor.augment_dataset(dataset, attack_module)
            )

        # Create recipe with new datasets
        new_rec_name = f"{recipe_id}-{attack_module}"

        try:
            rec_args = RecipeArguments(
                id="",
                name=new_rec_name,
                description=selected_recipe.description,
                tags=selected_recipe.tags,
                categories=selected_recipe.categories,
                datasets=augmented_datasets_id,
                prompt_templates=selected_recipe.prompt_templates,
                metrics=selected_recipe.metrics,
                grading_scale=selected_recipe.grading_scale,
            )
            return Recipe.create(rec_args)
        except Exception as e:
            raise e

    @staticmethod
    def augment_dataset(dataset_id: str, attack_module: str) -> str:
        """
        Augments a dataset using the specified attack module.

        Args:
            dataset_id (str): The ID of the dataset to be augmented.
            attack_module (str): The attack module to use for augmentation.

        Returns:
            str: The ID of the newly created augmented dataset.
        """
        dataset = Dataset.read(dataset_id)
        inputs = dataset.examples
        new_examples = []
        for input in inputs:
            # prompt = input.get("input")
            new_prompts = [
                "new prompt 1",
                "new prompt 2",
                "new prompt 3",
                "new prompt 4",
                "new prompt 5",
                "new prompt 6",
            ]
            new_examples = new_prompts
            break

        try:
            new_name = f"{dataset.id}-{attack_module}"
            new_ds_id = slugify(new_name).lower()
            ds_args = DatasetArguments(
                id="",
                name=new_ds_id,
                description=dataset.description,
                reference=dataset.reference,
                license=dataset.license,
                examples=new_examples,
            )
            Dataset.create(ds_args)
            return new_ds_id
        except Exception as e:
            raise e
