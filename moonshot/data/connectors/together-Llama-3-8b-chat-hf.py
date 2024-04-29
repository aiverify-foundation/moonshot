import logging
from typing import Any

from together import AsyncTogether

from moonshot.src.connectors.connector import Connector, perform_retry
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Together_Llama3_8b_Chat_HF(Connector):
    def __init__(self, ep_arguments: ConnectorEndpointArguments):
        # Initialize super class
        super().__init__(ep_arguments)

        # Set Together Key
        self._client = AsyncTogether(api_key=self.token)

    @Connector.rate_limited
    @perform_retry
    async def get_response(self, prompt: str) -> str:
        """
        Retrieve and return a response.
        This method is used to retrieve a response, typically from an object or service represented by
        the current instance.

        Returns:
            str: retrieved response data
        """
        connector_prompt = f"{self.pre_prompt}{prompt}{self.post_prompt}"
        if self.system_prompt:
            together_request = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": connector_prompt},
            ]
        else:
            together_request = [{"role": "user", "content": connector_prompt}]

        # Merge self.optional_params with additional parameters
        new_params = {
            **self.optional_params,
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": together_request,
        }
        response = await self._client.chat.completions.create(**new_params)
        return await self._process_response(response)

    def _prepare_headers(self) -> dict:
        """
        Prepare HTTP headers for authentication using a bearer token.

        This function takes a bearer token as input and prepares a dictionary of HTTP headers
        commonly used for authentication in API requests.

        Returns:
            dict: A dictionary containing HTTP headers with the 'Authorization' header set
            to 'Bearer <bearer_token>'. This dictionary can be used in API requests for
            authentication purposes.
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def _process_response(self, response: Any) -> str:
        """
        Process the response from the Together API and return the message content.

        This method processes the response received from the Together API call, specifically targeting
        the chat completion response structure. It extracts the message content from the first choice
        provided in the response, which is expected to contain the relevant information or answer.

        Args:
            response (Any): The response object received from a Together API call. It is expected to
            follow the structure of Together's chat completion response.

        Returns:
            str: A string containing the message content from the first choice in the response. This
            content represents the AI-generated text based on the input prompt.
        """
        return response.choices[0].message.content
