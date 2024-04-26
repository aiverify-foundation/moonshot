from abc import abstractmethod
from typing import Any

from moonshot.src.utils.timeit import timeit


class MetricInterface:
    @abstractmethod
    @timeit
    def get_metadata(self) -> dict | None:
        """
        Abstract method to retrieve metadata from a report.

        Returns:
            dict | None: Returns a dictionary containing the metadata of the report, or None if the operation was
            unsuccessful.
        """
        pass

    @abstractmethod
    def get_results(
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
