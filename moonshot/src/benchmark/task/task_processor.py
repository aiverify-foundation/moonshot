import asyncio
from datetime import datetime

from moonshot.src.benchmark.prompt_generation.prompt_generator import PromptGenerator
from moonshot.src.benchmark.prompt_generation.prompt_processor import PromptProcessor
from moonshot.src.benchmark.task.task_config import TaskConfig
from moonshot.src.benchmark.task.task_status import TaskStatus
from moonshot.src.messages_constants import (
    TASK_PROCESSOR_GENERATE_PROMPTS_DEBUG,
    TASK_PROCESSOR_PROCESS_PROMPTS_DEBUG,
    TASK_PROCESSOR_PROCESS_PROMPTS_TASK_PROMPT_GENERATOR_NOT_PROVIDED,
    TASK_PROCESSOR_PROCESS_TASK_CANCELLED_ERROR,
    TASK_PROCESSOR_PROCESS_TASK_EXCEPTION_ERROR,
    TASK_PROCESSOR_SET_STATUS_DEBUG,
)
from moonshot.src.utils.atomic_integer import AtomicInteger
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class TaskProcessor:
    def __init__(self, config: TaskConfig):
        """
        Initializes a TaskProcessor instance using the provided configuration.

        This constructor sets up the task with all necessary attributes, including
        required and optional configurations, as well as attributes related to the task's
        unique identification and evaluation.

        Args:
            config (TaskConfig): A configuration object containing all necessary attributes for the task.
        """

        # Required attributes for task configuration
        self.cancel_event = config.cancel_event
        self.connector = config.connector
        self.cookbook = config.cookbook
        self.database = config.database
        self.recipe = config.recipe

        # Attributes related to the task's unique identification and evaluation
        self.task_concurrency_limit = config.task_concurrency_limit
        self.task_progress_fn = config.task_progress_fn
        self.task_prompt_augmented_template_id = (
            config.task_prompt_augmented_template_id
        )
        self.task_prompt_generator = None
        self.task_prompt_selection_percentage = config.task_prompt_selection_percentage
        self.task_prompt_updates = {}
        self.task_random_seed = config.task_random_seed
        self.task_semaphore = asyncio.Semaphore(config.task_concurrency_limit)
        self.task_status = TaskStatus.PENDING
        self.task_uuid = str(config.task_uuid)

        # Optional attributes for task configuration
        self.end_time = config.end_time
        self.start_time = config.start_time
        self.use_cache = config.use_cache
        if self.end_time < self.start_time:
            self.duration = 0
        else:
            self.duration = (self.end_time - self.start_time).total_seconds()

        # TaskProcessor tracking statistics
        # self.num_of_prompts_cancelled = AtomicInteger(0)
        # self.num_of_prompts_completed = AtomicInteger(0)
        # self.num_of_prompts_error = AtomicInteger(0)
        # self.num_of_prompts_pending = AtomicInteger(0)
        # self.num_of_prompts_running_metrics_calculation = AtomicInteger(0)
        # self.num_of_prompts_running_query = AtomicInteger(0)
        self.num_of_prompts_total = AtomicInteger(0)

        # # TaskProcessor prompts lists
        # self.cancelled_prompts = []
        # self.completed_prompts = []
        # self.error_prompts = []
        # self.pending_prompts = []
        # self.running_prompts = []

        # # TaskProcessor error lists
        # self.error_messages = []

    async def set_status(self, new_status: TaskStatus) -> None:
        """
        Update the status of the task and perform real-time updates if a progress function is provided.

        Args:
            new_status (TaskStatus): The new status to set for the task.
        """
        # Update the task status
        self.task_status = new_status
        logger.debug(
            TASK_PROCESSOR_SET_STATUS_DEBUG.format(
                uuid=self.task_uuid, new_status=new_status.value
            )
        )

        # If a progress function is provided, perform real-time updates
        if self.task_progress_fn:
            # Await the progress function to provide task progress
            await self.task_progress_fn(self.provide_task_progress())

    async def process_task(self) -> None:
        """
        Asynchronously process the task by executing various phases such as prompt generation and prompt processing.
        This method updates the task status and checks for cancellations at each phase.

        Raises:
            asyncio.CancelledError: If the task is explicitly cancelled by higher-level logic.
            Exception: For any other exceptions that occur during task processing.
        """
        try:
            # Set the status to RUNNING
            await self.set_status(TaskStatus.RUNNING)

            # Check if cancelled before starting
            if self.cancel_event.is_set():
                await self.set_status(TaskStatus.CANCELLED)
                return

            # Run the Prompt Processing phase
            await self.set_status(TaskStatus.RUNNING_PROMPT_PROCESSING)
            await self.process_prompts()
            await self.set_status(TaskStatus.COMPLETED_PROMPT_PROCESSING)

            # Check for cancellation after prompt processing phase
            if self.cancel_event.is_set():
                await self.set_status(TaskStatus.CANCELLED)
                return

            # Everything seems okay, mark the task as completed
            await self.set_status(TaskStatus.COMPLETED)
            self.end_time = datetime.now()

        except asyncio.CancelledError:
            # If the task was explicitly cancelled by higher-level logic
            logger.warning(
                TASK_PROCESSOR_PROCESS_TASK_CANCELLED_ERROR.format(uuid=self.task_uuid)
            )
            await self.set_status(TaskStatus.CANCELLED)
            self.end_time = datetime.now()

        except Exception as e:
            # Log the error and set the status to COMPLETED_WITH_ERRORS
            logger.error(
                TASK_PROCESSOR_PROCESS_TASK_EXCEPTION_ERROR.format(
                    uuid=self.task_uuid, message=str(e)
                )
            )
            await self.set_status(TaskStatus.COMPLETED_WITH_ERRORS)
            self.end_time = datetime.now()

    async def generate_prompts(self) -> None:
        """
        Asynchronously generate prompts for the task.

        This method initializes a PromptGenerator instance, creates prompts using the provided
        configuration, and updates the total number of prompts.

        Raises:
            Exception: If an error occurs during prompt creation.
        """
        # Log the start of the prompt generation process
        logger.debug(TASK_PROCESSOR_GENERATE_PROMPTS_DEBUG.format(uuid=self.task_uuid))

        # Initialize the PromptGenerator
        prompts_generator = PromptGenerator()

        # Create prompts using the PromptGenerator
        num_of_prompts, prompts_generator = await prompts_generator.create_prompts(
            self.cancel_event,
            self.connector,
            self.database,
            self.handle_prompt_progress,
            self.task_prompt_selection_percentage,
            self.task_prompt_augmented_template_id,
            self.task_random_seed,
            self.recipe,
            self.use_cache,
        )

        # Update the task's prompts generator and total number of prompts
        self.task_prompt_generator = prompts_generator
        await self.num_of_prompts_total.set(num_of_prompts)

    async def process_prompts(self) -> None:
        """
        Asynchronously process all prompts for the task.

        This method logs the start of the prompt processing, checks if the prompt generator
        is provided, and creates tasks for processing each prompt with a concurrency limit.

        Raises:
            RuntimeError: If the prompt generator is not provided.
        """
        # Log the start of the prompt processing
        logger.debug(TASK_PROCESSOR_PROCESS_PROMPTS_DEBUG.format(uuid=self.task_uuid))

        # Check if the prompt generator is provided
        if not self.task_prompt_generator:
            raise RuntimeError(
                TASK_PROCESSOR_PROCESS_PROMPTS_TASK_PROMPT_GENERATOR_NOT_PROVIDED
            )

        # Define an asynchronous function to process each prompt with concurrency limit
        async def limited_process_prompt(prompt: PromptProcessor):
            async with self.task_semaphore:
                # Update the task prompt updates with the current prompt UUID
                self.task_prompt_updates.update({prompt.prompt_uuid: {}})
                # Process the current prompt
                await prompt.process_prompt()

        # Create asyncio tasks for processing each prompt
        asyncio_tasks = []
        async for prompt in self.task_prompt_generator:
            asyncio_tasks.append(asyncio.create_task(limited_process_prompt(prompt)))
            break
        # asyncio_tasks = [
        #     asyncio.create_task(limited_process_prompt(prompt))
        #     async for prompt in self.task_prompt_generator
        # ]

        # Wait for all tasks to complete (partial-failure approach with return_exceptions=True)
        await asyncio.gather(*asyncio_tasks, return_exceptions=True)

    async def handle_prompt_progress(self, prompt_progress: dict) -> None:
        """
        Handle and print the progress of a specific prompt.

        This method is called to provide updates on the progress of prompt processing.

        Args:
            prompt_progress (dict): A dictionary containing the progress update for the prompt.
        """
        print("*" * 10, "TaskProcessor::handle_prompt_progress", "*" * 10)
        print(prompt_progress)

    def provide_task_progress(self) -> dict:
        """
        Provides a dictionary with the current progress and status of the task.

        This method gathers all essential information for an update, including
        the task's UUID, current status, and other relevant details.

        Returns:
            dict: A dictionary containing the current progress and status of the task.
        """
        return {}


#     async def handle_prompt_progress(
#         self, prompt_uuid: uuid.UUID, prompt_update: dict
#     ) -> None:
#         """
#         Asynchronously handle and update the progress of a specific prompt.

#         This method updates the prompt progress with the provided prompt update and
#         aggregates the progress data from all prompts to notify the overall task processor progress.

#         Args:
#             prompt_uuid (uuid.UUID): The unique identifier for the prompt.
#             prompt_update (dict): A dictionary containing the progress update for the prompt.
#         """
#         if prompt_uuid and prompt_update:
#             self.prompts_updates.update({prompt_uuid: prompt_update})

#             # Temporary structures to aggregate the progress results
#             temp_num_of_prompts_cancelled = AtomicInteger(0)
#             temp_num_of_prompts_completed = AtomicInteger(0)
#             temp_num_of_prompts_error = AtomicInteger(0)
#             temp_num_of_prompts_pending = AtomicInteger(0)
#             temp_num_of_prompts_running_metrics_calculation = AtomicInteger(0)
#             temp_num_of_prompts_running_query = AtomicInteger(0)
#             temp_num_of_prompts_total = AtomicInteger(0)
#             # Lists to store task processor prompts
#             temp_cancelled_prompts = []
#             temp_completed_prompts = []
#             temp_error_prompts = []
#             temp_pending_prompts = []
#             temp_running_prompts = []
#             # List to store task processor error messages
#             temp_error_messages = []

#             # Aggregate progress data from all prompts
#             for prompt in self.prompts_updates.values():
#                 temp_cancelled_prompts.extend(prompt["cancelled_prompts"])
#                 temp_completed_prompts.extend(prompt["completed_prompts"])
#                 temp_error_messages.extend(prompt["current_error_messages"])
#                 temp_error_prompts.extend(prompt["error_prompts"])
#                 await temp_num_of_prompts_cancelled.increment(
#                     prompt["num_of_prompts_cancelled"]
#                 )
#                 await temp_num_of_prompts_completed.increment(
#                     prompt["num_of_prompts_completed"]
#                 )
#                 await temp_num_of_prompts_error.increment(
#                     prompt["num_of_prompts_error"]
#                 )
#                 await temp_num_of_prompts_pending.increment(
#                     prompt["num_of_prompts_pending"]
#                 )
#                 await temp_num_of_prompts_running_metrics_calculation.increment(
#                     prompt["num_of_prompts_running_metrics_calculation"]
#                 )
#                 await temp_num_of_prompts_running_query.increment(
#                     prompt["num_of_prompts_running_query"]
#                 )
#                 await temp_num_of_prompts_total.increment(
#                     prompt["num_of_prompts_total"]
#                 )
#                 temp_pending_prompts.extend(prompt["pending_prompts"])
#                 temp_running_prompts.extend(prompt["running_prompts"])

#             self.cancelled_prompts = temp_cancelled_prompts
#             self.completed_prompts = temp_completed_prompts
#             self.error_messages = temp_error_messages
#             self.error_prompts = temp_error_prompts
#             self.num_of_prompts_cancelled = temp_num_of_prompts_cancelled
#             self.num_of_prompts_completed = temp_num_of_prompts_completed
#             self.num_of_prompts_error = temp_num_of_prompts_error
#             self.num_of_prompts_pending = temp_num_of_prompts_pending
#             self.num_of_prompts_running_metrics_calculation = (
#                 temp_num_of_prompts_running_metrics_calculation
#             )
#             self.num_of_prompts_running_query = temp_num_of_prompts_running_query
#             self.num_of_prompts_total = temp_num_of_prompts_total
#             self.pending_prompts = temp_pending_prompts
#             self.running_prompts = temp_running_prompts

#             if temp_error_messages:
#                 self.task_status = TaskStatus.RUNNING_WITH_ERRORS

#             # Notify the run progress with the aggregated results
#             if self.progress_callback_fn:
#                 await self.progress_callback_fn(self.uuid, self.provide_task_progress())

# async def provide_task_progress(self) -> dict:
#     """
#     Asynchronously retrieves the current progress update of the benchmarking task processor.

#     This method gathers and returns the current state of various prompt categories
#     and error messages associated with the task processor.

#     Returns:
#         dict: A dictionary containing the current progress of the task processor, including:
#             - num_of_prompts_cancelled: Number of prompts that were cancelled.
#             - num_of_prompts_completed: Number of prompts that were completed.
#             - num_of_prompts_error: Number of prompts that encountered errors.
#             - num_of_prompts_pending: Number of prompts that are pending.
#             - num_of_prompts_running_metrics_calculation: Number of prompts currently running metrics calculation.
#             - num_of_prompts_running_query: Number of prompts currently running queries.
#             - num_of_prompts_total: Total number of prompts.
#             - cancelled_prompts: List of cancelled prompts.
#             - completed_prompts: List of completed prompts.
#             - error_prompts: List of prompts that encountered errors.
#             - pending_prompts: List of pending prompts.
#             - running_prompts: List of prompts that are currently running.
#             - current_error_messages: List of current error messages.
#             - task_metadata: Metadata related to the task processor.
#     """
#     return {}
# return {
#     "task_metadata": {
#         "cancel_event": self.cancel_event,
#         "concurrency_limit": self.concurrency_limit,
#         "connector": self.connector,
#         "cookbook_name": self.cookbook_name,
#         "database_instance": self.database_instance,
#         "end_time": self.end_time,
#         "progress_callback_fn": self.progress_callback_fn,
#         "prompt_selection_percentage": self.prompt_selection_percentage,
#         "prompt_template": self.prompt_template,
#         "random_seed": self.random_seed,
#         "recipe": self.recipe,
#         "recipe_name": self.recipe_name,
#         "start_time": self.start_time,
#         "task_status": self.task_status,
#         "task_uuid": self.uuid,
#         "use_cache": self.use_cache,
#     },
#     "cancelled_prompts": self.cancelled_prompts,
#     "completed_prompts": self.completed_prompts,
#     "current_error_messages": self.error_messages,
#     "error_prompts": self.error_prompts,
#     "num_of_prompts_cancelled": await self.num_of_prompts_cancelled.get(),
#     "num_of_prompts_completed": await self.num_of_prompts_completed.get(),
#     "num_of_prompts_error": await self.num_of_prompts_error.get(),
#     "num_of_prompts_pending": await self.num_of_prompts_pending.get(),
#     "num_of_prompts_running_metrics_calculation": await self.num_of_prompts_running_metrics_calculation.get(),
#     "num_of_prompts_running_query": await self.num_of_prompts_running_query.get(),
#     "num_of_prompts_total": await self.num_of_prompts_total.get(),
#     "pending_prompts": self.pending_prompts,
#     "running_prompts": self.running_prompts,
# }
