from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..schemas.recipe_create_dto import RecipeCreateDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class RunnerService(BaseService):

    
    @exception_handler
    def get_all_runner(self) -> list[dict]:
        runners = moonshot_api.api_get_all_runner()
        return runners
    

    @exception_handler
    def get_all_runner_name(self) -> list[str]:
        runners = moonshot_api.api_get_all_runner_name()
        return runners


    @exception_handler
    def get_runner_by_id(self, runner_id: str) -> dict | None: 
        runner = moonshot_api.api_read_runner(runner_id)
        return runner
    

    @exception_handler
    def delete_run(self, runner_id: str) -> None:
        moonshot_api.api_delete_runner(runner_id)