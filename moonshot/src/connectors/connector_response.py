from pydantic import BaseModel


class ConnectorResponse(BaseModel):
    response: str = ""
    context: list = []

    def to_dict(self) -> dict:
        """
        Converts the ConnectorResponse instance to a dictionary.

        Returns:
            dict: A dictionary representation of the ConnectorResponse instance.
        """
        return {"response": self.response, "context": self.context}
