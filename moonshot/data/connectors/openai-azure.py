import logging
from typing import Any

import openai
import os

from moonshot.src.connectors.connector import Connector, perform_retry
from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class OpenAIAzure(Connector):
    def __init__(self, ep_arguments: ConnectorEndpointArguments):
        # Initialize super class
        super().__init__(ep_arguments)

        # Look at the parameters and set sensible defaults
        params = self.params
        if 'temperature' in params:
            try:
                self.temperature = float(params['temperature'])
            except ValueError:
                logger.warn("Invalid temperature value. Using default value of 0.0")
                self.temperature = 0.0
        else:
            self.temperature = 0.0

        # Azure OpenAI model to use
        if 'model' in params and len(params['model']) > 0:
            self.model = params['model']
        else:
            self.model = None

        # Azure OpenAI deployment_id to use
        if 'deployment_id' in params and len(params['deployment_id']) > 0:
            self.deployment_id = params['deployment_id']
        else:
            self.deployment_id = None

        # 
        # Environment variables override the connector endpoint configuration
        #

        if 'OPENAI_API_KEY' in os.environ and len(os.environ['OPENAI_API_KEY']) > 0:
            self.token = os.environ['OPENAI_API_KEY']

        if 'OPENAI_API_MODEL' in os.environ and len(os.environ['OPENAI_API_MODEL']) > 0:
            self.model = os.environ['OPENAI_API_MODEL']
            self.deployment_id = os.environ['OPENAI_API_MODEL']

        if 'OPENAI_API_VERSION' in os.environ and len(os.environ['OPENAI_API_VERSION']) > 0:
            self.api_version = os.environ['OPENAI_API_VERSION']
        else:
            self.api_version = "2024-03-01-preview" # Sensible default

        # If 'OPENAI_API_BASE' is set, use it.
        # Expected formats:
        # https://aoa-sea-poc-eastus2.openai.azure.com
        # https://aoa-sea-poc-eastus2.openai.azure.com/openai/deployments/gpt-4-1106-preview
        if 'OPENAI_API_BASE' in os.environ and len(os.environ['OPENAI_API_BASE']) > 0:
            self.endpoint = os.environ['OPENAI_API_BASE']

        # Special case, check if self.endpoint contains "/openai/deployments/" and then extract the deployment_id
        if "/openai/deployments/" in self.endpoint:
            # Split the endpoint to extract the deployment_id
            parts = self.endpoint.split("/openai/deployments/")
            self.endpoint = parts[0]  # Update self.endpoint to the base URL
            self.deployment_id = parts[1]  # Extract the deployment_id

        # Sanity check
        if self.deployment_id is None:
            logger.error("Missing deployment_id parameter, or OPENAI_API_MODEL environment variable.")
            raise ValueError("Missing deployment_id parameter, or OPENAI_API_MODEL environment variable.")
        if self.model is None:
            logger.error("Missing model parameter, or OPENAI_API_MODEL environment variable.")
            raise ValueError("Missing model parameter, or OPENAI_API_MODEL environment variable.")

        # This is how to initialise the openai library (v0.28.1) for Microsoft Azure Endpoints
        # @see https://github.com/openai/openai-python/tree/v0.28.1
        openai.api_type = "azure"
        openai.api_key = self.token
        openai.api_base = self.endpoint
        openai.api_version = self.api_version


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
        openai_request = [{"role": "user", "content": connector_prompt}]
        response = await openai.ChatCompletion.acreate(
            deployment_id=self.deployment_id,
            model=self.model,
            messages=openai_request,
            temperature=self.temperature,
            timeout=self.timeout,
        )
        return await self._process_response(response)

    async def _process_response(self, response: Any) -> str:
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
