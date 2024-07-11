from moonshot.src.utils.timeit import timeit

from .logger_mock import LoggerMock


class TestCollectionTimeitMethod:
    def test_time_class_method(self, mocker):
        """
        Tests the `timeit` decorator to ensure it correctly logs the execution time of a class method.

        This test function uses a custom LoggerMock to intercept logging calls made by the `timeit` decorator.
        It patches the logger in the `timeit` module to use this mock logger, then executes a dummy function
        decorated with `@timeit` to trigger the logging. Finally, it asserts that the correct logging calls were made,
        indicating the decorator functioned as expected.

        Args:
            mocker: A fixture provided by pytest-mock to patch objects for testing.

        """
        # Instantiate your custom logger mock
        mock_logger = LoggerMock()

        # Patch the logger object in the timeit module with your custom mock
        mocker.patch("moonshot.src.utils.timeit.logger", mock_logger)

        # Example function to test
        @timeit
        def dummy_function():
            pass

        # Call the function to trigger the logger
        dummy_function()

        # Assert that your custom logger was used. For example, check if debug was called.
        assert mock_logger.messages["debug"] == [
            "[src.test_timeit] Running [dummy_function] took 0.0000s"
        ]
        assert mock_logger.messages["info"] == []
        assert mock_logger.messages["warning"] == []
        assert mock_logger.messages["error"] == []
