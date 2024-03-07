import logging
from typing import Any, Callable
from pydantic import ValidationError

class SessionException(Exception):
    error_code: str
    msg: str

    def __init__(self, msg: str, method_name: str, error_code: str = 'UnknownSessionError'):
        self.error_code = error_code
        message = f"[SessionException] {error_code} in {method_name} - {msg}"
        self.msg = message 
        super().__init__(message)
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.logger.error(msg);

def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise SessionException(f"A file not found error occurred: {e}", func.__name__, "FileNotFound")
        except ValidationError as e:
            raise SessionException(f"A validation error occurred: {e}", func.__name__, "ValidationError")
        except Exception as e:
            raise SessionException(f"An unexpected error occurred: {e}", func.__name__, "UnexpectedError")
    return wrapper
