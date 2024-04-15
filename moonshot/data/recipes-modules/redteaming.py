from __future__ import annotations

import time
from typing import Any, Callable

from moonshot.src.connectors.connector import Connector
from moonshot.src.metrics.metric import Metric
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.redteaming.attack.context_strategy import ContextStrategy
from moonshot.src.redteaming.attack.stop_strategy import StopStrategy
from moonshot.src.storage.db_accessor import DBAccessor
from moonshot.src.storage.storage import Storage


class RedTeaming:
    sql_create_session_metadata_table = """
            CREATE TABLE IF NOT EXISTS session_metadata_table (
            session_id text PRIMARY KEY NOT NULL,
            name text NOT NULL,
            description text NOT NULL,
            endpoints text NOT NULL,
            created_epoch INTEGER NOT NULL,
            created_datetime text NOT NULL,
            context_strategy text,
            prompt_template text,
            chat_ids text
            );
    """
    sql_create_chat_metadata_table = """
        CREATE TABLE IF NOT EXISTS chat_metadata_table (
        chat_id text PRIMARY KEY,
        endpoint text NOT NULL,
        created_epoch INTEGER NOT NULL,
        created_datetime text NOT NULL
        );
    """

    async def generate(
        self,
        event_loop: Any,
        database_instance: DBAccessor | None,
        num_of_prompts: int,
        recipe_inst: Recipe,
        recipe_eps: list[Connector],
        metrics_insts: list[Metric],
        handle_error_message_callback: Callable,
    ) -> dict:
        self.event_loop = event_loop
        self.database_instance = database_instance
        self.num_of_prompts = num_of_prompts
        self.recipe_instance = recipe_inst
        self.recipe_eps = recipe_eps
        self.metrics_instances = metrics_insts
        self.handle_error_message = handle_error_message_callback

        # ------------------------------------------------------------------------------
        # Part 1: Create new chat table(s)
        # ------------------------------------------------------------------------------
        print("[Red Teaming] Part 1: Creating chat table(s)...")

        # Create chat_tables
        if database_instance:
            for endpoint in recipe_eps:
                endpoint_id = endpoint.id.replace("-", "_")
                sql_create_chat_history_table = f"""
                    CREATE TABLE IF NOT EXISTS {endpoint_id} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    connection_id text NOT NULL,
                    context_strategy text,
                    prompt_template text,
                    prompt text NOT NULL,
                    prepared_prompt text NOT NULL,
                    predicted_result text NOT NULL,
                    duration text NOT NULL,
                    prompt_time text NOT NULL
                    );
                """
                Storage.create_database_table(
                    database_instance, sql_create_chat_history_table
                )

        else:
            raise RuntimeError("Failed to get database instance.")

        # ------------------------------------------------------------------------------
        # Part 2: Load Attack Module(s) and Stop Strategy Module(s)
        # ------------------------------------------------------------------------------
        print(
            "[Red teaming] Part 2: Loading Attack Module(s) and Stop Strategy Module(s)..."
        )

        loaded_attack_modules = []
        for attack_strategy in recipe_inst.attack_strategies:
            try:
                # get name of attack module
                attack_module_name = attack_strategy["attack_module"]

                # iterate through stop_strategies, load the modules and store in list
                stop_strategy_insts = [
                    StopStrategy.load(stop_strategy_name)
                    for stop_strategy_name in attack_strategy["stop_strategies"]
                ]

                # load context strategy is specified
                context_strategy_insts = []
                if "context_strategies" in attack_strategy.keys():
                    context_strategy_insts = [
                        ContextStrategy.load(context_strategy_name)
                        for context_strategy_name in attack_strategy[
                            "context_strategies"
                        ]
                    ]

                # prepare attack module arguments
                am_arguments = AttackModuleArguments(
                    name=attack_module_name,
                    recipe_id=recipe_inst.id,
                    num_of_prompts=self.num_of_prompts,
                    connector_instances=recipe_eps,
                    stop_strategy_instances=stop_strategy_insts,
                    datasets=self.recipe_instance.datasets,
                    prompt_templates=self.recipe_instance.prompt_templates,
                    metric_instances=self.metrics_instances,
                    context_strategies=context_strategy_insts,
                    db_instance=self.database_instance,
                )
                loaded_attack_modules.append(AttackModule.load(am_arguments))

            except KeyError:
                print("Attack Module and Stop Strategy are required in red teaming.")

        # ------------------------------------------------------------------------------
        # Part 3: Run attack module(s)
        # ------------------------------------------------------------------------------
        print("[Red teaming] Part 3: Running Attack Module(s)...")

        responses_from_attack_module = []
        for attack_module in loaded_attack_modules:
            print(f"[Red teaming] Starting to run attack module [{attack_module.name}]")
            start_time = time.perf_counter()

            attack_module_response = await attack_module.execute()
            print(
                f"[Red teaming] Running attack module [{attack_module.name}] took "
                f"{(time.perf_counter() - start_time):.4f}s"
            )
            responses_from_attack_module.append(attack_module_response)

        return {"responses_from_att_modules": responses_from_attack_module}
