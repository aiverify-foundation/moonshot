import anthropic
from anthropic import AI_PROMPT, HUMAN_PROMPT
from anthropic.types import Completion


class Claude2:
    def __init__(self, api_endpoint: str, api_token: str, api_params: dict):
        self._api_endpoint = api_endpoint
        self._api_token = api_token
        self._api_params = api_params
        self._pre_prompt = ""
        self._post_prompt = ""

        self.client = anthropic.AsyncAnthropic(api_key=self._api_token)

    async def get_response(self, prompt: str) -> str:
        """
        Retrieve and return a response.
        This method is used to retrieve a response, typically from an object or service represented by
        the current instance.

        Returns:
            str: retrieved response data
        """
        if not await self._check_connection():
            raise RuntimeError("Server Not Found or Incorrect connection info!")

        connector_prompt = f"{self._pre_prompt}{prompt}{self._post_prompt}"

        response = await self.client.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=f"{HUMAN_PROMPT}{connector_prompt}{AI_PROMPT}",
        )
        return await self._process_response(response)

    async def _check_connection(self) -> bool:
        """
        Check the connection status of a model connector.
        This hook allows plugins to implement the logic necessary to verify the connection
        status to an external service, typically requiring a name, API endpoint, and API token.

        Returns:
            bool: True if the connection to the external service is successfully established;
            otherwise, False.
        """
        try:
            await self.client.completions.create(
                model="claude-2",
                max_tokens_to_sample=300,
                prompt=f"{HUMAN_PROMPT}Hello World.{AI_PROMPT}",
            )
            return True
        except Exception:
            return False

    async def _process_response(self, response: Completion) -> str:
        """
        Process an HTTP response and extract relevant information as a string.

        This function takes an HTTP response object as input and processes it to extract
        relevant information as a string. The extracted information may include data
        from the response body, headers, or other attributes.

        Args:
            response (Completion): An HTTP response object containing the response data.

        Returns:
            str: A string representing the relevant information extracted from the response.
        """
        return response.completion[1:]  # not sure why got a space infront
