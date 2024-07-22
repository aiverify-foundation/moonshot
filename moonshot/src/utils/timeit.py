import time
from functools import wraps

from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        """
        A decorator function that measures the execution time of the decorated function.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the decorated function.
        """
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.debug(
            f"[{func.__module__}] Running [{func.__name__}] took {total_time:.4f}s"
        )
        return result

    return timeit_wrapper
