from pydantic import BaseModel, ConfigDict


class BenchmarkRunnerDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    run_name: str
    description: str
    endpoints: list[str]
    inputs: list[str]
    num_of_prompts: int
    random_seed: int
    system_prompt: str
    runner_processing_module: str
    attack_module: str = ""
