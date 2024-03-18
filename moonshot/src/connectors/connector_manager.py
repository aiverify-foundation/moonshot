import time
from pathlib import Path
from typing import Callable, Union

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.benchmarking.prompt_arguments import PromptArguments
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.storage.storage_manager import StorageManager


class ConnectorManager:
    # Endpoint functions
    @staticmethod
    def create_endpoint(ep_args: ConnectorEndpointArguments) -> None:
        """
        Creates a new endpoint and stores its information in a JSON file.

        This method takes the arguments provided in the `ep_args` parameter, generates a unique endpoint ID by
        slugifying the endpoint name, and then constructs a dictionary with the endpoint's information. It then
        writes this information to a JSON file named after the endpoint ID within the directory specified by
        `EnvironmentVars.CONNECTORS_ENDPOINTS`. If the operation fails for any reason, an exception is raised
        and the error is printed.

        Args:
            ep_args (ConnectorEndpointArguments): An object containing the necessary information to create a
            new endpoint.

        Raises:
            Exception: If there is an error during file writing or any other operation within the method.
        """
        try:
            ep_id = slugify(ep_args.name, lowercase=True)
            ep_info = {
                "id": ep_id,
                "name": ep_args.name,
                "connector_type": ep_args.connector_type,
                "uri": ep_args.uri,
                "token": ep_args.token,
                "max_calls_per_second": ep_args.max_calls_per_second,
                "max_concurrency": ep_args.max_concurrency,
                "params": ep_args.params,
            }

            # Write as json output
            StorageManager.create_connector_endpoint(ep_id, ep_info)

        except Exception as e:
            print(f"Failed to create endpoint: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def read_endpoint(ep_id: str) -> ConnectorEndpointArguments:
        """
        Reads an endpoint and returns its information.

        This method takes an endpoint ID as input, reads the corresponding JSON file from the directory specified by
        `EnvironmentVars.CONNECTORS_ENDPOINTS`, and returns a ConnectorEndpointArguments object containing the
        endpoint's information. If the operation fails for any reason, an exception is raised and the error is printed.

        Args:
            ep_id (str): The ID of the endpoint to read.

        Returns:
            ConnectorEndpointArguments: An object containing the endpoint's information.

        Raises:
            Exception: If there is an error during file reading or any other operation within the method.
        """
        try:
            return ConnectorEndpointArguments(
                **StorageManager.read_connector_endpoint(ep_id)
            )

        except Exception as e:
            print(f"Failed to read endpoint: {str(e)}")
            raise e

    @staticmethod
    def update_endpoint(ep_args: ConnectorEndpointArguments) -> None:
        """
        Updates an existing endpoint with new information.

        This method takes a ConnectorEndpointArguments object as input, which contains the new information for the
        endpoint. Instead of deleting and recreating the endpoint, it directly updates the existing endpoint file
        with the new information. If the operation fails for any reason, an exception is raised and the error
        is printed.

        Args:
            ep_args (ConnectorEndpointArguments): An object containing the new information for the endpoint.

        Raises:
            Exception: If there is an error during the update operation.
        """
        try:
            # Convert the endpoint arguments to a dictionary
            ep_info = ep_args.to_dict()

            # Write the updated endpoint information to the file
            StorageManager.create_connector_endpoint(ep_args.id, ep_info)

        except Exception as e:
            print(f"Failed to update endpoint: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def delete_endpoint(ep_id: str) -> None:
        """
        Deletes an endpoint.

        This method takes an endpoint ID as input, deletes the corresponding JSON file from the directory specified by
        `EnvironmentVars.CONNECTORS_ENDPOINTS`. If the operation fails for any reason, an exception is raised and the
        error is printed.

        Args:
            ep_id (str): The ID of the endpoint to delete.

        Raises:
            Exception: If there is an error during file deletion or any other operation within the method.
        """
        try:
            StorageManager.delete_connector_endpoint(ep_id)

        except Exception as e:
            print(f"Failed to delete endpoint: {str(e)}")
            raise e

    @staticmethod
    def get_available_endpoints() -> tuple[list[str], list[ConnectorEndpointArguments]]:
        """
        Retrieves a list of available endpoints and their information.

        This method scans the designated directory for connector endpoints, reads each endpoint's information from its
        JSON file, and compiles a list of endpoint IDs and their corresponding information. It filters out any files
        that do not represent valid endpoints (e.g., system files starting with "__"). The method returns a tuple
        containing a list of endpoint IDs and a list of dictionaries, each containing the information of an endpoint.

        Returns:
            tuple[list[str], list[dict]]: A tuple containing a list of endpoint IDs and a list of dictionaries with
            endpoint information.
        """
        try:
            retn_eps = []
            retn_eps_ids = []

            eps = StorageManager.get_connector_endpoints()
            for ep in eps:
                if "__" in ep:
                    continue

                ep_info = ConnectorEndpointArguments(
                    **StorageManager.read_connector_endpoint(Path(ep).stem)
                )
                retn_eps.append(ep_info)
                retn_eps_ids.append(ep_info.id)

            return retn_eps_ids, retn_eps

        except Exception as e:
            print(f"Failed to get available endpoints: {str(e)}")
            raise e

    # Connector functions
    @staticmethod
    def create_connector(ep_args: ConnectorEndpointArguments) -> Connector:
        """
        Creates a connector object based on the provided endpoint arguments.

        This method takes a ConnectorEndpointArguments object, which contains the necessary information
        to initialize and return a Connector object. The Connector object is created by calling the
        `load_connector` method, which dynamically loads and initializes the connector based on the
        endpoint arguments provided.

        Args:
            ep_args (ConnectorEndpointArguments): The endpoint arguments required to create the connector.

        Returns:
            Connector: An initialized Connector object based on the provided endpoint arguments.
        """
        try:
            return Connector.load_connector(ep_args)

        except Exception as e:
            print(f"Failed to create connector: {str(e)}")
            raise e

    @staticmethod
    def get_available_connector_types() -> list[str]:
        """
        Retrieves a list of all available connector types.

        This method uses the `StorageManager.get_connectors` method to find all Python files in the directory
        specified by the `EnvironmentVars.CONNECTORS` environment variable. It then filters out any files that are not
        meant to be exposed as connectors (those containing "__" in their names). The method returns a list of the
        names of these connector types.

        Returns:
            list[str]: A list of strings, each representing the name of a connector type.

        Raises:
            Exception: If there is an error during the retrieval of connector types.
        """
        try:
            return [
                Path(fp).stem
                for fp in StorageManager.get_connectors()
                if "__" not in fp
            ]

        except Exception as e:
            print(f"Failed to get available connectors: {str(e)}")
            raise e

    @staticmethod
    async def get_prediction(
        generated_prompt: PromptArguments,
        connector: Connector,
        prompt_callback: Union[Callable, None] = None,
    ) -> PromptArguments:
        """
        Generates a prediction for a given prompt using a specified connector.

        This method takes a `generated_prompt` object, which contains the prompt to be predicted, and a `connector`
        object, which is used to generate the prediction. The method also optionally takes a `prompt_callback` function,
        which is called after the prediction is generated.

        The method first prints a message indicating that it is predicting the prompt. It then records the start time
        and uses the `connector` to generate a prediction for the `generated_prompt`. The duration of the prediction
        is calculated and stored in the `generated_prompt`.

        If a `prompt_callback` function is provided, it is called with the `generated_prompt` and `connector.id` as
        arguments.

        The method then returns the `generated_prompt` with the generated prediction and duration.

        Args:
            generated_prompt (PromptArguments): The prompt to be predicted.
            connector (Connector): The connector to be used for prediction.
            prompt_callback (Union[Callable, None]): An optional callback function to be called after prediction.

        Returns:
            PromptArguments: The `generated_prompt` with the generated prediction and duration.

        Raises:
            Exception: If there is an error during prediction.
        """
        try:
            print(f"Predicting prompt {generated_prompt.prompt_index} [{connector.id}]")

            start_time = time.perf_counter()
            generated_prompt.predicted_results = await connector.get_response(
                generated_prompt.prompt
            )
            generated_prompt.duration = time.perf_counter() - start_time
            print(
                f"[Prompt {generated_prompt.prompt_index}] took {generated_prompt.duration:.4f}s"
            )

            # Call prompt callback
            if prompt_callback:
                prompt_callback(generated_prompt, connector.id)

            # Return the updated prompt
            return generated_prompt

        except Exception as e:
            print(f"Failed to get prediction: {str(e)}")
            raise e
