from moonshot.src.redteaming.attack.attack_module import AttackModule
from moonshot.src.redteaming.attack.attack_module_arguments import AttackModuleArguments


class SampleAttackModule(AttackModule):
    def __init__(self, am_arguments: AttackModuleArguments):
        # Initialize super class
        super().__init__(am_arguments)

    async def execute(self):
        """
        Asynchronously executes the attack module.

        This method loads the dataset contents using the `load_dataset_contents` method,
        processes the dataset through a prompt template, retrieves the connector to the first
        Language Learning Model (LLM) and sends the processed dataset as a prompt to the LLM.
        """
        # prepares prompt or dataset to send to LLM
        prepared_prompt = self.prepare_prompt()

        # gets the required LLM connectors to send the prompts to
        toxic_llm_connector = next(
            (
                conn_inst
                for conn_inst in self.connector_instances
                if conn_inst.id == "my-openai-gpt35"
            ),
            None,
        )
        target_llm_connector = next(
            (
                conn_inst
                for conn_inst in self.connector_instances
                if conn_inst.id == "my-openai-gpt4"
            ),
            None,
        )

        # gets the toxic prompts from toxic LLM and send to target LLM
        if toxic_llm_connector and target_llm_connector:
            # maximum no. of prompts to be sent to the LLM to in case the stop condition does not get fulfilled
            for iteration_count in range(self.get_max_no_iterations()):
                toxic_llm_response = await self.send_prompt(
                    toxic_llm_connector, prepared_prompt
                )
                target_llm_response = await self.send_prompt(
                    target_llm_connector, toxic_llm_response
                )
                if self.check_stop_condition(
                    toxic_llm_response,
                    iteration_count,
                    target_llm_response,
                    self.metric_instances,
                ):
                    return toxic_llm_response
