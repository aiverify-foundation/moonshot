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

    @exception_handler
    def update_metric_config(self, metric_id: str, update_args: dict) -> bool:
        """
        Updates the configuration of a specific metric.

        Args:
            metric_id (str): The ID of the metric to be updated.
            update_args (dict): The updated configuration parameters.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        bool_updated = moonshot_api.api_update_metric_config(metric_id, **update_args)
        return bool_updated

    @exception_handler
    def delete_metric_config(self, metric_id: str) -> bool:
        """
        Deletes the configuration of a specific metric.

        Args:
            metric_id (str): The ID of the metric to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        bool_deleted = moonshot_api.api_delete_metric_config(metric_id)
        return bool_deleted
