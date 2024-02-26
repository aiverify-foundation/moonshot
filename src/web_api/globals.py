from multiprocessing.managers import DictProxy
from queue import Queue
from .queue.queue_manager import QueueManager


# Initialize SHARED_CHANNELS as an empty dictionary.
# SHARED_CHANNELS: DictProxy[str, Queue] | None = None

BENCHMARK_TEST_QUEUE_MANAGER: QueueManager | None = None

