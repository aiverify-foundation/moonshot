import asyncio

from moonshot.api import (
    api_create_runner,
    api_load_runner, 
    api_load_session, 
    api_get_available_session_info, 
    api_get_all_session_names,
    api_get_all_session_metadata,
    api_update_context_strategy,
    api_update_cs_num_of_prev_prompts,
    api_update_prompt_template,
    api_update_metric,
    api_update_system_prompt,
    api_update_attack_module,
    api_delete_session,
    api_create_session,
    api_get_all_chats_from_session,
    api_get_all_attack_modules,
    api_get_all_attack_module_metadata,
    api_get_all_context_strategies,
    api_get_all_context_strategy_metadata,

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
    return runner.id

def runner_callback_fn(progress_args: dict):
    print("=" * 100)
    print("PROGRESS CALLBACK FN: ", progress_args)
    print("=" * 100)

def run_manual_and_automated_rt():
    runner_name = "test mrt art"
    runner_id = "test-mrt-art"

    endpoints = ["openai-gpt35-turbo-16k", "openai-gpt35-turbo"]
    print("1) Creating Runner")
    runner = api_create_runner(
        name=runner_name,
        endpoints=endpoints,
        progress_callback_func=runner_callback_fn
    )    
    runner.close()

    print("2) Creating Session in Runner")
    api_create_session(runner.id, runner.database_instance, runner.endpoints, {})

    mrt_arguments = {
        "manual_rt_args": {
            "prompt": "hell0 world",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 1
                }],
            "prompt_template_ids": ["mmlu"]
        }
    }
    
    art_arguments = {
        "attack_strategies": [{
            "attack_module_id": "charswap_attack", # sample_attack_module, charswap_attack
            "prompt": "hello world",
            "system_prompt": "test system prompt",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 1
                }],
            "prompt_template_ids": ["mmlu"],
            "metric_ids": ["bleuscore"] 
            },
        ],
        "chat_batch_size": 5
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
    endpoints = ["openai-gpt35-turbo-16k", "openai-gpt35-turbo", "openai-gpt4"]

    mrt_arguments = {
        "manual_rt_args": {
            "prompt": "hell0 world",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 1
                }],
            "prompt_template_ids": ["mmlu"]
        }
    }

    print("1) Creating Runner")
    runner = api_create_runner(
        name=runner_name,
        endpoints=endpoints
    )
    runner.close()

    print("2)Loading and Running runner")
    runner = api_load_runner(runner_id, progress_callback_func=runner_callback_fn)
    loop = asyncio.get_event_loop()
    manual_rt_results = loop.run_until_complete(
        runner.run_red_teaming(mrt_arguments)
    )
    runner.close()
    print("Manual Red Teaming Results:", manual_rt_results)
    return manual_rt_results

def run_automated_rt():
    # Run automated red teaming
    print("Running Automated Red Teaming")
    # Red teaming config
    runner_name = "test art"
    runner_id = "test-art"
    endpoints = ["openai-gpt35-turbo-16k", "openai-gpt35-turbo"]
    art_arguments = {
        "attack_strategies": [{
            "attack_module_id": "charswap_attack", # sample_attack_module, charswap_attack
            "prompt": "hello world",
            "system_prompt": "test system prompt",
            "context_strategy_info": [{
                "context_strategy_id":"add_previous_prompt",
                "num_of_prev_prompts": 1
                }],
            "prompt_template_ids": ["mmlu"],
            "metric_ids": ["bleuscore"] 
            },
        ],
        "chat_batch_size": 5
    }


    # print("1) Creating Runner")
    runner = api_create_runner(
        name=runner_name,
        endpoints=endpoints,
        progress_callback_func=runner_callback_fn,
    )
    runner.close()

    print("2)Loading and Running runner")
    runner = api_load_runner(runner_id, progress_callback_func=runner_callback_fn)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        runner.run_red_teaming(art_arguments)

    )
    runner.close()

def test_art_and_cancel():
    async def run_and_cancel():
        runner_id = "test-art"
        runner = api_load_runner(runner_id)
        art_arguments = {
            "attack_strategies": [{
                "attack_module_id": "charswap_attack", # sample_attack_module, charswap_attack
                "prompt": "hello world",
                "system_prompt": "test system prompt",
                "context_strategy_info": [{
                    "context_strategy_id":"add_previous_prompt",
                    "num_of_prev_prompts": 1
                    }],
                "prompt_template_ids": ["mmlu"],
                "metric_ids": ["bleuscore"],
                "optional_params": {"max_number_of_iteration": 1, 
                           "sample_param_field": "hello world"}
                },
            ],
            "chat_batch_size": 5
        }

        # Run the recipes in a background task
        run_task = asyncio.create_task(runner.run_red_teaming(art_arguments))

        # Wait for 1 second before cancelling
        await asyncio.sleep(1)
        await runner.cancel()

        # Wait for the run task to complete
        await run_task
        runner.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        run_and_cancel()
    )

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

    print("Update Metadata")
    api_update_context_strategy(runner_id, "add_previous_prompt")
    api_update_prompt_template(runner_id, "analogical-similarity")
    api_update_metric(runner_id, "advglue")
    api_update_system_prompt(runner_id, "this is a test system prompt")
    api_update_attack_module(runner_id, "sample_attack_module")
    api_update_cs_num_of_prev_prompts(runner_id, 2)

    print("Get Updated Metadata")
    single_session_metadata = api_load_session(runner_id)
    print(f"{single_session_metadata}\n")

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


if __name__ == "__main__":
# # tests automated and red teaming. creates a runner, and runss manual and automated red teaming
    run_manual_rt()
    run_automated_rt()
    run_manual_and_automated_rt()

    # test cancellation of automated red teaming
    runner_id = "test-art"
    test_art_and_cancel()

    # tests all session apis
    test_session_apis(runner_id)

    # tests all attack apis
    test_attack_apis()