from dependency_injector.wiring import inject
from .... import api as moonshot_api
from ..schemas.report_analysis_create_dto import ReportAnalysisCreateDTO
from ..services.base_service import BaseService
from ..services.utils.exceptions_handler import exception_handler


class ReportAnalysisService(BaseService):

    @exception_handler
    def create_report_analysis(self, report_analysis_data: ReportAnalysisCreateDTO) -> dict:
        result = moonshot_api.api_create_report_analysis(
            ra_id= report_analysis_data.ra_id,
            ra_args= report_analysis_data.ra_args
        )
        return result
    

    @exception_handler
    def get_all_report_analysis(self) -> list[str]:
        results = moonshot_api.api_get_all_report_analysis()
        return results
    

    @exception_handler
    def read_report_analysis(self,report_id: str) -> dict:
        result = moonshot_api.api_read_report_analysis(report_id)
        return result
    
    
    @exception_handler
    def delete_report_analysis(self, report_id: str) -> None:
        moonshot_api.api_delete_report_analysis(report_id)
