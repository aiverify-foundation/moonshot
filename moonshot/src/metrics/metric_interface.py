from abc import abstractmethod
from typing import Any

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger
from moonshot.src.utils.timeit import timeit

# Create a logger for this module
logger = configure_logger(__name__)


class MetricInterface:
    config_name = "metrics_config"
    config_extension = "json"

    @abstractmethod
    @timeit
    def get_metadata(self) -> dict | None:
        """
        Abstract method to retrieve metadata from a metric class.

        Returns:
            dict | None: Returns a dictionary containing the metadata of the metric class, or None if the operation was
            unsuccessful.
        """
        pass

    @abstractmethod
    async def get_results(
        self, prompts: Any, predicted_results: Any, targets: Any, *args, **kwargs
    ) -> dict:
        """
        Abstract method to compute metrics based on model predictions.

        This method is intended to be implemented by subclasses to calculate specific
        metrics (e.g., accuracy, BLEU score) based on the inputs provided.
        It should handle any necessary preprocessing of inputs, computation of the metric, and formatting of the output.

        Args:
            prompts (Any): The input prompts used to generate the predictions.
            The exact type and format will depend on the specific implementation and the nature of the
            task (e.g., text, images).

            predicted_results (Any): The model's predictions in response to the prompts.
            The type and format should align with the prompts and the expected output of the model.

            targets (Any): The ground truth targets against which the predicted results will be evaluated.

            *args: Variable length argument list for additional parameters that might be required for specific metric
            computations.

            **kwargs: Arbitrary keyword arguments for additional options or configuration settings that might be
            required for specific metric computations.

        Returns:
            dict: A dictionary containing the computed metric(s). The keys should clearly indicate the metric being
            reported, and the values should be the corresponding metric values.
        """
        pass

    def get_metrics_configuration(self, met_id: str) -> dict:
        """
        Retrieves the configuration for a specific metric by its identifier.

        Args:
            met_id (str): The identifier for the metric configuration to retrieve.

        Returns:
            dict: The metric configuration as a dictionary. Returns an empty dict if the configuration is not found.

        Raises:
            Exception: If reading the metrics configuration fails or if the configuration cannot be created.
        """
        try:
            obj_results = Storage.read_object(
                EnvVariables.METRICS.name, "metrics_config", "json"
            )
            return obj_results.get(met_id, {})

        except Exception as e:
            logger.warning(
                f"[MetricInterface] Failed to read metrics configuration: {str(e)}"
            )
            logger.info("Attempting to create empty metrics configuration...")
            try:
                Storage.create_object(
                    obj_type=EnvVariables.METRICS.name,
                    obj_id="metrics_config",
                    obj_info={},
                    obj_extension="json",
                )
                # After creation, attempt to read it again to ensure it was created successfully
                obj_results = Storage.read_object(
                    EnvVariables.METRICS.name, "metrics_config", "json"
                )
                return obj_results.get(met_id, {})
            except Exception as e:
                raise Exception(
                    f"[MetricInterface] Failed to create metrics configuration: {str(e)}"
                )
