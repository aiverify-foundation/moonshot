from moonshot.api import api_read_recipe,api_set_environment_variables,api_read_dataset, api_create_recipe, api_create_datasets
from dotenv import dotenv_values
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage

from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.storage.db_interface import DBInterface
import asyncio
from slugify import slugify

api_set_environment_variables(dotenv_values(".env"))

def run_augment_recipe(recipe_id: str, attack_module: str) -> str:
    """
    User will select 1 recipe and 1 attack module

    What to do:
    Step 1. Get recipe information
    Step 2. Get all the datasets in that recipe
    Step 3. Augment the datasets
    Step 4. Write each new augmented dataset to a new file
    Step 5. Create new recipe with new set of datasets

    Returns the new recipe id
    """
    selected_recipe = api_read_recipe(recipe_id)

    datasets = selected_recipe.get("datasets")

    augmented_datasets_id = []

    for dataset in datasets: 
        augmented_datasets_id.append(augment_dataset(dataset,attack_module))

    # Create recipe with new datasets
    new_rec_name = f"{recipe_id}-{attack_module}"
    new_recipe = api_create_recipe(
        name=new_rec_name,
        description=selected_recipe.get("description",""),
        tags=selected_recipe.get("tags",""),
        categories=selected_recipe.get("categories",""),
        datasets=augmented_datasets_id,
        prompt_templates=selected_recipe.get("prompt_templates",""),
        metrics=selected_recipe.get("metrics",""),
        grading_scale=selected_recipe.get("grading_scale","")
    )

    return new_recipe

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
    new_examples = []

    #step 1
    dataset = api_read_dataset(dataset_id)
    inputs = dataset.get("examples")

    for input in inputs:
        prompt = input.get("input")
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

    new_name = f"{dataset.get('name', dataset_id)}-{attack_module}"
    new_ds_id = slugify(new_name).lower()

    api_create_datasets(
        name= new_ds_id,
        description=dataset.get("description",""),
        reference= dataset.get("reference",""),
        license= dataset.get("license",""),
        examples= new_examples,
        method=""
    )

    return new_ds_id

if __name__ == "__main__":
    print(run_augment_recipe("norman-recipe", "charswap_attack"))
