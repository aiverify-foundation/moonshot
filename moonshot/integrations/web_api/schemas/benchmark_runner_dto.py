from pydantic import BaseModel, ConfigDict, Field


class BenchmarkRunnerDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    run_name: str
    description: str
    endpoints: list[str]
    inputs: list[str]
    prompt_selection_percentage: int = Field(..., ge=1, le=100)
    random_seed: int
    system_prompt: str
    runner_processing_module: str
