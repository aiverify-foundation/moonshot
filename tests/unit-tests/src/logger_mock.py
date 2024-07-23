class LoggerMock:
    """
    A mock logger class for testing logging functionality.

    Attributes:
        messages (dict): A dictionary holding lists of logged messages, categorized by log level.
    """

    def __init__(self):
        """
        Initializes the LoggerMock with empty message lists for each log level.
        """
        self.messages = {
            "debug": [],
            "info": [],
            "warning": [],
            "error": [],
            "critical": [],
        }

    def debug(self, msg):
        """
        Logs a debug message.

        Args:
            msg (str): The debug message to log.
        """
        self.messages["debug"].append(msg)

    def info(self, msg):
        """
        Logs an info message.

        Args:
            msg (str): The info message to log.
        """
        self.messages["info"].append(msg)

    def warning(self, msg):
        """
        Logs a warning message.

        Args:
            msg (str): The warning message to log.
        """
        self.messages["warning"].append(msg)

    def error(self, msg):
        """
        Logs an error message.

        Args:
            msg (str): The error message to log.
        """
        self.messages["error"].append(msg)

    def critical(self, msg):
        """
        Logs a critical message.

        Args:
            msg (str): The critical message to log.
        """
        self.messages["critical"].append(msg)
