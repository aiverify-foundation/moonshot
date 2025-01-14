import json
import time
from typing import Callable

from moonshot.src.messages_constants import RUN_NOTIFY_PROGRESS_DB_INSTANCE_NOT_PROVIDED
from moonshot.src.runs.run_arguments import RunArguments
from moonshot.src.runs.run_progress_structure import create_run_progress_structure
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

    def display_run_progress(self, progress: dict) -> None:
        """
        Display the current progress of the run.

        This method prints the current progress to the console. It is used as the default
        callback function for displaying run progress if no other callback function is provided.

        Args:
            progress (dict): A dictionary containing the current progress information.
        """
        # Print the progress dictionary to the console
        print("Progress: ", json.dumps(progress))

    def __init__(
        self, run_arguments: RunArguments, run_progress_callback_func: Callable | None
    ):
        """
        Initialize a RunProgress instance to track and manage the progress of a run.

        This constructor sets up the initial state of the RunProgress object, including
        storing the run arguments and setting up a callback function for progress updates.

        Args:
            run_arguments (RunArguments): The arguments related to the run, containing
                                          details such as start time, error messages, etc.
            run_progress_callback_func (Callable | None): A callback function that is invoked
                                                          to update run progress. If None, a default
                                                          display function is used.
        """
        self.current_progress = create_run_progress_structure()

        # Store the run arguments
        self.run_arguments = run_arguments

        # Assign the callback function for progress updates, default to display function if no callback is provided
        self.run_progress_callback_func = (
            run_progress_callback_func or self.display_run_progress
        )

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

            # Append the error message to the run arguments' error messages list if it's not already present
            if error_message not in self.run_arguments.error_messages:
                self.run_arguments.error_messages.append(error_message)

            # Update progress status to indicate that the run is continuing with errors
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
            # Update self.run_arguments if the attribute exists
            if hasattr(self.run_arguments, key):
                setattr(self.run_arguments, key, value)

            # Update self.current_progress with the key and value
            if key == "status" and isinstance(value, RunStatus):
                self.current_progress[key] = value.value
            else:
                self.current_progress[key] = value

        # Update database record
        if self.run_arguments.database_instance:
            Storage.update_database_record(
                self.run_arguments.database_instance,
                self.run_arguments.to_tuple(),
                RunProgress.sql_update_run_record,
            )
        else:
            logger.warning(RUN_NOTIFY_PROGRESS_DB_INSTANCE_NOT_PROVIDED)

        # If a callback function is provided, call it with the updated run arguments
        if self.run_progress_callback_func:
            # Call the callback function with the current state of run arguments
            self.run_progress_callback_func(self.format_progress())

    def format_progress(self) -> dict:
        """
        Format the current progress by removing duplicate error messages.

        This method ensures that the 'current_error_messages' list in the current progress
        dictionary contains only unique error messages. It then returns the updated
        current progress dictionary.

        Returns:
            dict: The updated current progress dictionary with unique error messages.
        """
        # Remove duplicate error messages
        self.current_progress["current_error_messages"] = list(
            set(self.current_progress["current_error_messages"])
        )

        # Return the updated current progress
        return self.current_progress
