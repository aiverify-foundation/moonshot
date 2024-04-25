from enum import Enum


class RunStatus(Enum):
    PENDING = "pending"
    CANCELLED = "cancelled"
    RUNNING = "running"
    RUNNING_WITH_ERRORS = "running_with_errors"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
