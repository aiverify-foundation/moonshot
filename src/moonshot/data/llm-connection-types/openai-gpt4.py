import openai
from openai.openai_object import OpenAIObject


class OpenAIGpt4:
    def __init__(self, api_endpoint: str, api_token: str, api_params: dict):
        self._api_endpoint = api_endpoint
        self._api_token = api_token
        self._api_params = api_params
        self._pre_prompt = ""
        self._post_prompt = ""

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
        openai_request = [{"role": "user", "content": connector_prompt}]
        response = await openai.ChatCompletion.acreate(
            model="gpt-4", messages=openai_request, temperature=0
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
            openai.api_key = self._api_token
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {
                    "role": "assistant",
                    "content": "The Los Angeles Dodgers won the World Series in 2020.",
                },
                {"role": "user", "content": "Where was it played?"},
            ]
            await openai.ChatCompletion.acreate(
                model="gpt-4", messages=messages, temperature=0, max_tokens=256
            )
            return True
        except Exception:
            return False

    async def _process_response(self, response: OpenAIObject) -> str:
        """
        Process an HTTP response and extract relevant information as a string.

        This function takes an HTTP response object as input and processes it to extract
        relevant information as a string. The extracted information may include data
        from the response body, headers, or other attributes.

        Args:
            response (OpenAIObject): An HTTP response object containing the response data.

        Returns:
            str: A string representing the relevant information extracted from the response.
        """
        return response["choices"][0]["message"]["content"]
