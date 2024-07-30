import os
from pathlib import Path
import pytest
import logging

from moonshot.src.utils.log import configure_logger

class TestCollectionLog:

    @pytest.mark.parametrize(
        "log_name,expected_log_name",
        [
            ("my_logger","my_logger"),
            ("my-logger","my-logger"),
            ("mylogger","mylogger"),
            (None,"log"),
            ("None","None"),
            ("","log"),
            ({},"log"),
            ([],"log"),
            (123,"log"),
        ],
    )
    def test_configure_logger(self, log_name, expected_log_name):
        output_logger = configure_logger(log_name)
        assert output_logger.name == expected_log_name
        stream_handler = next((handler for handler in output_logger.handlers if isinstance(handler, logging.StreamHandler)), None)
        assert stream_handler is not None
        assert stream_handler.formatter._fmt == "%(asctime)s [%(levelname)s][%(filename)s::%(funcName)s(%(lineno)d)] %(message)s"

        # Clear the handlers
        for handler in output_logger.handlers[:]:
            output_logger.removeHandler(handler)
            handler.close()
        assert len(output_logger.handlers) == 0

    @pytest.mark.parametrize(
        "environ_value,expected_log_level",
        [
            ({"MS_LOG_LEVEL": "DEBUG"}, logging.DEBUG),
            ({"MS_LOG_LEVEL": "INFO"}, logging.INFO),
            ({"MS_LOG_LEVEL": "WARNING"}, logging.WARNING),
            ({"MS_LOG_LEVEL": "ERROR"}, logging.ERROR),
            ({"MS_LOG_LEVEL": "CRITICAL"}, logging.INFO),
            ({"MS_LOG_LEVEL": "INVALID"}, logging.INFO),
        ],
    )
    def test_configure_logger_log_level(self, mocker, environ_value, expected_log_level):
        mocker.patch.dict(os.environ, environ_value)
        output_logger = configure_logger("my_logger")
        assert output_logger.level == expected_log_level

        # Clear the handlers
        for handler in output_logger.handlers[:]:
            output_logger.removeHandler(handler)
            handler.close()
        assert len(output_logger.handlers) == 0

    @pytest.mark.parametrize(
        "environ_value,expected_log_file",
        [
            ({"MS_LOG_TO_FILE": "false"}, False),
            ({"MS_LOG_TO_FILE": "true"}, True),
            ({"MS_LOG_TO_FILE": "invalid_value"}, False),
        ],
    )
    def test_configure_logger_log_to_file(self, mocker, environ_value, expected_log_file):
        mocker.patch.dict(os.environ, environ_value)
        output_logger = configure_logger("my_logger")
        # Assert that the file handler is not added to the logger
        if expected_log_file:
            file_handler = next((handler for handler in output_logger.handlers if isinstance(handler, logging.FileHandler)), None)

            # Remove the log file
            if file_handler:
                Path(file_handler.baseFilename).unlink(missing_ok=True)
            else:
                assert False
        else:
            assert not any(isinstance(handler, logging.FileHandler) for handler in output_logger.handlers)
        
        # Clear the handlers
        for handler in output_logger.handlers[:]:
            output_logger.removeHandler(handler)
            handler.close()
        assert len(output_logger.handlers) == 0

    @pytest.mark.parametrize(
        "environ_value,expected_log_name",
        [
            ({"MS_LOG_NAME": "my_logger","MS_LOG_TO_FILE": "true"}, "my_logger"),
            ({"MS_LOG_NAME": "my-logger","MS_LOG_TO_FILE": "true"}, "my-logger"),
            ({"MS_LOG_NAME": "mylogger","MS_LOG_TO_FILE": "true"}, "mylogger"),
            ({"MS_LOG_NAME": "moonshot!@#$%","MS_LOG_TO_FILE": "true"}, "moonshot!@#$%"),
            ({"MS_LOG_NAME": "None","MS_LOG_TO_FILE": "true"}, "none"),
            ({"MS_LOG_NAME": "","MS_LOG_TO_FILE": "true"}, "moonshot"),
            ({"MS_LOG_NAME": "1234","MS_LOG_TO_FILE": "true"}, "1234"),
        ],
    )
    def test_configure_logger_log_name(self, mocker, environ_value, expected_log_name):
        mocker.patch.dict(os.environ, environ_value)
        output_logger = configure_logger("my_logger")

        file_handler = next((handler for handler in output_logger.handlers if isinstance(handler, logging.FileHandler)), None)
        if file_handler:
            file_path = file_handler.baseFilename
            assert os.path.exists(file_path)
            
            expected_path = str(Path(".").resolve() / (expected_log_name + ".log"))
            assert file_path == expected_path

            # Clear the handlers
            for handler in output_logger.handlers[:]:
                output_logger.removeHandler(handler)
                handler.close()
            assert len(output_logger.handlers) == 0

            # Remove the log file
            Path(expected_path).unlink(missing_ok=True)

        else:
            assert False
