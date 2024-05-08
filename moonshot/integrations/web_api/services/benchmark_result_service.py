from .... import api as moonshot_api
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from ..types.types import BenchmarkResult


class BenchmarkResultService(BaseService):
    @exception_handler
    def get_all_results(self) -> list[BenchmarkResult] | BenchmarkResult | None:
        results: list[BenchmarkResult] = moonshot_api.api_get_all_result()
        return results

    @exception_handler
    def get_all_result_name(self) -> list[str] | None:
        results = moonshot_api.api_get_all_result_name()
        return results

    @exception_handler
    def get_result_by_id(self, result_id: str) -> BenchmarkResult | None:
        result = moonshot_api.api_read_result(result_id)
        return result

    @exception_handler
    def delete_result(self, result_id: str) -> None:
        moonshot_api.api_delete_result(result_id)
