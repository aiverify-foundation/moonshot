import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException, Query

from ..container import Container
from ..schemas.prompt_response_model import PromptResponseModel
from ..schemas.session_create_dto import SessionCreateDTO
from ..schemas.session_prompt_dto import SessionPromptDTO
from ..schemas.session_response_model import SessionMetadataModel, SessionResponseModel
from ..services.session_service import SessionService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Red Teaming"])
logger = logging.getLogger(__name__)


@router.get("/")
@inject
async def healthcheck() -> dict[str, str]:
    """
    Check the health of the web API.

    Returns:
        Dict[str, str]: The status message indicating the API is running.
    """
    return {"status": "web api is up and running"}


@router.get("/api/v1/sessions")
@inject
async def get_all_sessions(
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> list[SessionMetadataModel]:
    """
    Fetches a list of all session metadata from the service layer.

    This endpoint does not require any parameters and will return a list of session metadata objects.
    Each object contains details about a specific session without including the session history.

    Returns:
        List[SessionMetadataModel]: A list of session metadata objects.

    Raises:
        HTTPException: 404 error if no sessions are found.
                       400 error if there is a validation issue with the request.
                       500 error for any other server-side issues.
    """
    try:
        return session_service.get_all_session()

    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.get("/api/v1/sessions/name")
@inject
async def get_all_sessions_name(
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> list[str]:
    """
    Retrieve the names of all sessions.

    Args:
        session_service (SessionService): The service responsible for session operations.

    Returns:
        List[str]: A list of session names.

    Raises:
        HTTPException: An error with status code 404 if no session names are found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        return session_service.get_all_sessions_names()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.get("/api/v1/sessions/{runner_id}")
@inject
async def get_session_by_runner_id(
    runner_id: str,
    include_history: bool = Query(
        default=False,
        description="Flag to determine if session history should be included.",
    ),
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> SessionResponseModel:
    """
    Retrieve session data for a given runner ID, optionally including chat history.

    Args:
        runner_id (str): The unique identifier for the runner.
        include_history (bool): A flag to determine if the session history should be included in the response.
        session_service (SessionService): The service responsible for session operations.

    Returns:
        SessionResponseModel: The session data, including metadata and optionally chat records.

    Raises:
        HTTPException: An error with status code 404 if no session is found for the runner ID.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_data = session_service.get_session_by_runner_id(
            runner_id, include_history
        )
        return session_data
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.post("/api/v1/sessions")
@inject
async def create_session(
    session_dto: SessionCreateDTO,
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> SessionResponseModel:
    """
    Create a new session based on the provided session data transfer object (DTO).

    Args:
        session_dto (SessionCreateDTO): The DTO containing the data needed to create a session.
        session_service (SessionService): The service responsible for session operations.

    Returns:
        SessionResponseModel: The metadata of the newly created session.

    Raises:
        HTTPException: An error with status code 404 if the session cannot be created due to a file not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        new_session = session_service.create_new_session(session_dto)
        return new_session
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.post("/api/v1/sessions/{runner_id}/prompt")
@inject
async def prompt(
    runner_id: str,
    user_prompt: SessionPromptDTO,
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> PromptResponseModel | str:
    """
    Process a user prompt for a given session and return the session's response.

    This endpoint receives a prompt from the user and sends it to the specified session.
    The session's response to the prompt is then returned to the user.

    Args:
        runner_id (str): The unique identifier for the session to which the prompt will be sent.
        user_prompt (SessionPromptDTO): The data transfer object containing the prompt information from the user.
        session_service (SessionService): The service responsible for session management and prompt handling.

    Returns:
        PromptResponseModel: A model representing the response to the user's prompt
        ,including any chat records generated.

    Raises:
        HTTPException: Raised with status code 404 if the session associated with the runner_id is not found.
                       Raised with status code 400 if there is a validation error with the provided prompt data.
                       Raised with status code 500 for any other server-side errors encountered while processing.
    """
    try:
        result = await session_service.send_prompt(runner_id, user_prompt)
        return result
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.post("/api/v1/sessions/{runner_id}/cancel")
@inject
async def cancel_auto_redteam(
    runner_id: str,
    session_service: SessionService = Depends(Provide[Container.session_service]),
):
    """
    Cancel the automated red team operation for a given session.

    This endpoint is used to stop any ongoing automated red team operations for the session
    associated with the provided runner_id.

    Args:
        runner_id (str): The unique identifier for the session whose automated red team operation is to be canceled.
        session_service (SessionService): The service responsible for managing red team sessions.

    Raises:
        HTTPException: Raised with status code 404 if the session associated with the runner_id is not found.
                       Raised with status code 400 if there is a validation error with the runner_id.
                       Raised with status code 500 for any other server-side errors encountered while processing.
    """
    try:
        await session_service.cancel_auto_redteam(runner_id)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.delete("/api/v1/sessions/{session_id}")
@inject
async def delete_session(
    session_id: str,
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Delete a session by its ID.

    Args:
        session_id (str): The unique identifier of the session to delete.
        session_service (SessionService): The service responsible for deleting sessions.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the session is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.delete_session(session_id)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.put("/api/v1/sessions/{runner_id}/prompt-template/{prompt_template_name}")
@inject
async def set_prompt_template(
    runner_id: str,
    prompt_template_name: str,
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Select a prompt template for the current session.

    Args:
        runner_id (str): The unique identifier of the session.
        prompt_template_name (str): The name of the prompt template to select.
        session_service (SessionService): The service responsible for managing session prompt templates.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the prompt template is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.select_prompt_template(runner_id, prompt_template_name)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.delete("/api/v1/sessions/{runner_id}/prompt-template/{prompt_template_name}")
@inject
async def unset_prompt_template(
    runner_id: str,
    prompt_template_name: str = "",
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Remove prompt template from the current session.

    Args:
        runner_id (str): The unique identifier of the session.
        prompt_template_name (str): The name of the prompt template to remove.
        session_service (SessionService): The service responsible for managing session prompt templates.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the prompt template is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.select_prompt_template(runner_id, "")
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.put(
    "/api/v1/sessions/{runner_id}/context-strategy/{ctx_strategy_name}/{num_of_prompt}"
)
@inject
async def set_context_strategy(
    runner_id: str,
    ctx_strategy_name: str,
    num_of_prompt: int,
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Set a context strategy for the current session.

    Args:
        runner_id (str): The unique identifier of the session.
        ctx_strategy_name (str): The name of the context strategy to set.
        num_of_prompt (int): The number of prompts to apply the context strategy to.
        session_service (SessionService): The service responsible for managing session context strategies.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the context strategy is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.select_ctx_strategy(runner_id, ctx_strategy_name, num_of_prompt)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.delete(
    "/api/v1/sessions/{runner_id}/context-strategy/{ctx_strategy_name}/{num_of_prompt}"
)
@inject
async def unset_context_strategy(
    runner_id: str,
    ctx_strategy_name: str = "",
    num_of_prompt: int = 0,
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Remove a context strategy from the current session.

    Args:
        runner_id (str): The unique identifier of the session.
        ctx_strategy_name (str): The name of the context strategy to remove.
        num_of_prompt (int): The number of prompts to apply the context strategy to, defaults to 0.
        session_service (SessionService): The service responsible for managing session context strategies.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the context strategy is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.select_ctx_strategy(runner_id, "", 0)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.put("/api/v1/sessions/{runner_id}/attack-module/{atk_module_name}")
@inject
async def set_attack_module(
    runner_id: str,
    atk_module_name: str,
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Set an attack module for the current session.

    Args:
        runner_id (str): The unique identifier of the session.
        atk_module_name (str): The name of the attack module to set.
        session_service (SessionService): The service responsible for managing session attack modules.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the attack module is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.select_attack_module(runner_id, atk_module_name)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.delete("/api/v1/sessions/{runner_id}/attack-module/{atk_module_name}")
@inject
async def unset_attack_module(
    runner_id: str,
    atk_module_name: str = "",
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Remove an attack module from the current session.

    Args:
        runner_id (str): The unique identifier of the session.
        atk_module_name (str): The name of the attack module to remove.
        session_service (SessionService): The service responsible for managing session attack modules.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the attack module is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.select_attack_module(runner_id, "")
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.put("/api/v1/sessions/{runner_id}/metric/{metric_name}")
@inject
async def set_metric(
    runner_id: str,
    metric_name: str,
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Set a metric for the current session.

    Args:
        runner_id (str): The unique identifier of the session.
        metric_name (str): The name of the metric to set.
        session_service (SessionService): The service responsible for managing session metrics.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the metric is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.select_metric(runner_id, metric_name)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.delete("/api/v1/sessions/{runner_id}/metric/{metric_name}")
@inject
async def unset_metric(
    runner_id: str,
    metric_name: str = "",
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    """
    Remove a metric from the current session.

    Args:
        runner_id (str): The unique identifier of the session.
        metric_name (str): The name of the metric to remove.
        session_service (SessionService): The service responsible for managing session metrics.

    Returns:
        Dict[str, bool]: A dictionary with a key 'success' indicating the operation result.

    Raises:
        HTTPException: An error with status code 404 if the metric is not found.
                       An error with status code 400 if there is a validation error.
                       An error with status code 500 for any other server-side error.
    """
    try:
        session_service.select_metric(runner_id, "")
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.put("/api/v1/sessions/{runner_id}/system-prompt")
@inject
async def set_system_prompts(
    runner_id: str,
    system_prompt: str = Body(..., embed=True),
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    try:
        session_service.update_system_prompt(runner_id, system_prompt)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.delete("/api/v1/sessions/{runner_id}/system-prompt")
@inject
async def unset_system_prompts(
    runner_id: str,
    system_prompt: str = "",
    session_service: SessionService = Depends(Provide[Container.session_service]),
) -> dict[str, bool]:
    try:
        session_service.update_system_prompt(runner_id, "")
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)


@router.get("/api/v1/sessions/{runner_id}/close")
@inject
async def close_session(
    runner_id: str,
    session_service: SessionService = Depends(Provide[Container.session_service]),
):
    try:
        await session_service.end_session(runner_id)
        return {"success": True}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=e.msg)
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=e.msg)
        else:
            raise HTTPException(status_code=500, detail=e.msg)
