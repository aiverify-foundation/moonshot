from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.storage.storage_manager import StorageManager
from moonshot.src.utils.import_modules import get_instance


class Metric:
    @classmethod
    def load(cls, met_id: str) -> Metric:
        """
        Loads a metric by its ID.

        This method loads a metric by its ID. It first checks if the metric instance exists.
        If it does, it returns the instance.
        If it doesn't, it raises a RuntimeError.

        Args:
            met_id (str): The ID of the metric to load.

        Returns:
            Metric: The loaded metric instance.

        Raises:
            RuntimeError: If the metric instance cannot be found.
        """
        metric_instance = get_instance(
            met_id, StorageManager.get_metric_filepath(met_id)
        )
        if metric_instance:
            return metric_instance()
        else:
            raise RuntimeError(f"Unable to get defined metric instance - {met_id}")

    @staticmethod
    @validate_arguments
    def delete(met_id: str) -> None:
        """
        Deletes a metric by its ID.

        This method deletes a metric by its ID. It first checks if the metric instance exists.
        If it does, it deletes the instance and returns None.
        If it doesn't, it raises a RuntimeError.

        Args:
            met_id (str): The ID of the metric to delete.

        Returns:
            None

        Raises:
            RuntimeError: If the metric instance cannot be found.
        """
        try:
            StorageManager.delete_metric(met_id)

        except Exception as e:
            print(f"Failed to delete metric: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> list[str]:
        """
        Retrieves the list of available metrics.

        This method retrieves the list of available metrics by calling the `get_metrics` method of the `StorageManager`.
        It filters out any metrics that are not intended to be used (those with "__" in their names), and returns
        the list of metric IDs.

        Returns:
            list[str]: A list of available metric IDs.

        Raises:
            Exception: If there is an error in retrieving the metrics.
        """
        try:
            retn_mets_ids = []

            mets = StorageManager.get_metrics()
            for met in mets:
                if "__" in met:
                    continue

                retn_mets_ids.append(Path(met).stem)

            return retn_mets_ids

        except Exception as e:
            print(f"Failed to get available metrics: {str(e)}")
            raise e
