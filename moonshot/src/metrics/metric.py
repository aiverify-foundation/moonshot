from __future__ import annotations

from pathlib import Path

from pydantic import validate_call

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.metrics.metric_interface import MetricInterface
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class Metric:
    cache_name = "cache"
    cache_extension = "json"

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
    @validate_call
    def delete(met_id: str) -> bool:
        """
        Deletes a metric identified by its unique metric ID.

        This method attempts to delete the metric with the given ID from the storage. If the deletion is successful,
        it returns True. If an exception occurs during the deletion process, it prints an error message and re-raises
        the exception.

        Args:
            met_id (str): The unique identifier of the metric to be deleted.

        Returns:
            bool: True if the metric was successfully deleted.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.METRICS.name, met_id, "py")
            return True

        except Exception as e:
            logger.error(f"Failed to delete metric: {str(e)}")
            raise e

    @staticmethod
    def get_cache_information() -> dict:
        """
        Retrieves cache information from the storage.

        This method attempts to read the cache information from the storage and return it as a dictionary.
        If the cache information does not exist or an error occurs, it returns an empty dictionary.

        Returns:
            dict: A dictionary containing the cache information or an empty dictionary if an error occurs
            or if the cache information does not exist.

        Raises:
            Exception: If there's an error during the retrieval process, it is logged and an
            empty dictionary is returned.
        """
        try:
            # Retrieve cache information from the storage and return it as a dictionary
            cache_info = Storage.read_object(
                EnvVariables.METRICS.name, Metric.cache_name, Metric.cache_extension
            )
            return cache_info if cache_info else {}
        except Exception:
            logger.error(
                f"No previous cache information because {Metric.cache_name} is not found."
            )
            return {}

    @staticmethod
    def write_cache_information(cache_info: dict) -> None:
        """
        Writes the updated cache information to the storage.

        Args:
            cache_info (dict): The cache information to be written.
        """
        try:
            Storage.create_object(
                obj_type=EnvVariables.METRICS.name,
                obj_id=Metric.cache_name,
                obj_info=cache_info,
                obj_extension=Metric.cache_extension,
            )
        except Exception as e:
            logger.error(f"Failed to write cache information: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[dict]]:
        """
        Retrieves a list of available metric names and their corresponding information.

        This method scans the storage for metric objects, filters out any system or cache-related entries,
        and compiles a list of metric names and their detailed information. It also checks the cache for
        any updates and writes back to the cache if necessary.

        Returns:
            tuple[list[str], list[dict]]: A tuple containing two lists, one with the names of the metrics
                                           and the other with the corresponding metric information dictionaries.
        """
        try:
            retn_mets = []
            retn_mets_ids = []
            met_cache_info = Metric.get_cache_information()
            cache_needs_update = False  # Initialize a flag to track cache updates
            mets = Storage.get_objects(EnvVariables.METRICS.name, "py")

            for met in mets:
                if "__" in met or MetricInterface.config_name in met:
                    continue

                met_name = Path(met).stem
                met_info, cache_updated = Metric._get_or_update_metrics_info(
                    met_name, met_cache_info
                )
                if cache_updated:
                    cache_needs_update = True  # Set the flag if any cache was updated

                retn_mets.append(met_info)
                retn_mets_ids.append(met_name)

            if cache_needs_update:  # Check the flag after the loop
                Metric.write_cache_information(met_cache_info)

            return retn_mets_ids, retn_mets

        except Exception as e:
            logger.error(f"Failed to get available metrics: {str(e)}")
            raise e

    @staticmethod
    def _get_or_update_metrics_info(
        met_name: str, met_cache_info: dict
    ) -> tuple[dict, bool]:
        """
        Retrieves or updates the metric information from the cache.

        This method checks if the metric information is already available in the cache and if the file hash matches
        the one stored in the cache. If it does, the information is retrieved from the cache. If not, the metric
        information is read from the storage, the cache is updated with the new information and the new file hash,
        and a flag is set to indicate that the cache has been updated.

        Args:
            met_name (str): The name of the metric.
            met_cache_info (dict): A dictionary containing the cached metric information.

        Returns:
            tuple[dict, bool]: A tuple containing the dictionary with the metric information
                               and a boolean indicating whether the cache was updated or not.
        """
        file_hash = Storage.get_file_hash(EnvVariables.METRICS.name, met_name, "py")
        cache_updated = False

        if met_name in met_cache_info and file_hash == met_cache_info[met_name]["hash"]:
            met_metadata = met_cache_info[met_name].copy()
            met_metadata.pop("hash", None)
        else:
            met_metadata = Metric.load(met_name).get_metadata()  # type: ignore ; ducktyping
            met_cache_info[met_name] = met_metadata.copy()
            met_cache_info[met_name]["hash"] = file_hash
            cache_updated = True

        return met_metadata, cache_updated
