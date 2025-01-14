from enum import Enum


class TaskStatus(Enum):
    """
    Enumeration for the status of a benchmarking task.

    This enum class defines the possible states a benchmarking task can be in during its lifecycle.
    Each status represents a distinct phase or condition of the task's execution.

    Attributes:
        PENDING (str): The task is awaiting execution.
        CANCELLED (str): The task has been cancelled before completion.
        RUNNING (str): The task is currently in progress.
        RUNNING_PROMPT_PROCESSING (str): The task is processing prompts.
        COMPLETED_PROMPT_PROCESSING (str): The task has completed processing prompts.
        COMPLETED (str): The task has finished successfully without errors.
        COMPLETED_WITH_ERRORS (str): The task has finished but encountered errors during execution.
    """

    PENDING = "pending"  # The task is awaiting execution
    RUNNING = "running"  # The task is currently in progress

    RUNNING_PROMPT_PROCESSING = (
        "running_prompt_processing"  # The task is processing prompts
    )
    COMPLETED_PROMPT_PROCESSING = (
        "completed_prompt_processing"  # The task has completed processing prompts
    )

    COMPLETED = "completed"  # The task has finished successfully without errors
    COMPLETED_WITH_ERRORS = "completed_with_errors"  # The task has finished but encountered errors during execution

    CANCELLED = "cancelled"  # The task has been cancelled before completion
