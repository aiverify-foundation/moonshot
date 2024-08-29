from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..container import Container
from ..services.augmentor_service import AugmentorService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Augmentor"])

class AugmentRecipeRequest(BaseModel):
    recipe_id: str
    attack_module_id: str

class AugmentDatasetRequest(BaseModel):
    dataset_id: str
    attack_module_id: str

@router.post("/api/v1/augment/recipe", response_description="Augment a Recipe")
@inject
def augment_recipe(
    request: AugmentRecipeRequest,
    augment_service: AugmentorService = Depends(Provide[Container.augmentor_service]),
) -> str:
    """
    Augments a recipe using the specified attack module.

    Args:
        request (AugmentRecipeRequest): The request containing the recipe ID and attack module ID.
        augment_service (AugmentorService): The service for augmenting recipes and datasets.

    Returns:
        str: The ID of the newly created augmented recipe.

    Raises:
        HTTPException: If the augmentation fails due to file not found, validation error, or any other error.
    """
    try:
        return augment_service.augment_recipe(request.recipe_id, request.attack_module_id)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to augment recipe: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to augment recipe: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to augment recipe: {e.msg}"
            )

@router.post("/api/v1/augment/dataset", response_description="Augment a Dataset")
@inject
def augment_dataset(
    request: AugmentDatasetRequest,
    augment_service: AugmentorService = Depends(Provide[Container.augmentor_service]),
) -> str:
    """
    Augments a dataset using the specified attack module.

    Args:
        request (AugmentDatasetRequest): The request containing the dataset ID and attack module ID.
        augment_service (AugmentorService): The service for augmenting recipes and datasets.

    Returns:
        str: The ID of the newly created augmented dataset.

    Raises:
        HTTPException: If the augmentation fails due to file not found, validation error, or any other error.
    """
    try:
        return augment_service.augment_dataset(request.dataset_id, request.attack_module_id)
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to augment dataset: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to augment dataset: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to augment dataset: {e.msg}"
            )