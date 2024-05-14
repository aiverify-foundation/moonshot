import datetime as dt
from datetime import datetime
from typing import Callable

from moonshot.src.runs.run_status import RunStatus


class RedTeamingProgress:
    DEFAULT_CHAT_BATCH_SIZE = 5

    def __init__(
        self,
        runner_id: str,
        red_teaming_arguments: dict,
        run_progress_callback_func: Callable | None,
    ):
        # Information on the run and callback for progress updating
        self.runner_id = runner_id
        self.am_id = red_teaming_arguments.get("am_id", "")
        self.cs_id = red_teaming_arguments.get("cs_id", "")
        self.pt_id = red_teaming_arguments.get("pt_id", "")
        self.chat_batch_size = red_teaming_arguments.get(
            "chat_batch_size", RedTeamingProgress.DEFAULT_CHAT_BATCH_SIZE
        )
        self.chats = red_teaming_arguments.get("chats", {})
        self.current_count = 0
        self.run_progress_callback_func = run_progress_callback_func
        self.status = RunStatus.PENDING

    def update_red_teaming_chats(
        self, red_teaming_prompt_arguments: dict, run_status: RunStatus
    ) -> None:
        """
        This method updates the red teaming chats with the provided arguments and run status.

        It calculates the response time by adding the duration to the start time. Then, it creates a dictionary
        with the prompt, response, prompt time, and response time. This dictionary is then added to the chats.

        Args:
            red_teaming_prompt_arguments (dict): A dictionary containing the arguments for the red teaming prompt.
            It should contain all keys in AttackModule.RedTeamingPromptArguments, which are mainly:
                - conn_id (str): The connection ID of the chat
                - cs_id (str): The context strategy ID (if any) or ""
                - pt_id (str): The prompt template ID (if any) or ""
                - am_id (str): The attack module ID
                - me_id (str): The metric ID (if any) or ""
                - original_prompt (str): The original prompt entered by the user
                - prepared_prompt(str): The modified and final prompt that was sent to the LLM
                - system_prompt (str): The system prompt entered by the user (if any)
                - response (str): The response from the LLM
                - duration (str): The amount of time it takes to get back the response from the LLM in seconds
                (in string)
                - start_time (str): The datetime of the prompt (in string)

            - run_status (RunStatus): The current status of the run.

        Returns:
            None
        """
        prompt_time = datetime.fromisoformat(red_teaming_prompt_arguments["start_time"])
        delta = dt.timedelta(seconds=float(red_teaming_prompt_arguments["duration"]))
        response_time = prompt_time + delta
        prompt_response_dict = {
            "prompt": red_teaming_prompt_arguments["prepared_prompt"],
            "response": red_teaming_prompt_arguments["response"],
            "prompt_time": red_teaming_prompt_arguments["start_time"],
            "response_time": str(response_time),
        }

        if red_teaming_prompt_arguments["conn_id"] not in self.chats:
            self.chats[red_teaming_prompt_arguments["conn_id"]] = []
        self.chats[red_teaming_prompt_arguments["conn_id"]].append(prompt_response_dict)
        self.am_id = red_teaming_prompt_arguments.get("am_id", "")
        self.pt_id = red_teaming_prompt_arguments.get("pt_id", "")
        self.cs_id = red_teaming_prompt_arguments.get("cs_id", "")
        self.status = run_status

    def reset_chats(self) -> None:
        """
        This method clears all the chat data stored in the 'chats' attribute.
        """
        self.chats.clear()

    def notify_progress(self) -> None:
        """
        This method checks if a callback function for run progress exists and if so,
        it calls the function with the current state of the red teaming progress.
        """
        if self.run_progress_callback_func:
            self.run_progress_callback_func(self.get_dict())

    def get_dict(self) -> dict:
        """
        This method returns a dictionary representation of the current state of the red teaming progress.

        The dictionary includes the following keys:
        - "current_runner_id": The ID of the current runner.
        - "current_am_id": The ID of the current attack module.
        - "current_pt_id": The ID of the current prompt template.
        - "current_cs_id": The ID of the current context strategy.
        - "current_chats": The chats that will be returned during a callback.
        - "current_batch_size": The current batch size, which indicates the number of chats returned during a callback.
        - "current_status": The current status of the run.

        Returns:
            dict: A dictionary representation of the current state of the red teaming progress.
        """
        return {
            "current_runner_id": self.runner_id,
            "current_am_id": self.am_id,
            "current_pt_id": self.pt_id,
            "current_cs_id": self.cs_id,
            "current_chats": self.chats,
            "current_batch_size": self.chat_batch_size,
            "current_status": self.status.name,
        }
