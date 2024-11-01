import asyncio


class AtomicInteger:
    def __init__(self, initial: int = 0):
        """
        Initialize an AtomicInteger with an initial value.

        Args:
            initial (int): The initial value of the AtomicInteger. Defaults to 0.
        """
        self.value: int = initial
        self._lock: asyncio.Lock = asyncio.Lock()

    async def increment(self, amount: int = 1) -> None:
        """
        Increment the value by a specified amount.

        Args:
            amount (int): The amount to increment the value by. Defaults to 1.
        """
        async with self._lock:
            self.value += amount

    async def decrement(self, amount: int = 1) -> None:
        """
        Decrement the value by a specified amount.

        Args:
            amount (int): The amount to decrement the value by. Defaults to 1.
        """
        async with self._lock:
            self.value -= amount

    async def get(self) -> int:
        """
        Get the current value.

        Returns:
            int: The current value of the AtomicInteger.
        """
        async with self._lock:
            return self.value

    async def set(self, value: int) -> None:
        """
        Set the value to a specified amount.

        Args:
            value (int): The value to set the AtomicInteger to.
        """
        async with self._lock:
            self.value = value
