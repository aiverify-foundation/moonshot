from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors_endpoints.connector_endpoint import ConnectorEndpoint
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

        # create toxic llm connector
        toxic_llm_endpoint = "my-openai-gpt4"
        toxic_llm_connector = Connector.create(
            ConnectorEndpoint.read(toxic_llm_endpoint)
        )

        try:
            print("=" * 200)
            if toxic_llm_connector:
                print(
                    f"Preparing prompts and sending prompts to toxic generator LLM - ({toxic_llm_connector.id})"
                )
                toxic_prompt_generator = self._generate_predictions(
                    self._generate_prompts(), toxic_llm_connector
                )
                toxic_prompts = [result async for result in toxic_prompt_generator]

                # send toxic prompts to all LLMs in the session
                iteration_count = 1
                for toxic_prompt in toxic_prompts:
                    print(
                        f"Iteration: {iteration_count}. Sending toxic prompt [{toxic_prompt}] to target LLMs."
                    )
                    for target_llm_connector in self.connector_instances:
                        print("=" * 200)
                        print(
                            f"Sending prompt to Target LLM [{target_llm_connector.id}]\n"
                        )
                        result = await self.send_prompt(
                            target_llm_connector,
                            toxic_prompt.connector_prompt.predicted_results,
                        )
                        print(
                            f'Response from Target LLM [{target_llm_connector.id}] -> prompt ["{result}"]'
                        )
                        if self.check_stop_condition(
                            toxic_prompt.connector_prompt.predicted_results, result
                        ):
                            return ""

                    # hit soft cap
                    if iteration_count >= self.get_max_no_iterations():
                        print(
                            "Maximum number of iterations hit. Stopping red teaming..."
                        )
                        break
                print(
                    "There is no more data in the dataset to send. Stopping red teaming..."
                )

        except Exception as e:
            print(f"Unable to carry out red teaming attack: {str(e)}")

    def check_stop_condition(self, prompt: str, predicted_results: str) -> bool:
        for metric in self.metric_instances:
            metric_score_dict = metric.get_results([prompt], [predicted_results], [])
            metric_key = "exact_str_match"
            expected_metric_score = 1
            metric_score = metric_score_dict.get(metric_key, None)
            print(
                f"Expected {metric_key} score: {expected_metric_score}. Current metric score: {metric_score}."
            )
            if metric_score >= expected_metric_score:
                print(
                    "Red teaming condition has been fulfilled. Stopping red teaming..."
                )
                return True
        return False
