from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..types.types import BenchmarkResult
from ..services.utils.results_formatter import transform_web_format
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler

class BenchmarkResultService(BaseService):
    @exception_handler
    def get_all_results(self, executor_id: str | None = None) -> list[BenchmarkResult] | BenchmarkResult | None:
        results: list[BenchmarkResult] = moonshot_api.api_get_all_result()
        if not executor_id:
            # returning in raw format because tranforming a big list is probably expensive
            return results
        
        for result in results:
            if result["metadata"]["id"] == executor_id:
                return transform_web_format(result)
        return None