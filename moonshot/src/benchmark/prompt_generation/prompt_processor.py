from __future__ import annotations

import ast
import asyncio
import json
from datetime import datetime

from moonshot.src.benchmark.prompt_generation.prompt_config import PromptConfig
from moonshot.src.benchmark.prompt_generation.prompt_status import PromptStatus
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_prompt_arguments import ConnectorPromptArguments
from moonshot.src.connectors.connector_response import ConnectorResponse
from moonshot.src.messages_constants import (
    PROMPT_PROCESS_EVALUATE_METRICS_EXCEPTION_ERROR,
    PROMPT_PROCESS_QUERY_CONNECTOR_EXCEPTION_ERROR,
    PROMPT_PROCESSOR_EVALUATE_METRICS_CURRENT_METRIC_DEBUG,
    PROMPT_PROCESSOR_EVALUATE_METRICS_DEBUG,
    PROMPT_PROCESSOR_PROCESS_PROMPT_CANCELLED_ERROR,
    PROMPT_PROCESSOR_PROCESS_PROMPT_EXCEPTION_ERROR,
    PROMPT_PROCESSOR_QUERY_CONNECTOR_DEBUG,
    PROMPT_PROCESSOR_SET_STATUS_DEBUG,
)
from moonshot.src.metrics.metric import Metric
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class PromptProcessor:
    # SQL query to create or update a runner cache record
    sql_create_runner_cache_record = """
        INSERT INTO runner_cache_table(connection_id, recipe_id, dataset_id, prompt_template_id,
        prompt_index, prompt, target, predicted_results, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    # SQL query to read a runner cache record
    sql_read_runner_cache_record = """
        SELECT * from runner_cache_table WHERE connection_id=? AND recipe_id=?
        AND dataset_id=? AND prompt_template_id=? AND prompt=?
        ORDER BY id DESC
        LIMIT 1;
    """

    def __init__(self, config: PromptConfig):
        """
        Initializes a PromptProcessor instance using the provided configuration.

        This constructor sets up the prompt with all necessary attributes, including
        required and optional configurations, as well as attributes related to the prompt's
        unique identification and evaluation.

        Args:
            config (PromptConfig): A configuration object containing all necessary attributes for the prompt.
        """
        # Required attributes for prompt configuration
        self.cancel_event = config.cancel_event
        self.connector = config.connector
        self.database = config.database
        self.dataset_id = config.dataset_id
        self.recipe = config.recipe

        # Attributes related to the prompt's unique identification and evaluation
        self.prompt_augmented_content = config.prompt_augmented_content
        self.prompt_augmented_template_id = config.prompt_augmented_template_id
        self.prompt_details = config.prompt_details
        self.prompt_evaluation_results = config.prompt_evaluation_results
        self.prompt_index = config.prompt_index
        self.prompt_progress_fn = config.prompt_progress_fn
        self.prompt_status = PromptStatus.PENDING
        self.prompt_uuid = str(config.prompt_uuid)

        # Form the ConnectorPromptArguments
        self.connector_prompt = ConnectorPromptArguments(
            prompt_index=self.prompt_index,
            prompt=self.prompt_augmented_content or self.prompt_details.get("input"),
            target=self.prompt_details.get("target"),
        )

        # Optional attributes for prompt configuration
        self.end_time = config.end_time
        self.error_messages = []
        self.start_time = config.start_time
        self.use_cache = config.use_cache
        if self.end_time < self.start_time:
            self.duration = 0
        else:
            self.duration = (self.end_time - self.start_time).total_seconds()

    async def set_status(self, new_status: PromptStatus) -> None:
        """
        Update the status of the prompt and perform real-time updates if a progress function is provided.

        Args:
            new_status (PromptStatus): The new status to set for the prompt.
        """
        # Update the prompt status
        self.prompt_status = new_status
        logger.debug(
            PROMPT_PROCESSOR_SET_STATUS_DEBUG.format(
                uuid=self.prompt_uuid, new_status=new_status.value
            )
        )

        # If a progress function is provided, perform real-time updates
        if self.prompt_progress_fn:
            # Await the progress function to provide prompt progress
            await self.prompt_progress_fn(self.provide_prompt_progress())

    async def process_prompt(self) -> None:
        """
        Process the prompt through various phases including querying the connector and evaluating metrics.

        This method sets the status of the prompt at each phase and checks for cancellation events.
        It handles exceptions and updates the prompt status accordingly.

        Asynchronously process this prompt through various stages:
          1) RUNNING
          2) RUNNING_QUERY_CONNECTOR -> COMPLETED_QUERY_CONNECTOR
          3) RUNNING_METRICS_EVALUATION -> COMPLETED_METRICS_EVALUATION
          4) COMPLETED (or COMPLETED_WITH_ERRORS)

        If an error occurs, transition to COMPLETED_WITH_ERRORS.
        If cancelled, transition to CANCELLED.

        Raises:
            asyncio.CancelledError: If the prompt was explicitly cancelled by higher-level logic.
            Exception: For any other errors encountered during the prompt processing.
        """
        try:
            # Set the status to RUNNING
            await self.set_status(PromptStatus.RUNNING)

            # Check if cancelled before starting
            if self.cancel_event.is_set():
                await self.set_status(PromptStatus.CANCELLED)
                return

            # Run Query Connector phase
            await self.set_status(PromptStatus.RUNNING_QUERY_CONNECTOR)
            await self.query_connector()
            await self.set_status(PromptStatus.COMPLETED_QUERY_CONNECTOR)

            # Check cancellation after connector query
            if self.cancel_event.is_set():
                await self.set_status(PromptStatus.CANCELLED)
                return

            # Run Metrics Evaluation phase
            await self.set_status(PromptStatus.RUNNING_METRICS_EVALUATION)
            await self.evaluate_metrics()
            await self.set_status(PromptStatus.COMPLETED_METRICS_EVALUATION)

            # Check cancellation after metrics evaluation phase
            if self.cancel_event.is_set():
                await self.set_status(PromptStatus.CANCELLED)
                return

            # Everything seems okay, mark prompt as completed
            await self.set_status(PromptStatus.COMPLETED)
            self.end_time = datetime.now()

        except asyncio.CancelledError:
            error_message = PROMPT_PROCESSOR_PROCESS_PROMPT_CANCELLED_ERROR.format(
                uuid=self.prompt_uuid
            )

            # If the prompt was explicitly cancelled by higher-level logic
            logger.error(error_message)
            self.error_messages.append(error_message)
            await self.set_status(PromptStatus.CANCELLED)
            self.end_time = datetime.now()

        except Exception as e:
            error_message = PROMPT_PROCESSOR_PROCESS_PROMPT_EXCEPTION_ERROR.format(
                uuid=self.prompt_uuid, message=str(e)
            )

            # Log the error and set the status to COMPLETED_WITH_ERRORS
            logger.error(error_message)
            self.error_messages.append(error_message)
            await self.set_status(PromptStatus.COMPLETED_WITH_ERRORS)
            self.end_time = datetime.now()

    async def query_connector(self) -> None:
        """
        Asynchronously queries the connector for predictions and handles caching.

        This method forms the ConnectorPromptArguments, checks if caching is enabled,
        attempts to retrieve cached results from the database, and if no cache is found,
        it queries the connector for predictions and caches the results.

        Raises:
            Exception: If an error occurs during the prediction or caching process.
        """
        logger.debug(
            PROMPT_PROCESSOR_QUERY_CONNECTOR_DEBUG.format(uuid=self.prompt_uuid)
        )

        cache_record = None
        # Determine if caching is enabled
        if self.use_cache:
            try:
                # Attempt to retrieve the cache record from the database
                cache_record = Storage.read_database_record(
                    self.database,
                    (
                        self.connector.id,
                        self.recipe.id,
                        self.dataset_id,
                        self.prompt_augmented_template_id,
                        self.connector_prompt.prompt,
                    ),
                    self.sql_read_runner_cache_record,
                )
            except Exception:
                # On error, ensure cache_record is set to None
                cache_record = None

        # If no cache record is found, perform prediction and cache the result
        if cache_record is None:
            try:
                # Obtain prediction from the connector for the current prompt
                self.connector_prompt = await Connector.get_prediction(
                    self.connector_prompt, self.connector
                )
                # Cache the result in the database
                Storage.create_database_record(
                    self.database,
                    self.to_tuple(),
                    self.sql_create_runner_cache_record,
                )
            except Exception as e:
                # Raise the exception with additional context
                raise Exception(
                    PROMPT_PROCESS_QUERY_CONNECTOR_EXCEPTION_ERROR.format(
                        uuid=self.prompt_uuid, message={e}
                    )
                ) from e
        else:
            # Load the result from cache if a record is found
            self.from_tuple(cache_record)

    async def evaluate_metrics(self) -> None:
        """
        Evaluates the metrics for the current prompt.

        This method iterates over the list of metrics defined in the recipe, loads each metric,
        and updates the prompt evaluation results with the results obtained from the metric.

        Raises:
            Exception: If an error occurs during the metric evaluation process.
        """
        # Log the start of the metrics evaluation process
        logger.debug(
            PROMPT_PROCESSOR_EVALUATE_METRICS_DEBUG.format(uuid=self.prompt_uuid)
        )

        # Iterate over each metric defined in the recipe
        for metric_name in self.recipe.metrics:
            # Log the current metric being evaluated
            logger.debug(
                PROMPT_PROCESSOR_EVALUATE_METRICS_CURRENT_METRIC_DEBUG.format(
                    uuid=self.prompt_uuid, metric_name=metric_name
                )
            )

            try:
                # Load the metric instance
                metric_instance = Metric.load(metric_name)

                # Update the prompt evaluation results with the results from the metric
                self.prompt_evaluation_results.update(
                    await metric_instance.get_results(  # type: ignore ; ducktyping
                        [self.connector_prompt.prompt],  # Changed to list
                        [self.connector_prompt.predicted_results],  # Changed to list
                        [self.connector_prompt.target],  # Changed to list
                    )
                )
            except Exception as e:
                # Raise the exception with additional context
                raise Exception(
                    PROMPT_PROCESS_EVALUATE_METRICS_EXCEPTION_ERROR.format(
                        uuid=self.prompt_uuid, message={e}
                    )
                ) from e

    def provide_prompt_progress(self) -> dict:
        """
        Provides a dictionary with the current progress and status of the prompt.

        This method gathers all essential information for an update, including the prompt's UUID,
        current status, index, cache usage, connector ID, dataset ID, recipe ID, prompt template ID,
        start time, end time, prompt details, target, predicted results, duration, and evaluation results.

        Returns:
            dict: A dictionary containing the current progress and status of the prompt.
        """
        return {
            "metadata": {
                "uuid": self.prompt_uuid,
                "status": self.prompt_status.name,
                "index": self.prompt_index,
                "use_cache": self.use_cache,
                "connector_id": self.connector.id,
                "dataset_id": self.dataset_id,
                "recipe_id": self.recipe.id,
                "prompt_template_id": self.prompt_augmented_template_id,
                "start_time": self.start_time.replace(microsecond=0).isoformat(" "),
                "end_time": self.end_time.replace(microsecond=0).isoformat(" "),
            },
            "execution": {
                "error_messages": self.error_messages,
                "prompt_info": {
                    "prompt": self.connector_prompt.prompt,
                    "target": self.connector_prompt.target,
                    "predicted_results": self.connector_prompt.predicted_results,
                    "duration": self.connector_prompt.duration,
                    "evaluation_results": self.prompt_evaluation_results,
                },
                "dataset_prompt_info": self.prompt_details,
            },
        }

    def to_tuple(self) -> tuple:
        """
        Converts the current prompt configuration and its associated details into a tuple.

        This method serializes the attributes of the prompt configuration, including the connector ID,
        recipe ID, dataset ID, prompt template ID, prompt index, prompt text, target, predicted results,
        and duration, into a tuple format. This tuple can be used for storage or transmission purposes.

        Returns:
            tuple: A tuple containing the serialized attributes of the prompt configuration.
        """
        return (
            self.connector.id,
            self.recipe.id,
            self.dataset_id,
            self.prompt_augmented_template_id,
            self.connector_prompt.prompt_index,
            self.connector_prompt.prompt,
            str(self.connector_prompt.target),
            json.dumps(self.connector_prompt.predicted_results.to_dict()),
            str(self.connector_prompt.duration),
        )

    def from_tuple(self, cache_record: tuple) -> None:
        """
        Reconstructs the prompt configuration and its associated details from a tuple.

        This method deserializes the attributes of the prompt configuration from a tuple format.
        It attempts to convert string representations of Python literals back into their original
        data types using ast.literal_eval. If the conversion fails, the original string values are used.
        The method also handles the conversion of JSON strings back into their respective objects.

        Args:
            cache_record (tuple): A tuple containing the serialized attributes of the prompt configuration.
        """
        # Attempt to convert the target field from its string representation back to its original data type
        try:
            target = ast.literal_eval(cache_record[9])
        except Exception:
            target = cache_record[9]

        # Attempt to convert the predicted_results field from its JSON string representation back to a dictionary
        try:
            predicted_results_dict = json.loads(cache_record[10])
            predicted_results = ConnectorResponse(**predicted_results_dict)
        except Exception:
            predicted_results = cache_record[10]

        # Reconstruct the ConnectorPromptArguments from the cache_record
        self.connector_prompt = ConnectorPromptArguments(
            prompt_index=cache_record[7],
            prompt=cache_record[8],
            target=target,
            predicted_results=predicted_results,
            duration=float(cache_record[11]),
        )
