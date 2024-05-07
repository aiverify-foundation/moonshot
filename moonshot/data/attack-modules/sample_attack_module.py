from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments


class SampleAttackModule(AttackModule):
    def __init__(self, am_arguments: AttackModuleArguments | None = None):
        # Initialize super class
        super().__init__(am_arguments)
        self.name = "Sample Attack Module"
        self.description = "This is a sample attack module."

    async def execute(self):
        """
        Asynchronously executes the attack module.

        This method loads the dataset contents using the `load_dataset_contents` method,
        processes the dataset through a prompt template, retrieves the connector to the first
        Language Learning Model (LLM) and sends the processed dataset as a prompt to the LLM.
        """
        self.load_modules()
        return await self.perform_attack_default()

    async def perform_attack_default(self) -> list:
        """
        Asynchronously performs the default attack.
        This function will take the defined context strategy and prompt template and append contents
        to the given prompt. It will then send the modified prompt to all the LLM endpoints.

        This method retrieves the results from all Language Learning Models (LLMs) using the default prompt.
        """
        consolidated_result_list = []
        generator_list = await self._send_prompt_to_all_llm_default()
        for generator in generator_list:
            async for result in generator:
                consolidated_result_list.append(result)
        return consolidated_result_list

    async def perform_attack_manually(self) -> list:
        """
        Asynchronously performs the attack manually. The user will need to pass in a list of prompts and
        the LLM connector endpoint to send the prompts to. In this example, there is a for loop to send the
        list of prepared prompts to all the LLM connectors defined.

        This method prepares prompts for each target Language Learning Model (LLM) using the provided prompt
        and sends them to the respective LLMs.
        """
        result_list = []
        for target_llm_connector in self.connector_instances:
            gen_prompts_generator = self._generate_prompts(
                self.prompt, target_llm_connector.id
            )
            prepared_prompts = [
                prepared_prompt.connector_prompt.prompt
                async for prepared_prompt in gen_prompts_generator
            ]
            result_list.append(
                await self._send_prompt_to_single_llm(
                    prepared_prompts, target_llm_connector
                )
            )
        return result_list
