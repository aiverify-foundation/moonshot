from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class Metric:
    @classmethod
    def load(cls, met_id: str) -> Metric:
        """
        Retrieves a metric instance by its ID.

        This method attempts to load a metric instance using the provided ID. If the metric instance is found,
        it is returned. If the metric instance does not exist, a RuntimeError is raised.

        Args:
            met_id (str): The unique identifier of the metric to be retrieved.

        Returns:
            Metric: The retrieved metric instance.

        Raises:
            RuntimeError: If the metric instance does not exist.
        """
        metric_instance = get_instance(
            met_id,
            Storage.get_filepath(EnvVariables.METRICS.name, met_id, "py"),
        )
        if metric_instance:
            return metric_instance()
        else:
            raise RuntimeError(f"Unable to get defined metric instance - {met_id}")

    @staticmethod
    @validate_arguments
    def delete(met_id: str) -> None:
        """
        Removes a metric using its ID.

        This function removes a metric using its ID. It initially verifies if the metric instance is present.
        If present, it removes the instance and returns None.
        If not present, it throws a RuntimeError.

        Args:
            met_id (str): The ID of the metric to be removed.

        Returns:
            None

        Raises:
            RuntimeError: If the metric instance is not found.
        """
        try:
            Storage.delete_object(EnvVariables.METRICS.name, met_id, "py")

        except Exception as e:
            print(f"Failed to delete metric: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> list[str]:
        """
        Fetches the list of all available metrics.

        This method uses the `get_objects` method from the StorageManager to obtain all Python files in the directory
        defined by the `EnvVariables.METRICS.name` environment variable. It then excludes any files that are
        not intended to be exposed as metrics (those containing "__" in their names). The method returns a list of the
        names of these metrics.

        Returns:
            list[str]: A list of strings, each denoting the name of a metric.

        Raises:
            Exception: If an error occurs during the extraction of metrics.
        """
        try:
            retn_mets_ids = []

            mets = Storage.get_objects(EnvVariables.METRICS.name, "py")
            for met in mets:
                if "__" in met:
                    continue

                retn_mets_ids.append(Path(met).stem)

            return retn_mets_ids

        except Exception as e:
            print(f"Failed to get available metrics: {str(e)}")
            raise e
