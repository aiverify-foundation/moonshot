import asyncio
import uuid
from typing import Callable

from moonshot.src.benchmark.task.task_config import TaskConfig
from moonshot.src.benchmark.task.task_processor import TaskProcessor
from moonshot.src.connectors.connector import Connector
from moonshot.src.cookbooks.cookbook import Cookbook
from moonshot.src.messages_constants import (
    TASK_GENERATOR_CREATE_TASKS_DEBUG,
    TASK_GENERATOR_CREATE_TASKS_INVALID_TASKS_PROMPTS_EXCEPTION_ERROR,
    TASK_GENERATOR_GENERATE_TASKS_INVALID_COOKBOOK_EXCEPTION_ERROR,
    TASK_GENERATOR_GENERATE_TASKS_INVALID_RECIPE_EXCEPTION_ERROR,
)
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class TaskGenerator:
    def __init__(
        self,
        cancel_event: asyncio.Event,
        concurrency_limit: int,
        connectors: list[Connector],
        cookbook_names: list[str],
        database_instance: DBInterface,
        prompt_selection_percentage: int,
        random_seed: int,
        recipe_names: list[str],
        task_progress_fn: Callable,
        use_cache: bool,
    ):
        """
        Set up the TaskGenerator with the given settings.

        Args:
            cancel_event (asyncio.Event): Event to stop tasks if needed.
            concurrency_limit (int): Max number of tasks to run at the same time.
            connectors (list[Connector]): List of connector instances.
            cookbook_names (list[str]): List of cookbook names.
            database_instance (DBInterface): Database interface instance.
            prompt_selection_percentage (int): Percentage of prompts to select.
            random_seed (int): Seed for random operations.
            recipe_names (list[str]): List of recipe names.
            task_progress_fn (Callable): Function to update task progress.
            use_cache (bool): Whether to use cache.
        """
        # Event to signal task cancellation
        self.cancel_event = cancel_event

        # Limit for task concurrency
        self.concurrency_limit = concurrency_limit

        # List of connector instances
        self.connectors = connectors

        # List of cookbook names
        self.cookbook_names = cookbook_names

        # Database interface instance
        self.database_instance = database_instance

        # Percentage of prompts to select
        self.prompt_selection_percentage = prompt_selection_percentage

        # Seed value for random operations
        self.random_seed = random_seed

        # List of recipe names
        self.recipe_names = recipe_names

        # Callback function to handle task progress updates
        self.task_progress_fn = task_progress_fn

        # Flag indicating whether to use cache
        self.use_cache = use_cache

    async def create_tasks(self) -> tuple[bool, dict]:
        """
        Create tasks and their prompts asynchronously.

        This method generates tasks and their prompts, checks if there are any tasks or prompts,
        and returns a tuple with a success flag and a dictionary containing the tasks, total prompts,
        and updates for each task.

        Returns:
            tuple: A tuple containing:
                - bool: Success flag indicating if tasks were created successfully.
                - dict: A dictionary containing:
                    - 'tasks' (list): List of created tasks.
                    - 'tasks_prompts' (int): Total number of prompts.
                    - 'tasks_updates' (dict): Dictionary with task UUIDs as keys and empty dictionaries as values.
        """
        # Log the start of task creation
        logger.debug(TASK_GENERATOR_CREATE_TASKS_DEBUG)

        # Generate benchmarking tasks and prompts
        benchmark_tasks, benchmark_tasks_prompts = await self.generate_tasks()

        # Verify if there are tasks or prompts available for processing
        if not benchmark_tasks or benchmark_tasks_prompts == 0:
            # Log a warning if no tasks or prompts are available
            logger.warning(
                TASK_GENERATOR_CREATE_TASKS_INVALID_TASKS_PROMPTS_EXCEPTION_ERROR
            )
            is_success = False
            benchmark_tasks = []
            benchmark_tasks_prompts = 0
            benchmark_tasks_updates = {}
        else:
            # Create a dictionary with task UUIDs as keys and empty dictionaries as values
            is_success = True
            benchmark_tasks_updates = {task.task_uuid: {} for task in benchmark_tasks}

        # Return the success flag and the generated tasks, total prompts, and task updates
        return is_success, {
            "tasks": benchmark_tasks,
            "tasks_prompts": benchmark_tasks_prompts,
            "tasks_updates": benchmark_tasks_updates,
        }

    async def generate_tasks(self) -> tuple[list[TaskProcessor], int]:
        """
        Make tasks based on the given cookbooks and recipes.

        This method goes through each cookbook and recipe to create a list of TaskProcessor instances
        and counts the total number of prompts.

        Returns:
            tuple: A tuple containing:
                - list[TaskProcessor]: List of TaskProcessor instances.
                - int: Total number of prompts.
        """
        new_tasks: list[TaskProcessor] = []
        total_number_of_tasks_prompts: int = 0

        # Process each cookbook to generate tasks
        if self.cookbook_names:
            for cookbook_name in self.cookbook_names:
                try:
                    # Load the cookbook by name
                    cookbook = Cookbook.load(cookbook_name)
                    for recipe_name in cookbook.recipes:
                        # Generate new tasks for each recipe in the cookbook
                        (
                            generated_tasks,
                            generated_tasks_num_of_prompts,
                        ) = await self.generate_new_task(recipe_name, cookbook)

                        # Add the generated tasks to the new tasks list
                        new_tasks.extend(generated_tasks)
                        # Update the total number of prompts
                        total_number_of_tasks_prompts += generated_tasks_num_of_prompts

                except Exception as e:
                    # Raise a runtime error if there is an issue with the cookbook
                    raise RuntimeError(
                        TASK_GENERATOR_GENERATE_TASKS_INVALID_COOKBOOK_EXCEPTION_ERROR.format(
                            cookbook_name=cookbook_name, message=str(e)
                        )
                    )

        # Process each standalone recipe to generate tasks
        if self.recipe_names:
            for recipe_name in self.recipe_names:
                try:
                    # Generate new tasks for the standalone recipe
                    (
                        generated_tasks,
                        generated_tasks_num_of_prompts,
                    ) = await self.generate_new_task(recipe_name)

                    # Add the generated tasks to the new tasks list
                    new_tasks.extend(generated_tasks)
                    # Update the total number of prompts
                    total_number_of_tasks_prompts += generated_tasks_num_of_prompts

                except Exception as e:
                    # Raise a runtime error if there is an issue with the recipe
                    raise RuntimeError(
                        TASK_GENERATOR_GENERATE_TASKS_INVALID_RECIPE_EXCEPTION_ERROR.format(
                            recipe_name=recipe_name, message=str(e)
                        )
                    )

        return new_tasks, total_number_of_tasks_prompts

    async def generate_new_task(
        self, recipe_name: str, cookbook: Cookbook | None = None
    ) -> tuple[list[TaskProcessor], int]:
        """
        Make new tasks based on the given recipe.

        This method creates a list of TaskProcessor instances for each connector and prompt template
        combination in the recipe. It also counts the total number of prompts.

        Args:
            recipe_name (str): Name of the recipe to load and make tasks from.
            cookbook (Cookbook | None): Cookbook instance for the recipe, if any.

        Returns:
            tuple: A tuple containing:
                - list[TaskProcessor]: List of TaskProcessor instances.
                - int: Total number of prompts.
        """
        new_tasks: list[TaskProcessor] = []
        new_tasks_num_of_prompts: int = 0
        recipe: Recipe = Recipe.load(recipe_name)

        # Create tasks for each connector and prompt template combination
        for connector in self.connectors:
            for prompt_template in recipe.prompt_templates:
                new_task = TaskProcessor(
                    TaskConfig(
                        cancel_event=self.cancel_event,
                        connector=connector,
                        cookbook=cookbook,
                        database=self.database_instance,
                        recipe=recipe,
                        task_concurrency_limit=self.concurrency_limit,
                        task_progress_fn=self.task_progress_fn,
                        task_prompt_augmented_template_id=prompt_template,
                        task_prompt_selection_percentage=self.prompt_selection_percentage,
                        task_random_seed=self.random_seed,
                        task_uuid=uuid.uuid4(),
                        use_cache=self.use_cache,
                    )
                )
                await new_task.generate_prompts()

                new_tasks.append(new_task)
                new_tasks_num_of_prompts += await new_task.num_of_prompts_total.get()

        return new_tasks, new_tasks_num_of_prompts
