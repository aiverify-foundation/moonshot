from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class ReportModule:
    @classmethod
    def load(cls, report_module_id: str) -> ReportModule:
        """
        Loads a report module instance by its ID.

        This method attempts to load a report module instance using the provided ID.
        If the report module instance is found, it is instantiated and returned.
        If the report module instance does not exist, a RuntimeError is raised.

        Args:
            report_module_id (str): The unique identifier of the report module to be retrieved.

        Returns:
            ReportModule: The instantiated report module.

        Raises:
            RuntimeError: If the report module instance cannot be found or instantiated.
        """
        report_module_instance = get_instance(
            report_module_id,
            Storage.get_filepath(
                EnvVariables.REPORTS_MODULES.name, report_module_id, "py"
            ),
        )
        if report_module_instance:
            return report_module_instance()
        else:
            raise RuntimeError(
                f"Unable to get defined report module instance - {report_module_id}"
            )

    @staticmethod
    @validate_arguments
    def delete(report_module_id: str) -> None:
        """
        Deletes a report module by its ID.

        This method attempts to delete the report module file associated with the given ID.
        If the deletion fails, it prints an error message and raises the exception.

        Args:
            report_module_id (str): The unique identifier of the report module to be deleted.

        Raises:
            Exception: If the deletion fails.
        """
        try:
            Storage.delete_object(
                EnvVariables.REPORTS_MODULES.name, report_module_id, "py"
            )
        except Exception as e:
            print(f"Failed to delete report module: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> list[str]:
        """
        Retrieves a list of available report module IDs.

        This method fetches all report module files and filters out any special files (e.g., __init__.py).
        It then extracts and returns the stem (filename without extension) of each report module file as a list.

        Returns:
            list[str]: A list of report module IDs.

        Raises:
            Exception: If there is an error retrieving the report module IDs.
        """
        try:
            retn_reports_module_ids = []
            report_module_ids = Storage.get_objects(
                EnvVariables.REPORTS_MODULES.name, "py"
            )
            for report_module_id in report_module_ids:
                if "__" in report_module_id:
                    continue
                retn_reports_module_ids.append(Path(report_module_id).stem)
            return retn_reports_module_ids
        except Exception as e:
            print(f"Failed to get available report modules: {str(e)}")
            raise e
