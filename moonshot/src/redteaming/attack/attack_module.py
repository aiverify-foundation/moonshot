import inspect
from abc import abstractmethod
from typing import Any

from moonshot.src.connectors.connector import Connector
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.storage.storage_manager import StorageManager
from moonshot.src.utils.import_modules import (
    create_module_spec,
    import_module_from_spec,
)


class AttackModule:
    def __init__(self, am_args: AttackModuleArguments) -> None:
        self.name = am_args.name
        self.connector_instances = am_args.connector_instances
        self.stop_strategy_instances = am_args.stop_strategy_instances
        self.datasets = am_args.datasets
        self.prompt_templates = am_args.prompt_templates
        self.metric_instances = am_args.metric_instances
        self.context_strategy = am_args.context_strategy

    @abstractmethod
    async def execute(self):
        pass

    @abstractmethod
    def get_connector(self, connector_name: str) -> Connector:
        pass

    @classmethod
    def load_attack_module(cls, am_args: AttackModuleArguments):
        attack_module_instance = cls._get_attack_module_instance(am_args.name)
        if attack_module_instance:
            return attack_module_instance(am_args)
        else:
            raise RuntimeError(f"Unable to get defined attack module - {am_args.name}")

    @staticmethod
    def _get_attack_module_instance(am_name: str) -> Any:
        # Create the module specification
        module_spec = create_module_spec(
            am_name,
            StorageManager.get_attack_module_filepath(am_name),
        )

        # Check if the module specification exists
        if module_spec:
            # Import the module
            module = import_module_from_spec(module_spec)

            # Iterate through the attributes of the module
            for attr in dir(module):
                # Get the attribute object
                obj = getattr(module, attr)

                # Check if the attribute is a class and has the same module name as the attack module
                if inspect.isclass(obj) and obj.__module__ == am_name:
                    return obj

        # Return None if no instance of the metric class is found
        return None
