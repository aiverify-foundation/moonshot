from moonshot.api import api_read_recipe,api_set_environment_variables
from dotenv import dotenv_values

api_set_environment_variables(dotenv_values(".env"))

def run_augment_recipe(recipe_id: str, attack_modules) -> str:
    """
    User will select 1 recipe and 1 attack module

    What to do:
    Step 1. Get recipe information
    Step 2. Get all the datasets in that recipe
    Step 3. Augment the datasets
    Step 4. Write each new augmented dataset to a new file
    Step 5. Create new recipe with new set of datasets
    """
    selected_recipe = api_read_recipe("advglue")
    test_attack_module = "charswap_attack"

    print(selected_recipe)
    return ""