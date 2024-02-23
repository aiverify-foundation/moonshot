from typing import Callable, Union

from pydantic import BaseModel


class BenchmarkProgress(BaseModel):
    # Executable information
    exec_id: str
    exec_name: str
    exec_type: str

    # Benchmarking information
    bm_max_progress_per_recipe: int
    bm_progress_callback_func: Union[Callable, None]

    # Current recipe index and name with its progress
    curr_recipe_index: int = 0
    curr_recipe_name: str = ""
    curr_duration: int = 0
    curr_status: str = "pending"
    curr_progress: int = 0
    curr_results: str = ""

    def update_progress(
        self,
        recipe_index: int,
        recipe_name: str,
        duration: int,
        status: str,
        results: str,
    ):
        """
        Updates the progress of the current recipe.

        This method updates the current recipe index and name, and calculates the current progress based on the
        recipe index and the maximum progress per recipe. If a progress callback function is provided, it will
        be called with the current benchmark progress information.

        Args:
            recipe_index (int): The index of the current recipe.
            recipe_name (str): The name of the current recipe.
        """
        self.curr_recipe_index = recipe_index
        self.curr_recipe_name = recipe_name
        self.curr_duration = duration
        self.curr_status = status.lower()
        self.curr_progress = self.curr_recipe_index * self.bm_max_progress_per_recipe
        self.curr_results = results

        if self.bm_progress_callback_func:
            self.bm_progress_callback_func(self.get_dict())

    def get_dict(self):
        """
        Returns a dictionary representation of the BenchmarkProgress instance.

        This method takes all the attributes of the BenchmarkProgress instance and constructs a dictionary
        with attribute names as keys and their corresponding values. This includes the exec_id, exec_name, exec_type,
        bm_max_progress_per_recipe, curr_recipe_index, curr_duration, curr_status, curr_recipe_name, curr_progress,
        and curr_results. This dictionary can be used for serialization purposes, such as storing the benchmark progress
        information in a JSON file or sending it over a network.

        Returns:
            dict: A dictionary representation of the BenchmarkProgress instance.
        """
        return {
            "exec_id": self.exec_id,
            "exec_name": self.exec_name,
            "exec_type": self.exec_type,
            "bm_max_progress_per_recipe": self.bm_max_progress_per_recipe,
            "curr_recipe_index": self.curr_recipe_index,
            "curr_duration": self.curr_duration,
            "curr_status": self.curr_status,
            "curr_recipe_name": self.curr_recipe_name,
            "curr_progress": self.curr_progress,
            "curr_results": self.curr_results,
        }
