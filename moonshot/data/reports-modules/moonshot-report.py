from moonshot.src.reports.report_module_interface import ReportModuleInterface
from moonshot.src.utils.timeit import timeit


class MoonshotReport(ReportModuleInterface):
    def __init__(self) -> None:
        self.id = "moonshot-report"
        self.name = "Moonshot Report"
        self.description = (
            "This report provides an in-depth analysis and summary of the run."
        )

    @timeit
    def get_metadata(self) -> dict | None:
        """
        Retrieves the metadata for the report module.

        This method is intended to be implemented by subclasses to return a dictionary
        containing metadata about the report module. If no metadata is available, it should
        return None.

        Returns:
            dict | None: A dictionary containing metadata, or None if not available.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    @timeit
    def generate(self, report_args: dict) -> dict | None:
        """
        Generates a report based on the provided arguments.

        This method is intended to be implemented by subclasses to create a report
        based on the given arguments. The report should be returned as a dictionary.
        If the report cannot be generated, it should return None.

        Args:
            report_args (dict): A dictionary of arguments used for generating the report.

        Returns:
            dict | None: A dictionary representing the generated report, or None if it cannot be generated.
        """
        # ------------------ PART 1 ------------------
        # Get required arguments
        if report_args.get("run_args"):
            run_args = report_args["run_args"]
            print(run_args)
        else:
            raise RuntimeError("[MLCReport] Failed to get required arguments.")
