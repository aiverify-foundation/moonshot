from .... import api as moonshot_api
from ..schemas.dataset_create_dto import DatasetCreateDTO
from ..schemas.dataset_response_dto import DatasetResponseDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from .utils.file_manager import copy_file


class DatasetService(BaseService):
    @exception_handler
    def create_dataset(self, dataset_data: DatasetCreateDTO, method: str) -> str:
        """
        Create a dataset using the specified method.

        Args:
            dataset_data (DatasetCreateDTO): The data required to create the dataset.
            method (str): The method to use for creating the dataset.
                          Supported methods are "hf" and "csv".

        Raises:
            Exception: If an error occurs during dataset creation.
        """
        new_ds_path = moonshot_api.api_create_datasets(
            name=dataset_data.name,
            description=dataset_data.description,
            reference=dataset_data.reference,
            license=dataset_data.license,
            method=method,
            **dataset_data.params,
        )
        return copy_file(new_ds_path)

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
