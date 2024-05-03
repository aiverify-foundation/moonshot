from abc import abstractmethod


class ReportModuleInterface:
    @abstractmethod
    def get_metadata(self) -> dict | None:
        """
        Retrieves the metadata for the report module.

        This method is intended to be implemented by subclasses to return a dictionary
        containing metadata about the report module. If no metadata is available, it should
        return None.

        Returns:
            dict | None: A dictionary containing metadata, or None if not available.
        """
        pass

    @abstractmethod
    def generate_report(self, report_args: dict) -> dict | None:
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
        pass
