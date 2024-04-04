from enum import Enum


class RunStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    RUNNING_WITH_ERRORS = "running_with_errors"
    CANCELLED = "cancelled"
    CANCELLED_WITH_ERRORS = "cancelled_with_errors"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
