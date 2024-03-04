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
    ):
        """
        Updates the progress of the current benchmark execution.

        This method updates the progress of the current benchmark execution based on the provided parameters.
        If a parameter is not provided or is None, the corresponding attribute of the BenchmarkExecutorProgress
        instance is not updated. If a parameter is provided, the corresponding attribute of the
        BenchmarkExecutorProgress instance is updated with the provided value.

        After updating the progress, if a progress callback function is set, it is called with the current
        progress information as a dictionary.

        Args:
            cookbook_index (Union[int, None], optional): The index of the current cookbook. Defaults to None.
            cookbook_name (Union[str, None], optional): The name of the current cookbook. Defaults to None.
            cookbook_total (Union[int, None], optional): The total number of cookbooks. Defaults to None.
            recipe_index (Union[int, None], optional): The index of the current recipe. Defaults to None.
            recipe_name (Union[str, None], optional): The name of the current recipe. Defaults to None.
            recipe_total (Union[int, None], optional): The total number of recipes. Defaults to None.
            duration (Union[int, None], optional): The duration of the current execution. Defaults to None.
            status (Union[str, None], optional): The status of the current execution. Defaults to None.
            results (Union[dict, None], optional): The results of the current execution. Defaults to None.
        """
        if cookbook_index is not None and cookbook_index >= 0:
            self.curr_cookbook_index = cookbook_index
            self.curr_progress = (
                self.curr_cookbook_index * self.bm_max_progress_per_cookbook
            )

        if cookbook_name:
            self.curr_cookbook_name = cookbook_name

        if cookbook_total:
            self.curr_cookbook_total = cookbook_total

        if recipe_index is not None and recipe_index >= 0:
            self.curr_recipe_index = recipe_index
            self.curr_progress = (
                self.curr_recipe_index * self.bm_max_progress_per_recipe
            )

        if recipe_name:
            self.curr_recipe_name = recipe_name

        if recipe_total:
            self.curr_recipe_total = recipe_total

        if duration:
            self.curr_duration = duration

        if status:
            self.curr_status = status.lower()

        if results:
            self.curr_results = results

        if self.bm_progress_callback_func:
            self.bm_progress_callback_func(self.get_dict())

    def get_dict(self):
        """
        Returns the current progress information as a dictionary.

        This method constructs a dictionary with the current progress information. The dictionary includes the
        execution ID, execution name, execution type, maximum progress per cookbook, maximum progress per recipe,
        current duration, current status, current cookbook index, current cookbook name, current cookbook total,
        current recipe index, current recipe name, current recipe total, current progress, and current results.

        Returns:
            dict: A dictionary representation of the current progress information.
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
        }
