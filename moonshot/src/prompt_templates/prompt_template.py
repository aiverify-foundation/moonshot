from pathlib import Path

from jinja2 import Template

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class PromptTemplate:
    def __init__(self):
        pass

    @staticmethod
    def get_all_prompt_template_names() -> list[str]:
        """
        Retrieve the names of all prompt templates available.

        Returns:
            list: A list of prompt template names.
        """

        filepaths = []
        prompt_template_files = Storage.get_objects(
            EnvVariables.PROMPT_TEMPLATES.name, "json"
        )
        for prompt_template in prompt_template_files:
            filepaths.append(Path(prompt_template).stem)
        return filepaths

    @staticmethod
    def get_all_prompt_template_details() -> list[dict]:
        """
        Retrieve details of all prompt templates available.

        Returns:
            list[dict]: A list of dictionaries containing the details of each prompt template.
        """
        list_of_pt_names = PromptTemplate.get_all_prompt_template_names()
        list_of_pt_contents = []

        for pt_name in list_of_pt_names:
            pt_contents = Storage.read_object(
                EnvVariables.PROMPT_TEMPLATES.name, pt_name, "json"
            )
            id = pt_name
            name = pt_contents["name"]
            description = pt_contents["description"]
            template = pt_contents["template"]
            list_of_pt_contents.append(
                {
                    "id": id,
                    "name": name,
                    "description": description,
                    "template": template,
                }
            )
        return list_of_pt_contents

    @staticmethod
    def delete(pt_id: str) -> bool:
        """
        Deletes a prompt template identified by its unique ID.

        This method attempts to delete the prompt template with the given ID from the storage.
        If the deletion is successful, it returns True. If an exception occurs during the deletion
        process, it prints an error message and re-raises the exception.

        Args:
            pt_id (str): The unique identifier of the prompt template to be deleted.

        Returns:
            bool: True if the prompt template was successfully deleted.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            Storage.delete_object(EnvVariables.PROMPT_TEMPLATES.name, pt_id, "json")
            return True

        except Exception as e:
            logger.error(f"Failed to delete prompt template: {str(e)}")
            raise e

    @staticmethod
    def process_prompt_pt(user_prompt: str, prompt_template_name: str) -> str:
        """
        Process a user prompt using a specified prompt template.

        Args:
            user_prompt (str): The user prompt to process.
            prompt_template (str): The name of the prompt template to use.

        Returns:
            str: The processed user prompt based on the template.
        """

        prompt_template_file = Storage.read_object(
            EnvVariables.PROMPT_TEMPLATES.name, prompt_template_name, "json"
        )
        template = prompt_template_file["template"]
        jinja_template = Template(template)
        return jinja_template.render({"prompt": user_prompt})
