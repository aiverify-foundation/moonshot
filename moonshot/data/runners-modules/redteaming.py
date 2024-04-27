from __future__ import annotations

import time
from typing import Any

from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.redteaming.session.session import SessionMetadata
from moonshot.src.storage.db_interface import DBInterface


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
        runner_args: dict,
        database_instance: DBInterface,
        session_metadata: SessionMetadata,
    ) -> dict:
        """
        Asynchronously generates the red teaming session.

        This method is responsible for the orchestration of the red teaming session. It sets up the necessary
        environment, initializes the attack strategies, and executes the red teaming logic. It handles any errors
        encountered during the session and returns the results in a dictionary format.

        Args:
            event_loop (Any): The event loop in which asynchronous tasks will be scheduled.
            runner_args (dict): A dictionary containing arguments for the red teaming session.
            database_instance (DBAccessor | None): The database instance to connect to, or None if not available.
            session_metadata (SessionMetadata): Metadata associated with the red teaming session.

        Returns:
            dict: A dictionary containing the results of the red teaming session, including any errors encountered.
        """
        self.event_loop = event_loop
        self.runner_args = runner_args
        self.database_instance = database_instance
        self.session_metadata = session_metadata

        # ------------------------------------------------------------------------------
        # Part 1: Load attack module
        # ------------------------------------------------------------------------------
        print("[Red teaming] Part 1: Loading All Attack Module(s)...")
        loaded_attack_modules = []
        try:
            # load red teaming modules
            for attack_strategy_args in self.runner_args.get("attack_strategies", None):
                # load attack module with arguments
                loaded_attack_module = AttackModule.load(
                    AttackModuleArguments(
                        name=attack_strategy_args.get("attack_module_id", ""),
                        connector_eps=self.session_metadata.endpoints
                        if self.session_metadata.endpoints
                        else [],
                        prompt_templates=attack_strategy_args.get(
                            "prompt_template_ids", []
                        ),
                        prompt=attack_strategy_args.get("prompt", ""),
                        system_prompt=attack_strategy_args.get("system_prompt", ""),
                        metric_ids=attack_strategy_args["metric_ids"]
                        if "metric_ids" in attack_strategy_args
                        else [],
                        context_strategy_ids=attack_strategy_args[
                            "context_strategy_ids"
                        ]
                        if "context_strategy_ids" in attack_strategy_args
                        else [],
                        db_instance=self.database_instance,
                    )
                )
                loaded_attack_modules.append(loaded_attack_module)

        except Exception as e:
            print(f"Unable to load attack modules in attack strategy: {str(e)}")

        # ------------------------------------------------------------------------------
        # Part 2: Run attack module(s)
        # ------------------------------------------------------------------------------
        print("[Red teaming] Part 2: Running Attack Module(s)...")

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
        return {}
