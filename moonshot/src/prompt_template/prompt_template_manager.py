import glob
import json
from pathlib import Path

from jinja2 import Template
from moonshot.src.configs.env_variables import EnvironmentVars


class PromptTemplateManager:
    def __init__(self):
        pass

    @staticmethod
    def get_all_prompt_template_names() -> list[str]:
        """
        Retrieve the names of all prompt templates available.

        Returns:
            list: A list of prompt template names.
        """
        try:
            prompt_template_file_path = f"{EnvironmentVars.PROMPT_TEMPLATES}"
            filepaths = [
                Path(fp).stem
                for fp in glob.iglob(f"{prompt_template_file_path}/*.json")
                if "__" not in fp
            ]
            return filepaths
        except Exception as e:
            raise e

    @staticmethod
    def get_all_prompt_template_details() -> list[dict]:
        """
        Retrieve details of all prompt templates available.

        Returns:
            list[dict]: A list of dictionaries containing the details of each prompt template.
        """
        list_of_pt_names = PromptTemplateManager.get_all_prompt_template_names()
        list_of_pt_contents = []
        for pt_name in list_of_pt_names:
            try:
                pt_file = open(
                    f"{EnvironmentVars.PROMPT_TEMPLATES}/{pt_name}.json",
                    "r",
                    encoding="utf-8",
                )
                pt_contents = json.load(pt_file)
                name = pt_contents["name"]
                description = pt_contents["description"]
                template = pt_contents["template"]
                list_of_pt_contents.append(
                    {"name": name, "description": description, "template": template}
                )
            except (FileNotFoundError, ValueError) as e:
                raise e
        return list_of_pt_contents

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
        try:
            prompt_template_file = (
                f"{EnvironmentVars.PROMPT_TEMPLATES}/{prompt_template_name}.json"
            )
            with open(prompt_template_file, "r", encoding="utf-8") as json_file:
                prompt_template_details = json.load(json_file)
                template = prompt_template_details["template"]
                jinja_template = Template(template)
                return jinja_template.render({"prompt": user_prompt})
        except Exception as e:
            raise e
