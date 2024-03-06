from typing import Callable, Union

from pydantic import BaseModel


class BenchmarkExecutorProgress(BaseModel):
    # Executable information
    exec_id: str
    exec_name: str
    exec_type: str

    # Benchmarking information
    bm_max_progress_per_cookbook: int
    bm_max_progress_per_recipe: int
    bm_progress_callback_func: Union[Callable, None]

    # Current cookbook, recipe index and name with its progress
    curr_cookbook_index: int = -1
    curr_cookbook_name: str = ""
    curr_cookbook_total: int = -1
    curr_recipe_index: int = -1
    curr_recipe_name: str = ""
    curr_recipe_total: int = -1
    curr_duration: int = 0
    curr_status: str = "pending"
    curr_progress: int = 0
    curr_results: dict = {}
    curr_error_messages: list = []

    def update_progress(
        self,
        cookbook_index: Union[int, None] = None,
        cookbook_name: Union[str, None] = None,
        cookbook_total: Union[int, None] = None,
        recipe_index: Union[int, None] = None,
        recipe_name: Union[str, None] = None,
        recipe_total: Union[int, None] = None,
        duration: Union[int, None] = None,
        status: Union[str, None] = None,
        results: Union[dict, None] = None,
        error_messages: Union[list, None] = None,
    ):
        """
        Updates the progress of the benchmark execution.

        This method takes various parameters related to the progress of the benchmark execution and updates the
        corresponding attributes of the BenchmarkExecutorProgress instance. If there are any changes in the progress,
        it calls the progress callback function with the current progress information.

        Args:
            cookbook_index (Union[int, None], optional): The current index of the cookbook being executed.
            Defaults to None.
            cookbook_name (Union[str, None], optional): The name of the current cookbook being executed.
            Defaults to None.
            cookbook_total (Union[int, None], optional): The total number of cookbooks. Defaults to None.
            recipe_index (Union[int, None], optional): The current index of the recipe being executed. Defaults to None.
            recipe_name (Union[str, None], optional): The name of the current recipe being executed. Defaults to None.
            recipe_total (Union[int, None], optional): The total number of recipes. Defaults to None.
            duration (Union[int, None], optional): The current duration of the benchmark execution. Defaults to None.
            status (Union[str, None], optional): The current status of the benchmark execution. Defaults to None.
            results (Union[dict, None], optional): The current results of the benchmark execution. Defaults to None.
            error_messages (Union[list, None], optional): The current error messages of the benchmark execution.
            Defaults to None.
        """
        has_changes = False

        # Update other attributes
        attributes = {
            "curr_cookbook_name": cookbook_name,
            "curr_cookbook_total": cookbook_total,
            "curr_recipe_name": recipe_name,
            "curr_recipe_total": recipe_total,
            "curr_duration": duration,
            "curr_status": status.lower() if status else None,
            "curr_results": results,
        }
        for attr, value in attributes.items():
            if value is not None and value != getattr(self, attr):
                has_changes = True
                setattr(self, attr, value)

        # Update error messages
        if error_messages is not None and error_messages != self.curr_error_messages:
            has_changes = True
            self.curr_error_messages = error_messages.copy()

        # Update cookbook index and progress
        if (
            cookbook_index is not None
            and cookbook_index >= 0
            and cookbook_index != self.curr_cookbook_index
        ):
            has_changes = True
            self.curr_cookbook_index = cookbook_index
            self.curr_progress = (
                self.curr_cookbook_index * self.bm_max_progress_per_cookbook
            )

        # Update recipe index and progress
        if (
            recipe_index is not None
            and recipe_index >= 0
            and recipe_index != self.curr_recipe_index
        ):
            has_changes = True
            self.curr_recipe_index = recipe_index
            self.curr_progress = (
                self.curr_recipe_index * self.bm_max_progress_per_recipe
            )

        # Perform callback only when it has changes and is provided.
        if has_changes and self.bm_progress_callback_func:
            self.bm_progress_callback_func(self.get_dict())

    def get_dict(self):
        """
        Returns a dictionary representation of the current benchmark execution progress.

        This method constructs a dictionary with the current state of the benchmark execution. The dictionary includes
        the execution id, name, type, maximum progress per cookbook and recipe, current duration, status,
        cookbook index, cookbook name, cookbook total, recipe index, recipe name, recipe total, progress, results,
        and error messages.

        Returns:
            dict: A dictionary containing the current state of the benchmark execution.
        """
        return {
            "exec_id": self.exec_id,
            "exec_name": self.exec_name,
            "exec_type": self.exec_type,
            "bm_max_progress_per_cookbook": self.bm_max_progress_per_cookbook,
            "bm_max_progress_per_recipe": self.bm_max_progress_per_recipe,
            "curr_duration": self.curr_duration,
            "curr_status": self.curr_status,
            "curr_cookbook_index": self.curr_cookbook_index,
            "curr_cookbook_name": self.curr_cookbook_name,
            "curr_cookbook_total": self.curr_cookbook_total,
            "curr_recipe_index": self.curr_recipe_index,
            "curr_recipe_name": self.curr_recipe_name,
            "curr_recipe_total": self.curr_recipe_total,
            "curr_progress": self.curr_progress,
            "curr_results": self.curr_results,
            "curr_error_messages": list(set(self.curr_error_messages)),
        }
