from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from ..container import Container
from ..services.augmentor_service import AugmentorService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Augmentor"])


@router.post("/api/v1/augment/recipe", response_description="Augment a Recipe")
@inject
def augment_recipe(
    recipe_id: str,
    attack_module_id: str,
    augment_service: AugmentorService = Depends(Provide[Container.augmentor_service]),
) -> str:
    """
    Augments a recipe using the specified attack module.

    Args:
        recipe_id (str): The ID of the recipe to be augmented.
        attack_module_id (str): The ID of the attack module to use for augmentation.
        augment_service (AugmentorService): The service for augmenting recipes and datasets.

    Returns:
        str: The ID of the newly created augmented recipe.

    Raises:
        HTTPException: If the augmentation fails due to file not found, validation error, or any other error.
    """
    try:
        return augment_service.augment_recipe(recipe_id, attack_module_id)
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
    dataset_id: str,
    attack_module_id: str,
    augment_service: AugmentorService = Depends(Provide[Container.augmentor_service]),
) -> str:
    """
    Augments a dataset using the specified attack module.

    Args:
        dataset_id (str): The ID of the dataset to be augmented.
        attack_module_id (str): The ID of the attack module to use for augmentation.
        augment_service (AugmentorService): The service for augmenting recipes and datasets.

    Returns:
        str: The ID of the newly created augmented dataset.

    Raises:
        HTTPException: If the augmentation fails due to file not found, validation error, or any other error.
    """
    try:
        return augment_service.augment_dataset(dataset_id, attack_module_id)
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
