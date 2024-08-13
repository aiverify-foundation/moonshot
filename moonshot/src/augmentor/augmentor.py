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
        User will select 1 recipe and 1 attack module

        What to do:
        Step 1. Get recipe information
        Step 2. Get all the datasets in that recipe
        Step 3. Augment the datasets
        Step 4. Write each new augmented dataset to a new file
        Step 5. Create new recipe with new set of datasets
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
        Step 1. Get the Datasets
        Step 2. Get the prompts
        Step 3. Load attack module
        Step 4. Generate new prompts
        Step 5. Write new dataset to file
        Step 6. Use existing license and references

        Returns the new dataset id
        """

        # step 1
        dataset = Dataset.read(dataset_id)
        inputs = dataset.examples

        # step 2 call AM
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
