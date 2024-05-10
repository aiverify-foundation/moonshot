import logging

import aiohttp
from aiohttp import ClientResponse
import json
from ibmcloud_iam.token import TokenManager

from moonshot.src.connectors.connector import Connector, perform_retry
from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class IBMwatsonx(Connector):
    def __init__(self, ep_arguments: ConnectorEndpointArguments):
        # Initialize super class
        super().__init__(ep_arguments)

        if (self.endpoint[len(self.endpoint)-1] != '/') : self.endpoint = self.endpoint + '/' 

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
        payload = {
            "model_id": "ibm/granite-13b-instruct-v2",
            "input": connector_prompt,
            "parameters": {
                "max_new_tokens": 300,
            },
            "project_id": self.project_id
        }

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(
                self.endpoint+'ml/v1/text/generation?version=2023-05-02',
                headers=self._prepare_headers(),
                data=json.dumps(payload),
            ) as response:
                #result = await response.json()
                #generated_text =  result['results'][0]['generated_text']
                #print(f'Generated Text = {generated_text}')
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
        tm = TokenManager(api_key="NGN72lQfgU74pxUQ_-18DKuOaEHapIuCg2HVFlaVPUci")
        token = tm.get_token()
        print(token)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
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
            return str(json_response["results"][0]["generated_text"])
        except Exception as exception:
            print(
                f"An exception has occurred: {str(exception)}"
            )
            raise exception
