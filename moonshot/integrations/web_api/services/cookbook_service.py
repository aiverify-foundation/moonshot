from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..schemas.cookbook_create_dto import CookbookCreateDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler

class CookbookService(BaseService):
    @exception_handler
    def create_cookbook(self, cookbook_data: CookbookCreateDTO) -> None:
        moonshot_api.api_create_cookbook(
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes
        )
    
    @exception_handler
    def update_cookbook(self, cookbook_data: CookbookCreateDTO, cookbook_id: str) -> None:
        moonshot_api.api_update_cookbook(
            id=cookbook_id,
            name=cookbook_data.name,
            description=cookbook_data.description,
            recipes=cookbook_data.recipes
        )

    @exception_handler
    def get_all_cookbooks(self) -> dict:
        cookbooks = moonshot_api.api_get_all_cookbook()
        return cookbooks

    @exception_handler
    def get_cookbook_by_id(self, cookbook_id: str) -> dict: 
        cookbook = moonshot_api.api_read_cookbook(cookbook_id)
        return cookbook
    
    @exception_handler
    def get_cookbooks_by_ids(self, cookbook_ids: list[str]) -> list[dict]: 
        cookbooks = moonshot_api.api_read_cookbooks(cookbook_ids)
        return cookbooks