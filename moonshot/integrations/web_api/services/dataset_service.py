from .... import api as moonshot_api
from ..schemas.dataset_create_dto import CSV_Dataset_DTO, HF_Dataset_DTO
from ..schemas.dataset_response_dto import DatasetResponseDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler
from .utils.file_manager import copy_file
import os


class DatasetService(BaseService):
    @exception_handler
    def convert_dataset(self, dataset_data: CSV_Dataset_DTO) -> str:
        """
        Convert a dataset using the provided dataset data.

        Args:
            dataset_data (CSV_Dataset_DTO): The data required to convert the dataset.

        Returns:
            str: The filename of the newly created dataset.

        Raises:
            Exception: If an error occurs during dataset conversion.
        """

        new_ds_path = moonshot_api.api_convert_dataset(
            name=dataset_data.name,
            description=dataset_data.description,
            reference=dataset_data.reference,
            license=dataset_data.license,
            file_path=dataset_data.file_path,
        )
        return os.path.splitext(os.path.basename(new_ds_path))[0]

    @exception_handler
    def download_dataset(self, dataset_data: HF_Dataset_DTO) -> str:
        """
        Download a dataset using the provided dataset data.

        Args:
            dataset_data (HF_Dataset_DTO): The data required to download the dataset.

        Returns:
            str: The path to the newly downloaded dataset.

        Raises:
            Exception: If an error occurs during dataset download.
        """

        new_ds_path = moonshot_api.api_download_dataset(
            name=dataset_data.name,
            description=dataset_data.description,
            reference=dataset_data.reference,
            license=dataset_data.license,
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
