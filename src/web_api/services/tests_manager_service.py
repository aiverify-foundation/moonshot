import uuid

class TestsManagerService:
    def __init__(self):
        self.benchmarking_tests = {}

    def add_test(self, test: dict[str, Any]) -> str:
        test_id = str(uuid.uuid4())
        self.benchmarking_tests[test_id] = test

