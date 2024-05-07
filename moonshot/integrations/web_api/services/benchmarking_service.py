from dependency_injector.wiring import inject
from ..services.benchmark_test_manager import BenchmarkTestManager
from ..schemas.benchmark_runner_dto import BenchmarkRunnerDTO
from ..types.types import BenchmarkCollectionType
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler

class BenchmarkingService(BaseService):
    @inject
    def __init__(self, benchmark_test_manager: BenchmarkTestManager) -> None:
        self.benchmark_test_manager = benchmark_test_manager

    
    @exception_handler
    async def execute_cookbook(self, cookbook_executor_data: BenchmarkRunnerDTO) -> str:
        id = self.benchmark_test_manager.schedule_test_task(cookbook_executor_data,BenchmarkCollectionType.COOKBOOK);
        return id

    @exception_handler
    async def execute_recipe(self, recipe_executor_data: BenchmarkRunnerDTO):
        id = self.benchmark_test_manager.schedule_test_task(recipe_executor_data,BenchmarkCollectionType.RECIPE);
        return id

    @exception_handler
    async def cancel_executor(self, executor_id: str) -> None:
        await self.benchmark_test_manager.cancel_task(executor_id);
