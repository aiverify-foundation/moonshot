from __future__ import annotations

from abc import abstractmethod
from datetime import datetime

from jinja2 import Template

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.metrics.metric import Metric
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance

# variable to cap the number of prompts sent to the LLMs in case the stop condition
# of the attack does not get fulfilled
MAX_NO_ITERATIONS = 3


class AttackModule:
    def __init__(self, am_args: AttackModuleArguments):
        self.name = am_args.name
        self.connector_instances = am_args.connector_instances
        self.stop_strategy_instances = am_args.stop_strategy_instances
        self.datasets = am_args.datasets
        self.prompt_templates = am_args.prompt_templates
        self.metric_instances = am_args.metric_instances
        self.context_strategies = am_args.context_strategies
        self.db_instance = am_args.db_instance

    @classmethod
    def load(cls, am_arguments: AttackModuleArguments) -> AttackModule:
        """
        Retrieves an attack module instance by its ID.

        This method attempts to load an attack module instance using the provided ID. If the attack module instance
        is found, it is returned. If the attack module instance does not exist, a RuntimeError is raised.

        Args:
            am_id (str): The unique identifier of the attack module to be retrieved.

        Returns:
            AttackModule: The retrieved attack module instance.

        Raises:
            RuntimeError: If the attack module instance does not exist.
        """
        attack_module_inst = get_instance(
            am_arguments.name,
            Storage.get_filepath(
                EnvVariables.ATTACK_MODULES.name, am_arguments.name, "py"
            ),
        )
        if attack_module_inst:
            return attack_module_inst(am_arguments)
        else:
            raise RuntimeError(
                f"Unable to get defined attack module instance - {am_arguments.name}"
            )

    # TODO to permutate the no. of datasets x prompt templates
    # currently, we're just taking the first dataset and prompt template defined
    def prepare_prompt(self) -> str:
        # if there is at least one dataset defined
        if self.datasets:
            ds_name = self.datasets[0]
            ds_details = Storage.read_object(
                EnvVariables.DATASETS.name, ds_name, "json"
            )
            prompt = ds_details["examples"]

        # TODO: if there is no dataset defined, decide where to get user prompt or a seed
        else:
            prompt = "hello world"

        if self.prompt_templates:
            pt_name = self.prompt_templates[0]
            pt_details = Storage.read_object(
                EnvVariables.PROMPT_TEMPLATES.name, pt_name, "json"
            )
            template = pt_details["template"]
            jinja_template = Template(template)
            return jinja_template.render({"prompt": prompt})

        return prompt

    def get_max_no_iterations(self) -> int:
        """
        Returns the default maximum number of iterations allowed.

        Returns:
            int: The default maximum number of iterations allowed.
        """
        return MAX_NO_ITERATIONS

    def check_stop_condition(
        self,
        prompt: str,
        iteration_count: int,
        llm_response: str,
        metric_instances: list[Metric],
    ) -> bool:
        """
        Checks if any stop strategy triggers the end of the red teaming attack based on the prompt iteration count
        and LLM response.

        Args:
            iteration_count (int): The current prompt iteration count.
            llm_response (str): The response from the LLM model.

        Returns:
            bool: True if any stop strategy triggers the end of the attack, False otherwise.
        """
        for stop_strategy in self.stop_strategy_instances:
            if stop_strategy.stop_red_teaming_attack(
                prompt, (iteration_count + 1), llm_response, self.metric_instances
            ):
                print("Stopping red teaming now as criteria is fulfilled...")
                return True
        return False

    async def send_prompt(
        self,
        connector_instance: Connector,
        prepared_prompt: str,
    ) -> str:
        """
        Sends a prompt to a LLM endpoint, stores LLM prediction in the LLM chat table,
        and returns the predicted results.

        Args:
            connector_instance (Connector): The LLM connector instance to send the prompt to.
            prepared_prompt (str): The prepared prompt to send.

        Returns:
            str: The predicted results from the LLM endpoint.
        """
        prompt_template_name = ""
        if self.prompt_templates:
            prompt_template_name = self.prompt_templates[0]

        dataset_name = ""
        if self.datasets:
            dataset_name = self.datasets[0]

        new_prompt_info = ConnectorPromptArguments(
            prompt_index=1, prompt=prepared_prompt, target=""
        )

        prompt_start_time = datetime.now()

        # sends prompt to endpoint
        prediction_response = await Connector.get_prediction(
            new_prompt_info, connector_instance
        )

        # stores chat prompts, predictions and its config into DB
        chat_record_tuple = (
            "",
            "",
            prompt_template_name,
            dataset_name,
            prepared_prompt,
            prediction_response.predicted_results,
            prediction_response.duration,
            prompt_start_time.strftime("%m/%d/%Y, %H:%M:%S"),
        )

        endpoint_id = connector_instance.id.replace("-", "_")
        sql_create_chat_record = f"""
            INSERT INTO {endpoint_id} (connection_id,context_strategy,prompt_template,prompt,
            prepared_prompt,predicted_result,duration,prompt_time)VALUES(?,?,?,?,?,?,?,?)
            """
        Storage.create_database_record(
            self.db_instance, chat_record_tuple, sql_create_chat_record
        )

        return prediction_response.predicted_results

    @abstractmethod
    async def execute(self):
        pass
