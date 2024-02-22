from multiprocessing.managers import DictProxy
from queue import Queue


# Initialize SHARED_CHANNELS as an empty dictionary.
SHARED_CHANNELS: DictProxy[str, Queue] | None = None

