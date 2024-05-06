from __future__ import annotations

from pathlib import Path

from pydantic.v1 import validate_arguments

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.import_modules import get_instance


class ReportAnalysis:
    @classmethod
    def load(cls, report_analysis_module_id: str) -> ReportAnalysis:
        """
        Loads a report analysis module instance by its ID.

        This method attempts to load a report analysis module instance using the provided ID.
        If the report analysis module instance is found, it is instantiated and returned.
        If the report analysis module instance does not exist, a RuntimeError is raised.

        Args:
            report_analysis_module_id (str): The unique identifier of the report analysis module to be retrieved.

        Returns:
            ReportAnalysis: The instantiated report analysis module.

        Raises:
            RuntimeError: If the report analysis module instance cannot be found or instantiated.
        """
        ra_instance = get_instance(
            report_analysis_module_id,
            Storage.get_filepath(
                EnvVariables.REPORTS_ANALYSIS_MODULES.name,
                report_analysis_module_id,
                "py",
            ),
        )
        if ra_instance:
            return ra_instance()
        else:
            raise RuntimeError(
                f"Unable to get defined report analysis instance - {report_analysis_module_id}"
            )

    @staticmethod
    @validate_arguments
    def delete(report_analysis_module_id: str) -> None:
        """
        Deletes a report analysis module by its ID.

        This method attempts to delete the report analysis module file associated with the given ID.
        If the deletion fails, it prints an error message and raises the exception.

        Args:
            report_analysis_module_id (str): The unique identifier of the report analysis module to be deleted.

        Raises:
            Exception: If the deletion fails.
        """
        try:
            Storage.delete_object(
                EnvVariables.REPORTS_ANALYSIS_MODULES.name,
                report_analysis_module_id,
                "py",
            )

        except Exception as e:
            print(f"Failed to delete report analysis module: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> list[str]:
        """
        Retrieves a list of available report analysis module IDs.

        This method fetches all report analysis module files from the storage and filters out any special files
        (e.g., files starting with "__" which are typically Python internal or special files).
        It then extracts and returns the stem (filename without extension) of each report analysis module file
        as a list.

        Returns:
            list[str]: A list of report analysis module IDs.

        Raises:
            Exception: If there is an error retrieving the report analysis module IDs.
        """
        try:
            retn_reports_analysis_module_ids = []
            reports_analysis_module_ids = Storage.get_objects(
                EnvVariables.REPORTS_ANALYSIS_MODULES.name, "py"
            )
            for report_analysis_module_id in reports_analysis_module_ids:
                if "__" in report_analysis_module_id:
                    continue
                retn_reports_analysis_module_ids.append(
                    Path(report_analysis_module_id).stem
                )
            return retn_reports_analysis_module_ids
        except Exception as e:
            print(f"Failed to get available report analysis modules: {str(e)}")
            raise e
