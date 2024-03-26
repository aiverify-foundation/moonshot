from pathlib import Path

from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.storage.storage_manager import StorageManager


class ConnectorEndpoint:
    @staticmethod
    def create(ep_args: ConnectorEndpointArguments) -> None:
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
    def read(ep_id: str) -> ConnectorEndpointArguments:
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
    def update(ep_args: ConnectorEndpointArguments) -> None:
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
    def delete(ep_id: str) -> None:
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
    def get_available_items() -> tuple[list[str], list[ConnectorEndpointArguments]]:
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
