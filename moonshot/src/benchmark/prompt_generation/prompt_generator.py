import asyncio
import random
import uuid
from typing import AsyncGenerator, Callable

from jinja2 import Template

from moonshot.src.benchmark.prompt_generation.prompt_config import PromptConfig
from moonshot.src.benchmark.prompt_generation.prompt_processor import PromptProcessor
from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors.connector import Connector
from moonshot.src.datasets.dataset import Dataset
from moonshot.src.messages_constants import PROMPT_GENERATION_GET_DATASET_PROMPTS
from moonshot.src.recipes.recipe import Recipe
from moonshot.src.storage.db_interface import DBInterface
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class PromptGenerator:
    async def load_prompt_templates(self, name: str) -> dict[str, str]:
        """
        Load prompt templates from storage.

        This method reads a JSON object from storage using the provided name and
        extracts the template information.

        Args:
            name (str): The name of the prompt template to load.

        Returns:
            dict[str, str]: A dictionary containing the template name as the key and the template string as the value.
        """
        # Read the JSON object from storage using the provided name
        pt_info = Storage.read_object(EnvVariables.PROMPT_TEMPLATES.name, name, "json")

        # Extract and return the template information as a dictionary
        return {name: pt_info["template"]}

    async def create_prompts(
        self,
        cancel_event: asyncio.Event,
        connector: Connector,
        db_instance: DBInterface,
        prompt_progress_fn: Callable,
        prompt_selection_percentage: int,
        prompt_template: str,
        random_seed: int,
        recipe_instance: Recipe,
        use_cache: bool,
    ) -> tuple[int, AsyncGenerator[PromptProcessor, None]]:
        """
        Asynchronously generate prompts and provide the total count with a generator.

        This method loads prompt templates from storage, calculates the total number
        of prompts to be generated, and returns both the total count and an asynchronous
        generator for the prompts.

        Args:
            cancel_event (asyncio.Event): An event to signal prompt generation cancellation.
            connector (Connector): The connector instance used for processing prompts.
            db_instance (DBInterface): The database interface for storing and retrieving data.
            prompt_progress_fn (Callable): A callback function to handle prompt progress updates.
            prompt_selection_percentage (int): The percentage of prompts to select from the dataset.
            prompt_template (str): The name of the prompt template to use.
            random_seed (int): The seed value for random selection of prompts.
            recipe_instance (Recipe): The recipe instance containing dataset information.
            use_cache (bool): A flag indicating whether to use cached prompts.

        Returns:
            tuple[int, AsyncGenerator[PromptProcessor, None]]: A tuple containing the total number
            of prompts and an asynchronous generator for creating the prompts.
        """
        templates: dict[str, str] = {}
        if prompt_template:
            # Load the prompt templates if a template name is provided
            templates = await self.load_prompt_templates(prompt_template)

        # Initialize the count of prompts to be generated
        count = 0
        async for _ in self.create_prompts_generator(
            cancel_event,
            connector,
            db_instance,
            prompt_progress_fn,
            prompt_selection_percentage,
            random_seed,
            recipe_instance,
            templates,
            use_cache,
            False,
        ):
            count += 1

        # Return the total count and the generator for creating prompts
        return count, self.create_prompts_generator(
            cancel_event,
            connector,
            db_instance,
            prompt_progress_fn,
            prompt_selection_percentage,
            random_seed,
            recipe_instance,
            templates,
            use_cache,
        )

    async def create_prompts_generator(
        self,
        cancel_event: asyncio.Event,
        connector: Connector,
        db_instance: DBInterface,
        prompt_progress_fn: Callable,
        prompt_selection_percentage: int,
        random_seed: int,
        recipe_instance: Recipe,
        templates: dict[str, str],
        use_cache: bool,
        to_log: bool = True,
    ) -> AsyncGenerator[PromptProcessor, None]:
        """
        Asynchronously generate prompts using the provided templates or yield original prompts
        if no templates are available.

        This method iterates over datasets and applies templates to render prompts.
        If no templates are available, it yields the original prompts from the datasets.

        Args:
            cancel_event (asyncio.Event): An event to signal prompt generation cancellation.
            connector (Connector): The connector instance used for processing prompts.
            db_instance (DBInterface): The database interface for storing and retrieving data.
            prompt_progress_fn (Callable): A callback function to handle prompt progress updates.
            prompt_selection_percentage (int): The percentage of prompts to select from the dataset.
            random_seed (int): The seed value for random selection of prompts.
            recipe_instance (Recipe): The recipe instance containing dataset information.
            templates (dict[str, str]): A dictionary mapping template IDs to template strings.
            use_cache (bool): A flag indicating whether to use cached prompts.
            to_log (bool): A flag indicating whether to log the number of selected prompts.

        Yields:
            PromptProcessor: An instance of PromptProcessor containing all necessary information
            for processing the prompt.
        """
        # Iterate over each dataset in the recipe instance
        for ds_id in recipe_instance.datasets:
            # Retrieve prompts from the dataset
            async for prompt_index, prompt in self.get_dataset_prompts(
                ds_id, prompt_selection_percentage, random_seed, to_log
            ):
                # If templates are provided, apply each template to the prompt
                if templates:
                    for pt_id, pt_template in templates.items():
                        actual_prompt = Template(pt_template).render(
                            {"prompt": prompt["input"]}
                        )
                        # Yield a PromptProcessor instance with the augmented content
                        yield PromptProcessor(
                            PromptConfig(
                                cancel_event=cancel_event,
                                connector=connector,
                                database=db_instance,
                                dataset_id=ds_id,
                                prompt_augmented_content=actual_prompt,
                                prompt_augmented_template_id=pt_id,
                                prompt_details=prompt,
                                prompt_evaluation_results={},
                                prompt_index=prompt_index,
                                prompt_progress_fn=prompt_progress_fn,
                                prompt_uuid=uuid.uuid4(),
                                recipe=recipe_instance,
                                use_cache=use_cache,
                            )
                        )
                else:
                    # Yield a PromptProcessor instance with the original content if no templates are available
                    yield PromptProcessor(
                        PromptConfig(
                            cancel_event=cancel_event,
                            connector=connector,
                            database=db_instance,
                            dataset_id=ds_id,
                            prompt_augmented_content=None,
                            prompt_augmented_template_id="no-template",
                            prompt_details=prompt,
                            prompt_evaluation_results={},
                            prompt_index=prompt_index,
                            prompt_progress_fn=prompt_progress_fn,
                            prompt_uuid=uuid.uuid4(),
                            recipe=recipe_instance,
                            use_cache=use_cache,
                        )
                    )

    async def get_dataset_prompts(
        self,
        ds_id: str,
        prompt_selection_percentage: int,
        random_seed: int,
        to_log: bool,
    ) -> AsyncGenerator[tuple[int, dict[str, str]], None]:
        """
        Asynchronously retrieve prompts from a dataset using the specified dataset ID.

        This method selects prompts based on the prompt_selection_percentage and random_seed.
        It yields each selected prompt along with its index.

        Args:
            ds_id (str): The unique identifier of the dataset from which to retrieve prompts.
            prompt_selection_percentage (int): The percentage of prompts to select from the dataset.
            random_seed (int): The seed value for random selection of prompts.
            to_log (bool): A flag indicating whether to log the number of selected prompts.

        Yields:
            tuple[int, dict[str, str]]: A tuple containing the index of the prompt and the prompt data.
        """
        # Retrieve dataset arguments
        ds_args = Dataset.read(ds_id)

        if ds_args.num_of_dataset_prompts == 0:
            # If there are no prompts in the dataset, set prompt_indices to an empty list
            prompt_indices = []
        else:
            # Calculate the number of prompts to select based on prompt_selection_percentage
            self.num_of_prompts = max(
                1,
                int(
                    (prompt_selection_percentage / 100) * ds_args.num_of_dataset_prompts
                ),
            )
            if self.num_of_prompts == ds_args.num_of_dataset_prompts:
                # If the number of prompts to select is equal to the total number of prompts, select all prompts
                prompt_indices = range(ds_args.num_of_dataset_prompts)
            else:
                # Randomly select a subset of prompts based on the random_seed
                random.seed(random_seed)
                prompt_indices = random.sample(
                    range(ds_args.num_of_dataset_prompts), self.num_of_prompts
                )

        if to_log:
            # Log the number of selected prompts if to_log is True
            logger.debug(
                PROMPT_GENERATION_GET_DATASET_PROMPTS.format(
                    ds_id=ds_id,
                    num_of_prompts=len(prompt_indices),
                    total_dataset_prompts=ds_args.num_of_dataset_prompts,
                )
            )

        # Iterate over the dataset examples and yield prompts based on the generated indices
        for prompts_gen_index, prompts_data in enumerate(ds_args.examples):
            if prompts_gen_index in prompt_indices:
                # Yield the index and data of each selected prompt
                yield prompts_gen_index, prompts_data
