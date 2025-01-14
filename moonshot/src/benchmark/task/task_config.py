import asyncio
import uuid
from datetime import datetime
from typing import Any, Callable

from pydantic import BaseModel, Field

from moonshot.src.connectors.connector import Connector
from moonshot.src.cookbooks.cookbook import Cookbook
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.storage.db_interface import DBInterface


class TaskConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    """
    Configuration model for a benchmarking task.

    Attributes:
        task_uuid (uuid.UUID): The unique identifier for the task.
        task_concurrency_limit (int): The maximum number of concurrent tasks.
        connector (Connector): The connector instance to be used for the task.
        cookbook (Cookbook | None): The cookbook associated with the task, if any.
        database (DBInterface): The database interface instance for storing and retrieving data.
        task_progress_fn (Callable): Function to handle task progress updates.
        task_prompt_selection_percentage (int): The percentage of prompts to be selected.
        task_prompt_augmented_template_id (Any): The ID of the prompt template used for augmentation.
        task_random_seed (int): The seed for random number generation.
        recipe (Recipe): The recipe instance to be used for the task.
        use_cache (bool): Flag indicating whether to use cached results.
        cancel_event (asyncio.Event): The event to signal task cancellation.
        start_time (datetime): The start time of the task.
        end_time (datetime): The end time of the task.
    """
    # Required attributes for task configuration
    cancel_event: asyncio.Event  # The event to signal task cancellation.
    connector: Connector  # The connector instance to be used for the task.
    cookbook: Cookbook | None  # The cookbook associated with the task, if any.
    database: DBInterface  # The database interface instance for storing and retrieving data.
    recipe: Recipe  # The recipe instance to be used for the task.

    # Attributes related to the task's unique identification and evaluation
    task_concurrency_limit: int  # The maximum number of concurrent tasks.
    task_progress_fn: Callable  # Function to handle task progress updates.
    task_prompt_augmented_template_id: Any  # The ID of the prompt template used for augmentation.
    task_prompt_selection_percentage: int  # The percentage of prompts to be selected.
    task_random_seed: int  # The seed for random number generation.
    task_uuid: uuid.UUID  # The unique identifier for the task.

    # Optional attributes for task configuration
    end_time: datetime = Field(
        default_factory=datetime.now
    )  # The timestamp when the task ends.
    start_time: datetime = Field(
        default_factory=datetime.now
    )  # The timestamp when the task starts.
    use_cache: bool = True  # Flag indicating whether to use cached results.
