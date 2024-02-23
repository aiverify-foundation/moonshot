import logging

import anthropic
from anthropic import AI_PROMPT, HUMAN_PROMPT
from anthropic.types import Completion

from moonshot.src.connectors.connector import Connector, perform_retry
from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Claude2(Connector):
    def __init__(self, ep_arguments: ConnectorEndpointArguments):
        # Initialize super class
        super().__init__(ep_arguments)

        # Create anthropic client
        self.client = anthropic.AsyncAnthropic(api_key=self.token)

    @Connector.rate_limited
    @perform_retry
    async def get_response(self, prompt: str) -> str:
        """
        Retrieve and return a response.
        This method is used to retrieve a response, typically from an object or service represented by
        the current instance.
        """
        connector_prompt = f"{self.pre_prompt}{prompt}{self.post_prompt}"
        response = await self.client.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=f"{HUMAN_PROMPT}{connector_prompt}{AI_PROMPT}",
        )
        return await self._process_response(response)

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
        return response.completion[1:]
