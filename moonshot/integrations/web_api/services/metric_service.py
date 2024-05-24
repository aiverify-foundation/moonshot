from .... import api as moonshot_api
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class MetricService(BaseService):
    @exception_handler
    def get_all_metric(self) -> list[dict]:
        metrics = moonshot_api.api_get_all_metric()
        return metrics

    @exception_handler
    def delete_metric(self, metric_id: str) -> None:
        moonshot_api.api_delete_metric(metric_id)
