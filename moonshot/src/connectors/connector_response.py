class ConnectorResponse:
    def __init__(self, response: str, context: list = []):
        """
        Initializes a ConnectorResponse instance.

        Args:
            response (str): The response text from the connector.
            context (list, optional): Additional context or metadata related to the response. Defaults to an empty list.
        """
        self.response = response
        self.context = context

    def to_dict(self) -> dict:
        """
        Converts the ConnectorResponse instance to a dictionary.

        Returns:
            dict: A dictionary representation of the ConnectorResponse instance.
        """
        return {"response": self.response, "context": self.context}
