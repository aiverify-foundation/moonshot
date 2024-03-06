from enum import Enum


class BenchmarkExecutorStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    RUNNING_WITH_ERRORS = "running_with_errors"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
