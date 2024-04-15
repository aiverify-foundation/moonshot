from abc import abstractmethod

from jsonschema import ValidationError, validate

from moonshot.src.utils.timeit import timeit


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

    @timeit
    def validate_output(self, output: dict, output_schema: dict) -> bool:
        """
        Validates the output against a specified JSON schema to ensure it adheres to the expected structure and
        data types.

        Args:
            output (dict): The output data that needs validation.
            output_schema (dict): The JSON schema the output data is validated against.

        Returns:
            bool: Returns True if the output conforms to the schema, False if it does not.
        """
        try:
            validate(instance=output, schema=output_schema)
            return True
        except ValidationError as e:
            print(f"Validation Error: {e}")
            return False
