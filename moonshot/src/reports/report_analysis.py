from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class ReportAnalysis:
    @classmethod
    def load(cls, ra_id: str) -> ReportAnalysis:
        """
        Retrieves a report analysis instance by its ID.

        This method attempts to load a report analysis instance using the provided ID.
        If the report analysis instance is found, it is returned.
        If the report analysis instance does not exist, a RuntimeError is raised.

        Args:
            ra_id (str): The unique identifier of the report analysis to be retrieved.

        Returns:
            ReportAnalysis: The retrieved report analysis instance.

        Raises:
            RuntimeError: If the report analysis instance does not exist.
        """
        ra_instance = get_instance(
            ra_id,
            Storage.get_filepath(
                EnvVariables.REPORTS_ANALYSIS_MODULES.name, ra_id, "py"
            ),
        )
        if ra_instance:
            return ra_instance()
        else:
            raise RuntimeError(
                f"Unable to get defined report analysis instance - {ra_id}"
            )

    @staticmethod
    @validate_arguments
    def delete(ra_id: str) -> None:
        """
        Removes a report analysis module using its ID.

        This function removes a report analysis module using its ID.
        It initially verifies if the module instance is present.
        If present, it removes the instance and returns None.
        If not present, it throws a RuntimeError.

        Args:
            ra_id (str): The ID of the report analysis module to be removed.

        Returns:
            None

        Raises:
            RuntimeError: If the report analysis module instance is not found.
        """
        try:
            Storage.delete_object(
                EnvVariables.REPORTS_ANALYSIS_MODULES.name, ra_id, "py"
            )

        except Exception as e:
            print(f"Failed to delete report analysis module: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> list[str]:
        """
        Fetches the list of all available report analysis modules.

        This method uses the `get_objects` method from the Storage class to obtain all Python files in the directory
        defined by the `EnvVariables.REPORTS_ANALYSIS_MODULES.name` environment variable.
        It then excludes any files that are not intended to be exposed as modules (those containing "__" in their names)
        The method returns a list of the names of these modules.

        Returns:
            list[str]: A list of strings, each denoting the name of a report analysis module.

        Raises:
            Exception: If an error occurs during the extraction of report analysis modules.
        """
        try:
            retn_ras_ids = []

            ras = Storage.get_objects(EnvVariables.REPORTS_ANALYSIS_MODULES.name, "py")
            for ra in ras:
                if "__" in ra:
                    continue

                retn_ras_ids.append(Path(ra).stem)

            return retn_ras_ids

        except Exception as e:
            print(f"Failed to get available report analysis modules: {str(e)}")
            raise e
