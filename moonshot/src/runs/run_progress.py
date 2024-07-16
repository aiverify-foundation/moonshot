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
        # Information on the run and callback for progress updating
        self.run_arguments = run_arguments
        self.run_progress_callback_func = run_progress_callback_func

        # Information to be sent back through callback
        self.cookbook_index: int = -1
        self.cookbook_name: str = ""
        self.cookbook_total: int = -1
        self.recipe_index: int = -1
        self.recipe_name: str = ""
        self.recipe_total: int = -1
        self.progress: int = 0

    def notify_error(self, error_message: str) -> None:
        """
        Notifies about an error that occurred during the run process.

        This method logs the error message, appends it to the run arguments' error messages list,
        and updates the run progress status to indicate that the run is continuing with errors.

        Args:
            error_message (str): The error message to be logged and recorded.
        """
        # Update error message
        logger.error(error_message)
        self.run_arguments.error_messages.append(error_message)

        # Update progress status
        self.notify_progress(status=RunStatus.RUNNING_WITH_ERRORS)

    def notify_progress(self, **kwargs) -> None:
        """
        Updates the run progress information and the run status.

        This method is responsible for updating the run status, setting the end time, calculating the run duration,
        and persisting these changes to the database. Additionally, if a callback function for run progress has been
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

        # Calculate percentage
        if self.cookbook_total > 0:
            if self.recipe_total > 0 and self.cookbook_index != self.cookbook_total:
                # Calculate percentage with cookbook and recipe defined
                per_recipe_percentage = (100 / self.cookbook_total) / self.recipe_total
                self.progress = int(
                    self.cookbook_index * (100 / self.cookbook_total)
                ) + int(self.recipe_index * per_recipe_percentage)
            else:
                # Calculate percentage with cookbook defined and no recipes defined
                # Or cookbook index and total is same.
                self.progress = int(self.cookbook_index * (100 / self.cookbook_total))
        elif self.recipe_total > 0:
            # There is no cookbook, calculate for recipes defined
            self.progress = int(self.recipe_index * (100 / self.recipe_total))
        else:
            # Initialization: set 0
            self.progress = 0

        # Update database record
        if self.run_arguments.database_instance:
            Storage.update_database_record(
                self.run_arguments.database_instance,
                self.run_arguments.to_tuple(),
                RunProgress.sql_update_run_record,
            )
        else:
            logger.warning(
                "[RunProgress] Failed to update run progress: database instance is not initialised."
            )

        # If a callback function is provided, call it with the updated run arguments
        if self.run_progress_callback_func:
            self.run_progress_callback_func(self.get_dict())

    def get_dict(self) -> dict:
        """
        Constructs and returns a dictionary with the current state of the benchmark execution.

        This method assembles a dictionary encapsulating the current progress of the benchmark execution.
        The resulting dictionary is composed of the following keys: execution identifier, name, type, current duration,
        status, cookbook index, cookbook name, cookbook total, recipe index, recipe name, recipe total,
        progress percentage, and a list of error messages.

        Returns:
            dict: A dictionary representing the current benchmark execution state, with keys for various progress
            metrics and details.
        """
        return {
            "current_runner_id": self.run_arguments.runner_id,
            "current_runner_type": self.run_arguments.runner_type.value,
            "current_duration": self.run_arguments.duration,
            "current_status": self.run_arguments.status.value,
            "current_cookbook_index": self.cookbook_index,
            "current_cookbook_name": self.cookbook_name,
            "current_cookbook_total": self.cookbook_total,
            "current_recipe_index": self.recipe_index,
            "current_recipe_name": self.recipe_name,
            "current_recipe_total": self.recipe_total,
            "current_progress": self.progress,
            "current_error_messages": list(set(self.run_arguments.error_messages)),
        }
