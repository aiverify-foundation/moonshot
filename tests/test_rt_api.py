from moonshot.src.api.api_red_teaming import api_run_red_teaming
from moonshot.src.redteaming.session.session import Session
from moonshot.src.api.api_runner import api_create_runner, api_load_runner
from moonshot.src.api.api_session import (
    api_load_session, 
    api_get_available_session_info, 
    api_get_all_session_names,
    api_get_all_session_metadata,
    api_update_context_strategy,
    api_update_prompt_template,
    api_delete_session
    )
from moonshot.src.redteaming.attack.attack_module import AttackModule

# ------------------------------------------------------------------------------
# Red Teaming APIs
# ------------------------------------------------------------------------------

# Run automated red teaming
print("Running Automated Red Teaming")

# Red teaming config
runner_name = "test rt runner"
runner_id = "test-rt-runner"
endpoints = ["my-openai-gpt35", "my-openai-gpt4"]
rt_arguments = {
    "attack_strategies": [{
        "attack_module_id": "sample_attack_module",
        "prompt": "hello world",
        "system_prompt": "test system prompt",
        "context_strategy_ids": ["add_previous_prompt"],
        "prompt_template_ids": ["auto-categorisation"],
        }
    ]
}

print("1) Creating Runner")
runner = api_create_runner(
    name=runner_name,
    endpoints=["my-openai-gpt35", "my-openai-gpt4"],
)
runner.close()

print("2)Loading and Running runner")
runner = api_load_runner(runner_id)
api_run_red_teaming(runner, rt_arguments)

# Get all attack module names
print("Get All Attack Module Names")
print(AttackModule.get_available_items(), "\n")

# ------------------------------------------------------------------------------
# Session APIs
# ------------------------------------------------------------------------------

# Replace this ID with something 
print("Get All Session Names")
session_names = api_get_all_session_names()
print(f"{session_names}\n")

print("Get All Session Metadata")
session_metadatas = api_get_all_session_metadata()
print(f"{session_metadatas}\n")

print("Get Single Session Metadata")
single_session = api_load_session(runner_id)
print(f"{single_session}\n")

print("Get All Session Info")
all_session_info = api_get_available_session_info()
print(f"{all_session_info}\n")

print("Update CS and PT")
api_update_context_strategy(runner_id, "add_previous_prompt")
api_update_prompt_template(runner_id, "mmlu")

print("Delete Session")
# api_delete_session(runner_id)
