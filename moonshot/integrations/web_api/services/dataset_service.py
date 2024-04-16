from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..schemas.dataset_response_dto import DatasetResponseDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class DatasetService(BaseService):

    @exception_handler
    def get_all_datasets(self) -> list[DatasetResponseDTO | None]:
        # datasets = moonshot_api.api_get_all_dataset()
        datasets = [{
            "id": "dummy_dataset",
            "name": "dummy_dataset",
            "description": "dummy_dataset",
            "keywords": ["dummy_dataset"],
            "examples": ["dummy_dataset"]
        }]
        return [DatasetResponseDTO.model_validate(dataset) for dataset in datasets]    


    @exception_handler
    def get_dataset_by_id(self, dataset_id: str) -> DatasetResponseDTO | None: 
        # dataset = moonshot_api.api_read_dataset(dataset_id)
        # return DatasetResponseDTO.model_validate(dataset)
        dummmy_value = {
            "id": "dummy_dataset",
            "name": "dummy_dataset",
            "description": "dummy_dataset",
            "keywords": ["dummy_dataset"],
            "examples": ["dummy_dataset"]
        }
        return DatasetResponseDTO.model_validate(dummmy_value)

