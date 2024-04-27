from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from ..container import Container
from ..schemas.report_analysis_create_dto import ReportAnalysisCreateDTO

from ..services.report_analysis_service import ReportAnalysisService
from ..services.utils.exceptions_handler import ServiceException
from typing import Optional


router = APIRouter()

@router.post("/api/v1/report-analysis")
@inject
def create_report_analysis(
    report_analysis_data: ReportAnalysisCreateDTO,
    report_service: ReportAnalysisService = Depends(Provide[Container.report_analysis_service])
    ):
    """
    Create the dictionary for report analysis
    """
    try:
        result = report_service.create_report_analysis(report_analysis_data)
        return result
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to create report analysis: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to create report analysis: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to create report analysis: {e.msg}")    


@router.get("/api/v1/report-analysis")
@inject
def get_all_report_analysis(report_service: ReportAnalysisService = Depends(Provide[Container.report_analysis_service])
    ):
    """
    Get all the report analysis from the database
    """
    try:
        return report_service.get_all_report_analysis()
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve report analysis: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve report analysis: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve report analysis: {e.msg}")   
            

@router.get("/api/v1/report-analysis/{ra_id}")
@inject 
def read_report_analysis(
    ra_id: str,
    report_service: ReportAnalysisService = Depends(Provide[Container.report_analysis_service])
    ) -> dict:
    """
    Get a report analysis from the database
    """
    try:
        result = report_service.read_report_analysis(ra_id)
        return result
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to retrieve report analysis: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to retrieve report analysis: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve report analysis: {e.msg}")


@router.delete("/api/v1/report-analysis/{ra_id}")
@inject
def delete_report_analysis(
    ra_id: str,
    report_service: ReportAnalysisService = Depends(Provide[Container.report_analysis_service])
    ) -> dict[str, str] | tuple[dict[str, str], int]:

    try:
        report_service.delete_report_analysis(ra_id)
        return {"message": "Report Analysis deleted successfully"}
    except ServiceException as e:
        if e.error_code == "FileNotFound":
            raise HTTPException(status_code=404, detail=f"Failed to delete report analysis: {e.msg}")
        elif e.error_code == "ValidationError":
            raise HTTPException(status_code=400, detail=f"Failed to delete report analysis: {e.msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete report analysis: {e.msg}")    
    
