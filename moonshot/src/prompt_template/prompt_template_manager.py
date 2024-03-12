import glob
from pathlib import Path
from moonshot.src.configs.env_variables import EnvironmentVars
import json


class PromptTemplateManager:
    def __init__(self):
        pass

    @staticmethod
    def get_all_prompt_template_names() -> list:
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
                pt_file = open(f"{EnvironmentVars.PROMPT_TEMPLATES}/{pt_name}.json")
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
