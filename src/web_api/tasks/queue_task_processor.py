import time


class QueueTaskProcessor:
    @staticmethod
    def process_task(task):
        # Example: perform calculation / tests etc
        # Replace this with actual processing logic
        return QueueTaskProcessor.run_benchmark_test(task)

    @staticmethod
    def run_benchmark_test(task):
        print(f"Running test for: {task}")
        time.sleep(10)  # Simulate test time
        return {"task": task, "data": "Mock"}
