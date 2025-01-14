from enum import Enum


class PromptStatus(Enum):
    """
    Enumeration for the status of a benchmarking prompt.

    This enum class defines the possible states a benchmarking prompt can be in during its lifecycle.
    Each status represents a distinct phase or condition of the prompt's execution.

    Attributes:
        PENDING (str): The prompt is awaiting execution.
        CANCELLED (str): The prompt has been cancelled before completion.
        RUNNING (str): The prompt is currently in progress.
        RUNNING_QUERY_CONNECTOR (str): The prompt is querying the connector.
        RUNNING_METRICS_EVALUATION (str): The prompt is evaluating metrics.
        COMPLETED (str): The prompt has finished successfully without errors.
        COMPLETED_QUERY_CONNECTOR (str): The prompt has successfully completed querying the connector.
        COMPLETED_METRICS_EVALUATION (str): The prompt has successfully completed evaluating metrics.
        COMPLETED_WITH_ERRORS (str): The prompt has completed but encountered some errors.
    """

    PENDING = "pending"  # The prompt is awaiting execution
    RUNNING = "running"  # The prompt is currently in progress

    RUNNING_QUERY_CONNECTOR = (
        "running_query_connector"  # The prompt is querying the connector
    )
    COMPLETED_QUERY_CONNECTOR = "completed_query_connector"  # The prompt has successfully completed querying the connector  # noqa: E501

    RUNNING_METRICS_EVALUATION = (
        "running_metrics_evaluation"  # The prompt is evaluating metrics
    )
    COMPLETED_METRICS_EVALUATION = "completed_metrics_evaluation"  # The prompt has successfully completed evaluating metrics  # noqa: E501

    COMPLETED = "completed"  # The prompt has finished successfully without errors
    COMPLETED_WITH_ERRORS = (
        "completed_with_errors"  # The prompt has completed but encountered some errors
    )

    CANCELLED = "cancelled"  # The prompt has been cancelled before completion
