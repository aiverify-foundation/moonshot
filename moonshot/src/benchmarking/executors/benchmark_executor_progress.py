from typing import Callable, Union

from pydantic import BaseModel


class BenchmarkExecutorProgress(BaseModel):
    # Executable information
    exec_id: str
    exec_name: str
    exec_type: str

    # Benchmarking information
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
        error_messages: Union[list, None] = None,
    ) -> None:
        """
        Updates the progress of the BenchmarkExecutor.

        This method takes the current progress information of the BenchmarkExecutor and updates its attributes
        accordingly. The attributes that can be updated include: cookbook index, cookbook name, cookbook total,
        recipe index, recipe name, recipe total, duration, status, and error messages.

        This method is useful for tracking the progress of the benchmark execution and can be used for updating
        the progress information in a user interface or logging system.

        Returns:
            None
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
        if cookbook_index is not None and cookbook_index != self.curr_cookbook_index:
            has_changes = True
            self.curr_cookbook_index = cookbook_index

        # Update recipe index and progress
        if recipe_index is not None and recipe_index != self.curr_recipe_index:
            has_changes = True
            self.curr_recipe_index = recipe_index

        # Calculate percentage
        if self.curr_cookbook_total > 0:
            if (
                self.curr_recipe_total > 0
                and self.curr_cookbook_index != self.curr_cookbook_total
            ):
                # Calculate percentage with cookbook and recipe defined
                per_recipe_percentage = (
                    100 / self.curr_cookbook_total
                ) / self.curr_recipe_total
                self.curr_progress = int(
                    self.curr_cookbook_index * (100 / self.curr_cookbook_total)
                ) + int(self.curr_recipe_index * per_recipe_percentage)
            else:
                # Calculate percentage with cookbook defined and no recipes defined
                # Or cookbook index and total is same.
                self.curr_progress = int(
                    self.curr_cookbook_index * (100 / self.curr_cookbook_total)
                )

        elif self.curr_recipe_total > 0:
            # There is no cookbook, calculate for recipes defined
            self.curr_progress = int(
                self.curr_recipe_index * (100 / self.curr_recipe_total)
            )
        else:
            # Initialization: set 0
            self.curr_progress = 0

        # Perform callback only when it has changes and is provided.
        if has_changes and self.bm_progress_callback_func:
            self.bm_progress_callback_func(self.get_dict())

    def get_dict(self):
        """
        Returns a dictionary representation of the current benchmark execution progress.

        This method constructs a dictionary with the current state of the benchmark execution. The dictionary includes
        the execution id, name, type, current duration, status, cookbook index, cookbook name, cookbook total,
        recipe index, recipe name, recipe total, progress, and error messages.

        Returns:
            dict: A dictionary containing the current state of the benchmark execution.
        """
        return {
            "exec_id": self.exec_id,
            "exec_name": self.exec_name,
            "exec_type": self.exec_type,
            "curr_duration": self.curr_duration,
            "curr_status": self.curr_status,
            "curr_cookbook_index": self.curr_cookbook_index,
            "curr_cookbook_name": self.curr_cookbook_name,
            "curr_cookbook_total": self.curr_cookbook_total,
            "curr_recipe_index": self.curr_recipe_index,
            "curr_recipe_name": self.curr_recipe_name,
            "curr_recipe_total": self.curr_recipe_total,
            "curr_progress": self.curr_progress,
            "curr_error_messages": list(set(self.curr_error_messages)),
        }
