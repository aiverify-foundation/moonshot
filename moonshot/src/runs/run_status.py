from enum import Enum


class RunStatus(Enum):
    """
    Enumeration for the status of a run.

    This enum class defines the possible states a run can be in during its lifecycle.
    Each status represents a distinct phase or condition of the run's execution.

    Attributes:
        PENDING (str): The run is awaiting execution.
        RUNNING (str): The run is currently in progress.
        RUNNING_BENCHMARK (str): The run is currently benchmarking.
        COMPLETED_BENCHMARK (str): The run has completed benchmarking.
        RUNNING_FORMAT_RESULTS (str): The run is formatting results.
        COMPLETED_FORMAT_RESULTS (str): The run has completed formatting results.
        RUNNING_WITH_ERRORS (str): The run is running but has encountered errors.
        COMPLETED (str): The run has finished successfully without errors.
        COMPLETED_WITH_ERRORS (str): The run has finished but encountered errors during execution.
        CANCELLED (str): The run has been cancelled before completion.
    """

    PENDING = "pending"  # The run is awaiting execution.
    RUNNING = "running"  # The run is currently in progress.

    RUNNING_BENCHMARK = "running_benchmark"  # The run is currently benchmarking.
    COMPLETED_BENCHMARK = "completed_benchmark"  # The run has completed benchmarking.

    RUNNING_FORMAT_RESULTS = "running_format_results"  # The run is formatting results.
    COMPLETED_FORMAT_RESULTS = (
        "completed_format_results"  # The run has completed formatting results.
    )

    RUNNING_WITH_ERRORS = (
        "running_with_errors"  # The run is running but has encountered errors.
    )

    COMPLETED = "completed"  # The run has finished successfully without errors.
    COMPLETED_WITH_ERRORS = "completed_with_errors"  # The run has finished but encountered errors during execution.

    CANCELLED = "cancelled"  # The run has been cancelled before completion.
