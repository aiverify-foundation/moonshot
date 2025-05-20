from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse

from ..container import Container
from ..schemas.bookmark_create_dto import BookmarkCreateDTO, BookmarkPydanticModel
from ..services.bookmark_service import BookmarkService
from ..services.utils.exceptions_handler import ServiceException

router = APIRouter(tags=["Bookmark"])


@router.post(
    "/api/v1/bookmarks", response_description="Bookmark data added to the database"
)
@inject
def insert_bookmark(
    bookmark_data: BookmarkCreateDTO,
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
) -> dict:
    """
    Insert a new bookmark into the database.

    Args:
        bookmark_data: The data of the bookmark to be added.
        bookmark_service: The service responsible for bookmark operations.

    Returns:
        A dictionary with a message indicating successful insertion.

    Raises:
        HTTPException: An error occurred while inserting the bookmark.
    """
    try:
        result = bookmark_service.insert_bookmark(bookmark_data)
        return result
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to insert bookmark: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to insert bookmark: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to insert bookmark: {e.msg}"
            )


@router.get(
    "/api/v1/bookmarks",
    response_description="List of all bookmarks or a specific bookmark by name",
)
@inject
def get_all_bookmarks(
    name: Optional[str] = Query(None, description="Name of the bookmark to query"),
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
) -> list[BookmarkPydanticModel]:
    """
    Retrieve all bookmarks or a specific bookmark by name from the database.

    Args:
        name: The name of the bookmark to retrieve. If None, all bookmarks are retrieved.
        bookmark_service: The service responsible for bookmark operations.

    Returns:
        A list of bookmarks or a single bookmark if a name is provided.

    Raises:
        HTTPException: An error occurred while retrieving bookmarks.
    """
    try:
        return bookmark_service.get_all_bookmarks(
            name=name,
        )
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to retrieve bookmarks: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to retrieve bookmarks: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve bookmarks: {e.msg}"
            )


@router.delete(
    "/api/v1/bookmarks", response_description="Bookmark data deleted from the database"
)
@inject
def delete_bookmark(
    all: bool = Query(False, description="Flag to delete all bookmarks"),
    name: Optional[str] = Query(None, description="Name of the bookmark to delete"),
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
) -> dict:
    """
    Delete a specific bookmark by name or all bookmarks from the database.

    Args:
        all: A flag indicating whether to delete all bookmarks.
        name: The name of the bookmark to delete. If 'all' is False and 'name' is None, no bookmark will be deleted.
        bookmark_service: The service responsible for bookmark operations.

    Returns:
        A dictionary with a message indicating successful deletion or an error message.

    Raises:
        HTTPException: An error occurred while deleting the bookmark(s).
    """
    try:
        if all:
            return bookmark_service.delete_bookmarks(all=True)
        elif name is not None:
            return bookmark_service.delete_bookmarks(all=False, name=name)
        else:
            raise HTTPException(
                status_code=400, detail="Must specify 'all' or 'name' parameter"
            )
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to delete bookmark: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to delete bookmark: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete bookmark: {e.msg}"
            )


@router.get(
    "/api/v1/bookmarks/export", response_description="Exporting Bookmark to JSON file"
)
@inject
def export_bookbookmarks(
    export_file_name: Optional[str] = Query(
        "bookmarks", description="Name of the exported file"
    ),
    bookmark_service: BookmarkService = Depends(Provide[Container.bookmark_service]),
) -> FileResponse:
    """
    Export bookmarks to a JSON file with a given file name.

    Args:
        export_file_name: The name of the file to export the bookmarks to.z
        bookmark_service: The service responsible for bookmark operations.

    Returns:
        A FileResponse with the path to the exported file or an error message.
    """
    try:
        file_path = bookmark_service.export_bookmarks(export_file_name)
        return FileResponse(
            file_path, media_type="application/json", filename=export_file_name
        )
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(
                status_code=404, detail=f"Failed to export bookmark: {e.msg}"
            )
        elif e.error_code == "ValidationError":
            raise HTTPException(
                status_code=400, detail=f"Failed to export bookmark: {e.msg}"
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to export bookmark: {e.msg}"
            )
