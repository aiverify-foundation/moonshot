import time
from typing import Callable

from moonshot.src.runs.run_arguments import RunArguments
from moonshot.src.runs.run_status import RunStatus
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class RunProgress:
    sql_update_run_record = """
        UPDATE run_table SET runner_id=?,runner_type=?,runner_args=?,endpoints=?,results_file=?,start_time=?,end_time=?,
        duration=?,error_messages=?,raw_results=?,results=?,status=?
        WHERE run_id=?
    """

    def __init__(
        self, run_arguments: RunArguments, run_progress_callback_func: Callable | None
    ):
        """
        Initializes the RunProgress instance with the given run arguments and callback function.

        Args:
            run_arguments (RunArguments): The arguments related to the run.
            run_progress_callback_func (Callable | None): A callback function for updating run progress.
        """
        # Store the run arguments and callback function for progress updates
        self.run_arguments = run_arguments
        self.run_progress_callback_func = run_progress_callback_func

        # Initialize progress tracking attributes
        self.total_num_of_tasks: int = 0
        self.total_num_of_prompts: int = 0
        self.total_num_of_metrics: int = 0
        self.completed_num_of_prompts: int = 0
        self.cancelled_num_of_prompts: int = 0
        self.error_num_of_prompts: int = 0
        self.completed_num_of_metrics: int = 0
        self.overall_progress: int = 0
        self.overall_prompt_progress: int = 0
        self.overall_metric_progress: int = 0

        # Lists to track error or cancelled prompts
        self.cancelled_prompts = []
        self.error_prompts = []

        # List to track current running tasks
        self.current_running_tasks = []

    def notify_error(self, error_message: str) -> None:
        """
        Logs an error message and updates the run status to indicate errors.

        This method logs the error message, appends it to the run arguments' error messages list,
        and updates the run progress status to indicate that the run is continuing with errors.

        Args:
            error_message (str): The error message to be logged and recorded.
        """
        if error_message:
            # Log the error message
            logger.error(error_message)
            if error_message not in self.run_arguments.error_messages:
                self.run_arguments.error_messages.append(error_message)

            # Update progress status
            self.notify_progress(status=RunStatus.RUNNING_WITH_ERRORS)

    def notify_progress(self, **kwargs) -> None:
        """
        Updates the run progress information and the run status.

        This method updates the run status, sets the end time, calculates the run duration,
        and persists these changes to the database. Additionally, if a callback function for run progress has been
        set, this method will invoke it with the current state of run arguments.

        The method accepts arbitrary keyword arguments which are used to update specific attributes of the run_arguments
        object. It ensures that the run progress is accurately reflected in both the object's state and the
        corresponding database record.

        Args:
            **kwargs: Keyword arguments that correspond to the attributes of run_arguments which should be updated.

        Returns:
            None
        """
        # Update run arguments values
        if self.run_arguments.start_time > 0.0:
            self.run_arguments.end_time = time.time()
            self.run_arguments.duration = int(
                self.run_arguments.end_time - self.run_arguments.start_time
            )

        # Update run arguments values with provided key-value pairs
        for key, value in kwargs.items():
            # Update self values
            if hasattr(self, key):
                setattr(self, key, value)

            # Update self.run_arguments
            if hasattr(self.run_arguments, key):
                setattr(self.run_arguments, key, value)

        # Update database record
        if self.run_arguments.database_instance:
            Storage.update_database_record(
                self.run_arguments.database_instance,
                self.run_arguments.to_tuple(),
                RunProgress.sql_update_run_record,
            )
        else:
            logger.warning(
                "[RunProgress] Failed to update run progress: database instance is not initialized."
            )

        # If a callback function is provided, call it with the updated run arguments
        if self.run_progress_callback_func:
            self.run_progress_callback_func(self.get_dict())

    def get_dict(self) -> dict:
        """
        Constructs and returns a dictionary with the current state of the run progress.

        This method assembles a dictionary encapsulating the current progress of the run.
        The resulting dictionary includes the total number of tasks, total number of prompts,
        completed prompts, cancelled prompts, error prompts, total number of metrics, completed metrics,
        current runner ID, current status, current progress, current cancelled prompts, current error prompts,
        a list of unique error messages, and the current running tasks.

        Returns:
            dict: A dictionary representing the current run progress state. The dictionary contains the following keys:
                - total_num_of_tasks (int): The total number of tasks.
                - total_num_of_prompts (int): The total number of prompts.
                - total_num_of_metrics (int): The total number of metrics.
                - completed_num_of_prompts (int): The number of completed prompts.
                - cancelled_num_of_prompts (int): The number of cancelled prompts.
                - error_num_of_prompts (int): The number of error prompts.
                - completed_num_of_metrics (int): The number of completed metrics.
                - current_runner_id (str): The ID of the current runner.
                - current_status (str): The current status of the run.
                - current_progress (float): The overall progress of the run.
                - current_prompt_progress (float): The progress of the prompts.
                - current_metric_progress (float): The progress of the metrics.
                - current_cancelled_prompts (list): The current cancelled benchmark prompts.
                - current_error_prompts (list): The current error benchmark prompts.
                - current_error_messages (list[str]): A list of unique error messages.
                - current_running_tasks (list[dict]): A list of dictionaries representing the current running tasks.
        """
        return {
            "total_num_of_tasks": self.total_num_of_tasks,
            "total_num_of_prompts": self.total_num_of_prompts,
            "total_num_of_metrics": self.total_num_of_metrics,
            "completed_num_of_prompts": self.completed_num_of_prompts,
            "cancelled_num_of_prompts": self.cancelled_num_of_prompts,
            "error_num_of_prompts": self.error_num_of_prompts,
            "completed_num_of_metrics": self.completed_num_of_metrics,
            "current_runner_id": self.run_arguments.runner_id,
            "current_status": self.run_arguments.status.value,
            "current_progress": self.overall_progress,
            "current_prompt_progress": self.overall_prompt_progress,
            "current_metric_progress": self.overall_metric_progress,
            "current_cancelled_prompts": self.cancelled_prompts,
            "current_error_prompts": self.error_prompts,
            "current_error_messages": list(set(self.run_arguments.error_messages)),
            "current_running_tasks": self.current_running_tasks,
        }
