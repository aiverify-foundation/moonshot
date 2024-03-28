import inspect
from typing import Any, Union

from moonshot.src.connectors.connector_manager import ConnectorManager
from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments
from moonshot.src.storage.storage_manager import StorageManager
from moonshot.src.utils.import_modules import (
    create_module_spec,
    import_module_from_spec,
)


class AttackStrategy:
    def __init__(self, args) -> None:
        self.name = args["name"]
        self.description = args["description"]
        self.endpoints = args["endpoints"]
        self.metrics = args["metrics"]
        self.datasets = args["datasets"]
        self.prompt_templates = args["prompt_templates"]
        self.params = args["params"]
        self.attack_strategies = args["attack_strategies"]

        self.prepare_attack_modules()

    def prepare_attack_modules(self) -> Union[list, None]:
        """
        This method prepares all the required attack modules for the attack modules.

        It loads the necessary connectors, metrics, stop strategies, and context strategies.
        It then creates an instance of AttackModuleArguments for each attack module,
        which includes all the necessary components for the attack module to function.

        The method returns a list of these AttackModuleArguments instances.

        Raises:
            RuntimeError: If no Stop Strategy is specified for an attack module.

        Returns:
            list: A list of AttackModuleArguments instances, each representing a fully prepared attack module.
        """
        list_of_attack_modules = []
        list_of_metrics_inst = []
        context_strategy_inst = None

        # get list of connector instances
        list_of_connector_inst = self.load_connectors()

        # get list of metric instances
        if self.metrics:
            for metric in self.metrics:
                list_of_metrics_inst.append(
                    self.get_module_instance(
                        metric, StorageManager.get_metric_filepath(metric)
                    )
                )

        list_of_stop_strategies_inst = []
        if self.attack_strategies:
            for attack_module_dict in self.attack_strategies:
                attack_module_name = attack_module_dict.get("attack_module", None)
                context_strategy_name = attack_module_dict.get("context_strategy", None)
                list_of_stop_strategies = attack_module_dict.get(
                    "stop_strategies", None
                )

                # get list of stop strategy instances
                if list_of_stop_strategies:
                    for stop_strategy_name in list_of_stop_strategies:
                        stop_strategy_inst = self.get_module_instance(
                            stop_strategy_name,
                            StorageManager.get_stop_strategy_filepath(
                                stop_strategy_name
                            ),
                        )
                        list_of_stop_strategies_inst.append(stop_strategy_inst)
                else:
                    raise RuntimeError(
                        "No Stop Strategy specified. Please select at least one Stop Strategy."
                    )

                # get context strategy instance (if any)
                if context_strategy_name:
                    context_strategy_inst = self.get_module_instance(
                        context_strategy_name,
                        StorageManager.get_context_strategy_filepath(
                            context_strategy_name
                        ),
                    )

                am_arguments = AttackModuleArguments(
                    name=attack_module_name,
                    connector_instances=list_of_connector_inst,
                    stop_strategy_instances=list_of_stop_strategies_inst,
                    datasets=self.datasets,
                    prompt_templates=self.prompt_templates,
                    metric_instances=list_of_metrics_inst,
                    context_strategy=context_strategy_inst,
                    params=self.params,
                )

                # store in a dictionary after everything for one attack module is prepared
                list_of_attack_modules.append(am_arguments)

            self.attack_modules = list_of_attack_modules
        else:
            print(
                "No Attack Module specified. Please select at least one Attack Module and try again"
            )

    async def run_attack_modules(self):
        """
        Asynchronously executes all the prepared attack modules.

        This method loads the attack modules using the `load_attack_modules` method and then
        asynchronously executes each attack module in the loaded list.
        """
        attack_module_list = self.load_attack_modules()
        for attack_module in attack_module_list:
            await attack_module.execute()

    def load_attack_modules(self) -> list:
        """
        Loads all the attack modules.

        This method iterates over AttackModuleArguments instances stored in `self.attack_modules`,
        and instantiates an AttackModule instance with each AttackModuleArguments, and appends
        it to a list. The method then returns this list of loaded attack modules.
        """
        attack_module_list = []
        for attack_module_args in self.attack_modules:
            attack_module_instance = AttackModule.load_attack_module(attack_module_args)
            attack_module_list.append(attack_module_instance)
        return attack_module_list

    def load_connectors(self) -> list:
        """
        Loads all the connectors.

        This method iterates over the endpoints stored in `self.endpoints`,
        creates a Connector instance for each endpoint using the `ConnectorManager.create_connector` method,
        and appends it to a list. The method then returns this list of loaded connectors.
        """
        connector_list = []
        for endpoint in self.endpoints:
            endpoint_instance = ConnectorManager.create_connector(
                ConnectorManager.read_endpoint(endpoint)
            )
            connector_list.append(endpoint_instance)
        return connector_list

    def get_module_instance(self, module_name: str, module_path: str) -> Any:
        """
        Creates and returns an instance of a specified module.

        This method takes a module name and a module path as arguments, creates a module specification,
        imports the module from the specification, and returns an instance of the module.
        If no instance of the module is found, it returns None.

        Args:
            module_name (str): The name of the module.
            module_path (str): The path to the module.

        Returns:
            The instance of the module if found, None otherwise.
        """

        # Create the module specification
        module_spec = create_module_spec(
            module_name,
            module_path,
        )

        # Check if the module specification exists
        if module_spec:
            # Import the module
            module = import_module_from_spec(module_spec)

            # Iterate through the attributes of the module
            for attr in dir(module):
                # Get the attribute object
                obj = getattr(module, attr)

                # Check if the attribute is a class and has the same module name as the connector type
                if inspect.isclass(obj) and obj.__module__ == module_name:
                    return obj

        # Return None if no instance of the metric class is found
        return None
