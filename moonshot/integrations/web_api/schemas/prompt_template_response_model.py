from pydantic import BaseModel, RootModel


class PromptTemplate(BaseModel):
    name: str
    description: str
    template: str


PromptTemplatesResponseModel = RootModel[list[PromptTemplate]]
