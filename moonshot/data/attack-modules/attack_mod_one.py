import json

from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.prompt_template.prompt_template_manager import PromptTemplateManager
from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments


class AttackModOne(AttackModule):
    def __init__(self, am_arguments: AttackModuleArguments):
        # Initialize super class
        super().__init__(am_arguments)
        # self.name = name of recipe
        # self.connector_instances = list of connectors. i.e. if the endpoints specified in recipe are gpt3.5 & 4,
        #                            this list will have their respective connectors
        # self.stop_strategy_instance = list of stop strategy instances loaded
        # self.datasets = list of name of the datasets to be used. datasets not loaded yet it's just their names
        # self.prompt_templates = list of name of the pt to be used. pt not loaded yet it's just their names
        # self.metric_instances = list of metrics instances loaded
        # self.context_strategy = context strategy instance loaded (only one instance)

    # loads the contents of the dataset
    def load_dataset_contents(self) -> str:
        """
        Loads the contents of the dataset.

        This method constructs the file path of the dataset using the `EnvironmentVars.DATASETS`
        and the name of the dataset stored in `self.datasets`. It then opens the file,
        reads its contents, and returns the loaded data.

        Returns:
            str: The loaded dataset contents.
        """
        ds_filepath = f"{EnvironmentVars.DATASETS}/{self.datasets[0]}.json"
        with open(ds_filepath, "r", encoding="utf-8") as json_file:
            # ds_info contains name, description, keywords, categories, examples
            ds_info = json.load(json_file)
        return ds_info

    def get_connector(self, connector_name: str):
        """
        Retrieves a specific connector instance.

        This method iterates over the connector instances stored in `self.connector_instances`,
        and returns the connector whose id matches the `connector_name` argument.

        Args:
            connector_name (str): The id of the connector to retrieve.

        Returns:
            The connector instance if found, None otherwise.
        """
        for connector in self.connector_instances:
            if connector.id == connector_name:
                return connector

    async def execute(self):
        """
        Asynchronously executes the attack module.

        This method loads the dataset contents using the `load_dataset_contents` method,
        processes the dataset through a prompt template, retrieves the connector to the first
        Language Learning Model (LLM) and sends the processed dataset as a prompt to the LLM.
        """
        # prepare dataset
        ds_info = self.load_dataset_contents()
        # pass dataset through prompt template
        dataset = PromptTemplateManager.process_prompt_pt(
            ds_info, self.prompt_templates[0]
        )

        # get connector to first LLM and send prompt
        first_llm_connector = self.get_connector("my-openai-gpt35")
        first_response = await first_llm_connector.get_response(dataset)
        print(first_response)

        # insert codes to send response to other LLMs
        # TODO: write a loop and use it with Stop Strategies
