from moonshot.api import * 
from dotenv import dotenv_values

api_set_environment_variables(dotenv_values(".env"))

test_recipe = api_read_recipe("advglue")
test_attack_module = "charswap_attack"