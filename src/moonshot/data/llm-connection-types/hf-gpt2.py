import aiohttp
from aiohttp import ClientResponse


class HFGpt2:
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
        payload = {
            "inputs": connector_prompt,
            "parameters": {
                "max_length": 512,
                "min_length": 100,
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._api_endpoint,
                headers=self._prepare_headers(),
                json=payload,
            ) as response:
                return await self._process_response(response)

    async def _check_connection(self) -> bool:
        """
        Check the connection status of a model connector.

        Returns:
            bool: True if the connection to the external service is successfully established; otherwise, False
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self._api_endpoint,
                    headers=self._prepare_headers(),
                    json={"inputs": "test"},
                ):
                    pass
            return True
        except Exception:
            return False

    def _prepare_headers(self) -> dict:
        """
        Prepare HTTP headers for authentication using a bearer token.

        This function takes a bearer token as input and prepares a dictionary of HTTP headers
        commonly used for authentication in API requests.

        Returns:
            dict: A dictionary containing HTTP headers with the 'Authorization' header set to
            'Bearer <bearer_token>'. This dictionary can be used in API requests for authentication
            purposes.
        """
        return {
            "Authorization": f"Bearer {self._api_token}",
            "Content-Type": "application/json",
        }

    async def _process_response(self, response: ClientResponse) -> str:
        """
        Process an HTTP response and extract relevant information as a string.

        This function takes an HTTP response object as input and processes it to extract relevant information
        as a string. The extracted information may include data from the response body, headers, or other attributes.

        Args:
            response (ClientResponse): An HTTP response object containing the response data.

        Returns:
            str: A string representing the relevant information extracted from the response.
        """
        try:
            json_response = await response.json()
            return json_response[0]["generated_text"]
        except Exception as exception:
            print(
                f"An exception has occurred: {str(exception)}, {await response.json()}"
            )
            raise exception
