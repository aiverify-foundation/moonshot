from __future__ import annotations

from abc import abstractmethod

from jinja2 import Template

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class AttackModule:
    def __init__(self, am_args: AttackModuleArguments):
        self.name = am_args.name
        self.connector_instances = am_args.connector_instances
        self.stop_strategy_instances = am_args.stop_strategy_instances
        self.datasets = am_args.datasets
        self.prompt_templates = am_args.prompt_templates
        self.metric_instances = am_args.metric_instances
        self.context_strategies = am_args.context_strategies

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

    # TODO to finalise decision on how to process recipe with multiple prompt templates and datasets
    def prepare_prompt(self) -> str:
        prompt = ""

        # if there is at least one dataset defined
        if self.datasets:
            ds_name = self.datasets[0]
            ds_details = Storage.read_object(
                EnvVariables.DATASETS.name, ds_name, "json"
            )
            prompt = ds_details["examples"]

        # TODO: if there is not dataset defined, decide where to get user prompt or a seed
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

    @abstractmethod
    async def execute(self):
        pass

    @abstractmethod
    def check_stop_condition(self) -> bool:
        pass
