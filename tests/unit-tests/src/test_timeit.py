from time import sleep

from moonshot.src.utils.timeit import timeit


class TestCollectionTimeitMethod:
    @staticmethod
    def time_me():
        """
        Simulate a time-consuming operation.

        This static method is used as a test function within the TestCollectionTimeitMethod
        class to emulate a process that takes a significant amount of time to complete,
        specifically by sleeping for 1 second.

        Returns:
            None
        """
        sleep(1)

    def test_time_class_method(self, capsys):
        """
        Test the timeit decorator on a static method.

        This test applies the 'timeit' decorator to the 'time_me' static method and
        executes it. It captures the standard output and asserts that the output contains
        the expected duration of the operation (1 second) as reported by the 'timeit'
        decorator.

        Args:
            capsys: A pytest fixture that captures the standard output and error streams.

        Returns:
            None
        """
        test_func = timeit(self.time_me)
        test_func()
        captured_sys_output = capsys.readouterr()
        # Compare the output. Omitted the decimal seconds
        assert captured_sys_output.out[:42] == (
            "[src.test_timeit] Running [time_me] took 1"
        )
        assert captured_sys_output.out[47:] == "s\n"
