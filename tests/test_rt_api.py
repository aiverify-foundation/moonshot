import asyncio
from moonshot.src.api.api_runner import api_create_runner, api_load_runner
from moonshot.src.api.api_session import (
    api_load_session, 
    api_get_available_session_info, 
    api_get_all_session_names,
    api_get_all_session_metadata,
    api_update_context_strategy,
    api_update_prompt_template,
    api_delete_session,
    api_create_session,
    api_get_all_chats_from_session
    )
from moonshot.src.api.api_red_teaming import (
    api_get_all_attack_modules,
    api_get_all_attack_module_metadata
)

from moonshot.src.api.api_context_strategy import(
    api_get_all_context_strategies,
    api_get_all_context_strategy_metadata
)


# ------------------------------------------------------------------------------
# Red Teaming APIs
# ------------------------------------------------------------------------------

def test_create_runner(name: str):
    runner = api_create_runner(
        name=name,
        endpoints=["openai-gpt35-turbo", "openai-gpt35-turbo-16k"],
    )
    runner.close()

def run_manual_and_automated_rt(runner_name: str, runner_id: str):
    endpoints = ["openai-gpt35-turbo", "openai-gpt4"]
    print("1) Creating Runner")
    runner = api_create_runner(
        name=runner_name,
        endpoints=endpoints,
    )    
    runner.close()

    print("2) Creating Session in Runner")
    api_create_session(runner.id, runner.database_instance, runner.endpoints, {})

    mrt_arguments = {
        "manual_rt_args": {
            "prompt": "hell0 world",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 4
                }],
            "prompt_template_ids": ["mmlu"]
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
            "prompt_template_ids": ["mmlu"],
            }
        ]
    }

    print("3)Loading and Running runner")
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
            "prompt_template_ids": ["mmlu"]
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

def test_session_apis(runner_id: str):
    # ------------------------------------------------------------------------------
    # Session APIs
    # ------------------------------------------------------------------------------    
    print("Get All Session Names")
    session_names = api_get_all_session_names()
    print(f"{session_names}\n")

    print("Get All Session Metadata")
    session_metadatas = api_get_all_session_metadata()
    print(f"{session_metadatas}\n")

    print("Get Single Session Metadata")
    single_session_metadata = api_load_session(runner_id)
    print(f"{single_session_metadata}\n")

    print("Get Single Session Chats")
    single_session_chats = api_get_all_chats_from_session(runner_id)
    print(f"{single_session_chats}\n")

    print("Get All Session Info")
    all_session_info = api_get_available_session_info()
    print(f"{all_session_info}\n")

    print("Update CS and PT")
    api_update_context_strategy(runner_id, "add_previous_prompt")
    api_update_prompt_template(runner_id, "mmlu")

    # print("Delete Session")
    # api_delete_session(runner_id)

def test_attack_apis():
    # ------------------------------------------------------------------------------
    # Attack APIs
    # ------------------------------------------------------------------------------    
    print("Get All Attack Module Names")
    print(api_get_all_attack_modules(), "\n")

    print("Get All Attack Module Metadata")
    print(api_get_all_attack_module_metadata(), "\n")
    
    print("Get All Context Strategy Names")
    print(api_get_all_context_strategies(), "\n")

    print("Get All Context Strategy Metadata")
    print(api_get_all_context_strategy_metadata(), "\n")    

runner_name = "mytestrunner"
runner_id = "mytestrunner"

# # tests automated and red teaming. creates a runner, and runss manual and automated red teaming
run_manual_and_automated_rt(runner_name, runner_id)

# tests all session apis
test_session_apis(runner_id)

# tests all attack apis
test_attack_apis()