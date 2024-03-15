from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from pydantic.v1 import validate_arguments

from moonshot.src.storage.storage_manager import StorageManager
from moonshot.src.utils.import_modules import (
    create_module_spec,
    import_module_from_spec,
)


class Metric:
    @classmethod
    def load_metric(cls, met_id: str) -> Metric:
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
        metric_instance = cls._get_metric_instance(met_id)
        if metric_instance:
            return metric_instance()
        else:
            raise RuntimeError(f"Unable to get defined metric instance - {met_id}")

    @staticmethod
    @validate_arguments
    def delete_metric(met_id: str) -> None:
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
    def get_available_metrics() -> list[str]:
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

    @staticmethod
    def _get_metric_instance(met_id: str) -> Any:
        """
        Retrieves the instance of the metric class.

        This method retrieves the instance of the metric class by calling the `create_module_spec` method with the
        metric ID and the file path of the metric.

        It then checks if the module specification exists. If it does, it imports the module and iterates through
        the attributes of the module.

        For each attribute, it gets the attribute object and checks if the attribute is a class and if it has the
        same module name as the metric ID.

        If it does, it returns the attribute object.

        Args:
            met_id (str): The ID of the metric.

        Returns:
            Any: The instance of the metric class if found, else None.

        Raises:
            None
        """
        # Create the module specification
        module_spec = create_module_spec(
            met_id,
            StorageManager.get_metric_filepath(met_id),
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
                if inspect.isclass(obj) and obj.__module__ == met_id:
                    return obj

        # Return None if no instance of the metric class is found
        return None
