from .... import api as moonshot_api
from ..schemas.dataset_response_dto import DatasetResponseDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class DatasetService(BaseService):
    @exception_handler
    def get_all_datasets(self) -> list[DatasetResponseDTO]:
        datasets = moonshot_api.api_get_all_datasets()
        return [DatasetResponseDTO.model_validate(dataset) for dataset in datasets]

    @exception_handler
    def get_all_datasets_name(self) -> list[str] | None:
        datasets = moonshot_api.api_get_all_datasets_name()
        return datasets

    @exception_handler
    def delete_dataset(self, dataset_id: str) -> None:
        moonshot_api.api_delete_dataset(dataset_id)
