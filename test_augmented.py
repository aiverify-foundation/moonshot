from moonshot.api import api_set_environment_variables, api_augment_recipe, api_augment_dataset
from dotenv import dotenv_values

api_set_environment_variables(dotenv_values(".env"))

print(api_augment_recipe("norman-recipe", "charswap_attack"))
