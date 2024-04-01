from dependency_injector.wiring import inject
from ..services.benchmark_test_manager import BenchmarkTestManager
from ..schemas.cookbook_executor_create_dto import CookbookExecutorCreateDTO
from ..schemas.recipe_executor_create_dto import RecipeExecutorCreateDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler

class BenchmarkingService(BaseService):
    @inject
    def __init__(self, benchmark_test_manager: BenchmarkTestManager) -> None:
        self.benchmark_test_manager = benchmark_test_manager

    
    @exception_handler
    async def execute_cookbook(self, cookbook_executor_data: CookbookExecutorCreateDTO) -> str:
        id = self.benchmark_test_manager.schedule_test_task(cookbook_executor_data);
        return id

    @exception_handler
    async def execute_recipe(self, recipe_executor_data: RecipeExecutorCreateDTO):
        async_task = self.benchmark_test_manager.schedule_test_task(recipe_executor_data);
        return async_task.get_name()

    @exception_handler
    async def cancel_executor(self, executor_id: str) -> None:
        self.benchmark_test_manager.cancel_task(executor_id);
