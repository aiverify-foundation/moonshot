from dependency_injector.wiring import inject

from moonshot.src.api.api_session import api_create_session
from moonshot.src.runners.runner import Runner

from .... import api as moonshot_api
from ..schemas.session_create_dto import SessionCreateDTO
from ..schemas.session_prompt_dto import SessionPromptDTO
from ..schemas.session_response_model import (
    PromptResponseModel,
    SessionMetadataModel,
    SessionResponseModel,
)
from ..services.runner_service import RunnerService
from ..services.utils.exceptions_handler import exception_handler
from ..status_updater.interface.redteam_progress_callback import (
    InterfaceRedTeamProgressCallback,
)
from .base_service import BaseService


class SessionService(BaseService):
    active_runner: Runner

    @inject
    def __init__(
        self,
        progress_status_updater: InterfaceRedTeamProgressCallback,
        runner_service: RunnerService,
    ) -> None:
        """
        Initialize the SessionService with dependencies.

        Args:
            progress_status_updater (InterfaceRedTeamProgressCallback): The callback interface for progress updates.
            runner_service (RunnerService): The service for managing runners.
        """
        self.progress_status_updater = progress_status_updater
        self.runner_service = runner_service
        super().__init__()

    @exception_handler
    def create_new_session(
        self, session_create_dto: SessionCreateDTO
    ) -> SessionMetadataModel:
        """
        Create a new session with a new runner and return the session metadata.

        Args:
            session_create_dto (SessionCreateDTO): Data transfer object containing session creation details.

        Returns:
            SessionMetadataModel: The metadata of the newly created session.
        """
        # Create a new runner instance using the runner service
        runner = self.runner_service.create_runner(
            runner_name=session_create_dto.name,
            endpoints=session_create_dto.endpoints,
            description=session_create_dto.description,
        )
        self.active_runner = runner

        # Prepare runner arguments for session creation
        runner_args = {
            "context_strategy": session_create_dto.context_strategy,
            "prompt_template": session_create_dto.prompt_template,
        }

        # Create a new session if the runner has a database instance
        if runner.database_instance:
            api_create_session(
                runner.id, runner.database_instance, runner.endpoints, runner_args
            )

        # Load and return the session metadata
        session_metadata_dict = moonshot_api.api_load_session(runner.id)
        if session_metadata_dict is None:
            raise ValueError(f"No session metadata found for runner ID {runner.id}")

        return SessionMetadataModel(**session_metadata_dict)

    @exception_handler
    def get_all_session(self) -> list[SessionMetadataModel]:
        """
        Retrieve all session metadata.

        Returns:
            list[SessionMetadataModel]: A list of session metadata models for all sessions.
        """
        sessions_metadata_dicts = moonshot_api.api_get_all_session_metadata()
        return [
            SessionMetadataModel(**metadata) for metadata in sessions_metadata_dicts
        ]

    @exception_handler
    def get_all_sessions_names(self) -> list[str]:
        """
        Retrieve a list of all session names.

        This method calls the moonshot API to get the names of all sessions and returns them.

        Returns:
            list[str]: A list of session names.
        """
        sessions = moonshot_api.api_get_all_session_names()
        return sessions

    @exception_handler
    def get_session_by_runner_id(
        self, runner_id: str, include_history: bool
    ) -> SessionResponseModel:
        """
        Retrieve session information by runner ID, optionally including chat history.

        Args:
            runner_id (str): The unique identifier of the runner.
            include_history (bool): Flag to determine if chat history should be included.

        Returns:
            SessionResponseModel: An object containing session metadata and optionally chat records.
        """
        runner: Runner = self.runner_service.load_runner(runner_id)
        self.active_runner = runner
        session_metadata_dict = moonshot_api.api_load_session(self.active_runner.id)

        if not isinstance(session_metadata_dict, dict):
            raise ValueError(
                f"Session metadata for runner ID {runner.id} must be a dictionary."
            )

        session_metadata = SessionMetadataModel(**session_metadata_dict)

        session_chat = (
            moonshot_api.api_get_all_chats_from_session(runner.id)
            if include_history
            else None
        )

        return SessionResponseModel(session=session_metadata, chat_records=session_chat)

    @exception_handler
    def update_session_chat(self, runner_id: str):
        """
        Update the chat for the current session.

        Args:
            runner_id (str): The unique identifier of the runner.

        Returns:
            The updated chat records for the session.
        """
        if self.active_runner.id != runner_id:
            raise RuntimeError("Active session and requested session do not match.")
        session_chat = moonshot_api.api_get_all_chats_from_session(
            self.active_runner.id
        )
        return session_chat

    @exception_handler
    def delete_session(self, runner_id: str) -> None:
        """
        Delete a session by runner ID.

        This method calls the moonshot API to delete the session associated with the given runner ID.

        Args:
            runner_id (str): The unique identifier of the runner whose session is to be deleted.
        """
        moonshot_api.api_delete_session(runner_id)

    @exception_handler
    def select_prompt_template(self, runner_id: str, prompt_template_name: str = ""):
        """
        Select a prompt template for the current session.

        Args:
            runner_id (str): The unique identifier of the runner.
            prompt_template_name (str): The name of the prompt template to be selected.
        """
        if self.active_runner.id != runner_id:
            raise RuntimeError("Active session and requested session do not match.")
        moonshot_api.api_update_prompt_template(
            self.active_runner.id, prompt_template_name
        )

    @exception_handler
    def select_ctx_strategy(
        self, runner_id: str, ctx_strategy_name: str = "", num_of_prompt: int = 5
    ) -> None:
        """
        Select a context strategy for the current session.

        Args:
            runner_id (str): The unique identifier of the runner.
            ctx_strategy_name (str): The name of the context strategy to be selected.
            num_of_prompt (int): The number of previous prompts to consider in the strategy.
        """
        if self.active_runner.id != runner_id:
            raise RuntimeError("Active session and requested session do not match.")
        moonshot_api.api_update_context_strategy(
            self.active_runner.id, ctx_strategy_name
        )
        moonshot_api.api_update_cs_num_of_prev_prompts(
            self.active_runner.id, num_of_prompt
        )

    @exception_handler
    def select_attack_module(self, runner_id: str, attack_module_name: str = ""):
        """
        Select an attack module for the current session.

        Args:
            runner_id (str): The unique identifier of the runner.
            attack_module_name (str): The name of the attack module to be selected.
        """
        if self.active_runner.id != runner_id:
            raise RuntimeError("Active session and requested session do not match.")
        moonshot_api.api_update_attack_module(self.active_runner.id, attack_module_name)

    @exception_handler
    def select_metric(self, runner_id: str, metric_name: str = ""):
        """
        Select a metric for the current session.

        Args:
            runner_id (str): The unique identifier of the runner.
            metric_name (str): The name of the metric to be selected.
        """
        if self.active_runner.id != runner_id:
            raise RuntimeError("Active session and requested session do not match.")
        moonshot_api.api_update_metric(self.active_runner.id, metric_name)

    @exception_handler
    def update_system_prompt(self, runner_id: str, system_prompt: str = ""):
        """
        Update the system prompt for the current session.

        Args:
            runner_id (str): The unique identifier of the runner.
            system_prompt (str): The new system prompt to be set.
        """
        if self.active_runner.id != runner_id:
            raise RuntimeError("Active session and requested session do not match.")
        moonshot_api.api_update_system_prompt(self.active_runner.id, system_prompt)

    @exception_handler
    async def send_prompt(
        self, runner_id: str, prompt: SessionPromptDTO
    ) -> PromptResponseModel:
        """
        Send a prompt to the runner for processing.

        Args:
            runner_id (str): The unique identifier of the runner.
            prompt (SessionPromptDTO): The prompt data transfer object containing user prompt details.

        Returns:
            The result of the red teaming operation initiated by the prompt.
        """
        if self.active_runner.id != runner_id:
            raise RuntimeError("Active session and requested session do not match.")

        session_metadata = moonshot_api.api_load_session(self.active_runner.id)
        if session_metadata is None:
            raise RuntimeError(
                f"No session metadata found for runner ID: {self.active_runner.id}"
            )

        def get_metadata_value(key, default=""):
            return session_metadata.get(key, default)

        prompt_template = get_metadata_value("prompt_template")
        context_strategy = get_metadata_value("context_strategy")
        num_of_prev_prompts = get_metadata_value("cs_num_of_prev_prompts")
        attack_module = get_metadata_value("attack_module")
        system_prompt = get_metadata_value("system_prompt")
        metric = get_metadata_value("metric")

        rt_args = {
            "prompt": prompt.user_prompt,
            "system_prompt": system_prompt,
            "context_strategy_info": [
                {
                    "context_strategy_id": context_strategy,
                    "num_of_prev_prompts": num_of_prev_prompts,
                }
            ]
            if context_strategy
            else [],
            "prompt_template_ids": [prompt_template] if prompt_template else [],
        }

        if attack_module:
            rt_args["attack_module_id"] = attack_module
            rt_args["metric_ids"] = [metric] if metric else []
            await self.active_runner.run_red_teaming({"attack_strategies": rt_args})
        else:
            await self.active_runner.run_red_teaming({"manual_rt_args": rt_args})

        retn_val = self.update_session_chat(self.active_runner.id)
        return retn_val

    @exception_handler
    async def end_session(self, runner_id: str):
        """
        End the current session.

        Args:
            runner_id (str): The unique identifier of the runner whose session is to be ended.
        """
        if self.active_runner.id != runner_id:
            raise RuntimeError("Active session and requested session do not match.")

        self.active_runner.close()
