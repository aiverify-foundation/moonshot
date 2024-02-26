import time
from typing import Any


class QueueJobWorker:
    @staticmethod
    def process_job(job):
        # Example: perform calculation / tests etc
        # Replace this with actual processing logic
        return QueueJobWorker.run_benchmark_test(job)

    @staticmethod
    def run_benchmark_test(task: dict[str, Any]) -> None:
        print(f"Running test for: {task}")
        time.sleep(10)  # Simulate test time
        return None #{"task": task, "data": "Mock"}
