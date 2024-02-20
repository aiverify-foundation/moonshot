from pydantic import BaseModel, Field

class SessionCreateDTO(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=1000)
    endpoints: list[str] = Field(min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "My Session",
                "description": "This is a session",
                "endpoints": ["http://localhost:8080", "http://localhost:8081"]
            }
        }
