from enum import Enum


class BenchmarkExecutorStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    RUNNING_WITH_ERRORS = "running-with-errors"
    COMPLETED = "completed"
