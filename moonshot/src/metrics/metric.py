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
    def get_available_items() -> tuple[list[str], list[Metric]]:
        """
        Retrieves all available metric IDs and their corresponding instances.

        This method searches the storage location specified by `EnvVariables.METRICS` for metric files, omitting any
        that include "__" in their filenames. It loads each valid metric file to create a metric instance and
        accumulates the metric IDs and the corresponding metric instances into separate lists, which are then returned
        together as a tuple.

        Returns:
            tuple[list[str], list[Metric]]: A tuple containing two elements. The first is a list of metric IDs, and the
            second is a list of Metric instances, each representing a loaded metric.

        Raises:
            Exception: If any issues arise during the retrieval and processing of metric files.
        """
        try:
            retn_mets = []
            retn_mets_ids = []

            mets = Storage.get_objects(EnvVariables.METRICS.name, "py")
            for met in mets:
                if "__" in met:
                    continue

                retn_mets.append(Metric.load(Path(met).stem))
                retn_mets_ids.append(Path(met).stem)

            return retn_mets_ids, retn_mets

        except Exception as e:
            print(f"Failed to get available metrics: {str(e)}")
            raise e
