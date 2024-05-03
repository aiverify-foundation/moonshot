from abc import abstractmethod


class ReportAnalysisInterface:
    @abstractmethod
    def get_metadata(self) -> dict | None:
        """
        Abstract method to retrieve metadata from a report.

        Returns:
            dict | None: Returns a dictionary containing the metadata of the report, or None if the operation was
            unsuccessful.
        """
        pass

    @abstractmethod
    def generate_analysis(self, ra_args: dict) -> dict | None:
        """
        Abstract method to generate an analysis from a report.

        Args:
            ra_args (dict): A dictionary of arguments necessary for the analysis.

        Returns:
            dict | None: Returns a dictionary containing the analysis of the report, or None if the operation was
            unsuccessful.
        """
        pass
