import asyncio
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

def run_manual_and_automated_rt():
    runner_name = "test amrt"
    runner_id = "test-amrt"
    endpoints = ["openai-gpt35-turbo", "openai-gpt4"]
    print("1) Creating Runner")
    runner = api_create_runner(
        name=runner_name,
        endpoints=endpoints,
    )    
    runner.close()

    mrt_arguments = {
        "manual_rt_args": {
            "prompt": "hell0 world",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 4
                }],
            "prompt_template_ids": ["auto-categorisation"]
        }
    }
    
    art_arguments = {
        "attack_strategies": [{
            "attack_module_id": "sample_attack_module",
            "prompt": "hello world",
            "system_prompt": "test system prompt",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 4
                }],
            "prompt_template_ids": ["auto-categorisation"],
            }
        ]
    }

    print("2)Loading and Running runner")
    loop = asyncio.get_event_loop()
    
    # manual red teaming
    runner = api_load_runner(runner_id)
    loop.run_until_complete(
        runner.run_red_teaming(mrt_arguments)
    )
    runner.close()

    # automated red teaming
    runner = api_load_runner(runner_id)
    loop.run_until_complete(
        runner.run_red_teaming(art_arguments)
    )
    runner.close()

def run_manual_rt():
    print("Running Manual Red Teamming")
    runner_name = "test mrt"
    runner_id = "test-mrt"
    endpoints = ["my-openai-gpt35", "my-openai-gpt4"]
    rt_arguments = {
        "manual_rt_args": {
            "prompt": "hell0 world",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 4
                }],
            "prompt_template_ids": ["auto-categorisation"]
        }
    }

    print("1) Creating Runner")
    runner = api_create_runner(
        name=runner_name,
        endpoints=endpoints,
    )
    runner.close()
    print("2)Loading and Running runner")
    runner = api_load_runner(runner_id)
    
    loop = asyncio.get_event_loop()
    runner = api_load_runner(runner_id)
    loop.run_until_complete(
        runner.run_red_teaming(rt_arguments)
    )
    runner.close()

def run_automated_rt():
    # Run automated red teaming
    print("Running Automated Red Teaming")
    # Red teaming config
    runner_name = "test art"
    runner_id = "test-art"
    endpoints = ["my-openai-gpt35", "my-openai-gpt4"]
    rt_arguments = {
        "attack_strategies": [{
            "attack_module_id": "sample_attack_module",
            "prompt": "hello world",
            "system_prompt": "test system prompt",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 4
                }],
            "prompt_template_ids": ["auto-categorisation"],
            }
        ]
    }

    print("1) Creating Runner")
    runner = api_create_runner(
        name=runner_name,
        endpoints=endpoints,
    )
    runner.close()
    print("2)Loading and Running runner")
    runner = api_load_runner(runner_id)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        runner.run_red_teaming(rt_arguments)
    )
    runner.close()

run_manual_and_automated_rt()


# ------------------------------------------------------------------------------
# Session APIs
# ------------------------------------------------------------------------------

runner_id = "test-amrt"

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

# ------------------------------------------------------------------------------
# Attack APIs
# ------------------------------------------------------------------------------

# Get all attack module names
print("Get All Attack Module Names")
print(AttackModule.get_available_items(), "\n")