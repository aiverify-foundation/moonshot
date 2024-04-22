from pydantic import BaseModel, ConfigDict

class ReportAnalysisCreateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ra_id: str
    ra_args: dict
