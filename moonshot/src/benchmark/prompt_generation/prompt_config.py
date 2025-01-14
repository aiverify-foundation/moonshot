import asyncio
import uuid
from datetime import datetime
from typing import Any, Callable

from pydantic import BaseModel, Field

from moonshot.src.connectors.connector import Connector
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.storage.db_interface import DBInterface


class PromptConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    """
    Configuration model for a benchmarking prompt.

    Attributes:
        cancel_event (asyncio.Event): Event to signal prompt cancellation.
        connector (Connector): Connector instance to be used for the prompt.
        database (DBInterface): Database interface for storing and retrieving data.
        dataset_id (str): ID of the dataset used in the benchmarking.
        recipe (Recipe): Recipe associated with the prompt.
        prompt_augmented_content (Any): The actual prompt content, potentially augmented by the prompt template.
        prompt_augmented_template_id (Any): The ID of the prompt template used for augmentation.
        prompt_details (dict): Detailed information about the prompt, including prompt text, target, and other relevant data.  # noqa: E501
        prompt_evaluation_results (dict): Contains the result of the evaluation of the prompt and predicted results.
        prompt_index (int): Index of the prompt in the dataset.
        prompt_progress_fn (Callable): Function to handle prompt progress updates.
        prompt_uuid (uuid.UUID): Unique identifier for the prompt.
        use_cache (bool, optional): Indicates whether to use cached results. Defaults to True.
        start_time (datetime, optional): Timestamp when the prompt starts. Defaults to current time.
        end_time (datetime, optional): Timestamp when the prompt ends. Defaults to current time.
    """
    # Required attributes for prompt configuration
    cancel_event: asyncio.Event  # Event to signal prompt cancellation
    connector: Connector  # Connector instance to be used for the prompt
    database: DBInterface  # Database interface for storing and retrieving data
    dataset_id: str  # ID of the dataset used in the benchmarking
    recipe: Recipe  # Recipe associated with the prompt

    # Attributes related to the prompt's unique identification and evaluation
    prompt_augmented_content: Any  # The actual prompt content, potentially augmented by the prompt template
    prompt_augmented_template_id: Any  # The ID of the prompt template used for augmentation
    prompt_details: dict  # Detailed information about the prompt, including prompt text, target, and other relevant data  # noqa: E501
    prompt_evaluation_results: dict  # Contains the result of the evaluation of the prompt and predicted results
    prompt_index: int  # Index of the prompt in the dataset
    prompt_progress_fn: Callable  # Function to handle prompt progress updates
    prompt_uuid: uuid.UUID  # Unique identifier for the prompt

    # Optional attributes for prompt configuration
    end_time: datetime = Field(
        default_factory=datetime.now
    )  # Timestamp when the prompt ends
    start_time: datetime = Field(
        default_factory=datetime.now
    )  # Timestamp when the prompt starts
    use_cache: bool = True  # Indicates whether to use cached results
