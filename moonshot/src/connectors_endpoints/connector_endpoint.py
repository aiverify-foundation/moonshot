from pathlib import Path

from pydantic import validate_call
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.storage.storage import Storage


class ConnectorEndpoint:
    @staticmethod
    def create(ep_args: ConnectorEndpointArguments) -> str:
        """
        Creates a new connector endpoint.

        This method takes a ConnectorEndpointArguments object as input, generates a unique slugified ID based on the
        endpoint's name, and then creates a new endpoint with the provided details. The endpoint information is stored
        as a JSON object in the directory specified by `EnvVariables.CONNECTORS_ENDPOINTS`. If the operation is
        successful, the unique ID of the new endpoint is returned. If any error arises during the process, an exception
        is raised and the error message is logged.

        Args:
            ep_args (ConnectorEndpointArguments): An object containing the details of the endpoint to be created.

        Returns:
            str: The unique ID of the newly created endpoint.

        Raises:
            Exception: If there's an error during the endpoint creation process.
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
            Storage.create_object(
                EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, ep_info, "json"
            )
            return ep_id

        except Exception as e:
            print(f"Failed to create endpoint: {str(e)}")
            raise e

    @staticmethod
    @validate_call
    def read(ep_id: str) -> ConnectorEndpointArguments:
        """
        Fetches the details of a given endpoint.

        This method takes an endpoint ID as input, finds the corresponding JSON file in the directory
        specified by `EnvironmentVars.CONNECTORS_ENDPOINTS`, and returns a ConnectorEndpointArguments object
        that contains the endpoint's details. If any error arises during the process, an exception is raised and the
        error message is logged.

        Args:
            ep_id (str): The unique ID of the endpoint to be fetched.

        Returns:
            ConnectorEndpointArguments: An object encapsulating the details of the fetched endpoint.

        Raises:
            Exception: If there's an error during the file reading process or any other operation within the method.
        """
        try:
            if ep_id:
                return ConnectorEndpointArguments(
                    **ConnectorEndpoint._read_endpoint(ep_id)
                )
            else:
                raise RuntimeError("Connector Endpoint ID is empty")

        except Exception as e:
            print(f"Failed to read endpoint: {str(e)}")
            raise e

    @staticmethod
    def _read_endpoint(ep_id: str) -> dict:
        """
        Reads the endpoint information from a JSON file and adds the creation datetime.

        This method accepts an endpoint ID as an argument, locates the corresponding JSON file in the directory
        defined by `EnvironmentVars.CONNECTORS_ENDPOINTS`, and returns a dictionary that encapsulates the endpoint's
        details along with its creation datetime. If any error occurs during the process, it is handled by the calling
        method.

        Args:
            ep_id (str): The unique identifier of the endpoint to be retrieved.

        Returns:
            dict: A dictionary containing the details of the retrieved endpoint along with its creation datetime.
        """
        connector_endpoint_info = Storage.read_object(
            EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, "json"
        )
        creation_datetime = Storage.get_creation_datetime(
            EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, "json"
        )
        connector_endpoint_info["created_date"] = creation_datetime.replace(
            microsecond=0
        ).isoformat(" ")
        return connector_endpoint_info

    @staticmethod
    def update(ep_args: ConnectorEndpointArguments) -> bool:
        """
        Updates the endpoint information based on the provided arguments.

        This method takes a ConnectorEndpointArguments object, converts it to a dictionary, and removes the
        'created_date' key if it exists. It then writes the updated information to the corresponding JSON file
        in the directory specified by `EnvVariables.CONNECTORS_ENDPOINTS`.

        Args:
            ep_args (ConnectorEndpointArguments): An object containing the updated details of the endpoint.

        Returns:
            bool: True if the update operation was successful.

        Raises:
            Exception: If there's an error during the update process.
        """
        try:
            # Convert the endpoint arguments to a dictionary
            # Remove created_date if it exists
            ep_info = ep_args.to_dict()
            ep_info.pop("created_date", None)

            # Write the updated endpoint information to the file
            Storage.create_object(
                EnvVariables.CONNECTORS_ENDPOINTS.name, ep_args.id, ep_info, "json"
            )
            return True

        except Exception as e:
            print(f"Failed to update endpoint: {str(e)}")
            raise e

    @staticmethod
    @validate_call
    def delete(ep_id: str) -> bool:
        """
        Deletes the endpoint with the specified ID.

        This method attempts to delete the endpoint corresponding to the given ID from the storage.
        If the deletion is successful, it returns True. If an error occurs, it prints an error message
        and re-raises the exception.

        Args:
            ep_id (str): The unique identifier of the endpoint to be deleted.

        Returns:
            bool: True if the endpoint was successfully deleted.

        Raises:
            Exception: If the deletion process encounters an error.
        """
        try:
            Storage.delete_object(EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, "json")
            return True

        except Exception as e:
            print(f"Failed to delete endpoint: {str(e)}")
            raise e

    @staticmethod
    def get_available_items() -> tuple[list[str], list[ConnectorEndpointArguments]]:
        """
        Fetches the details of all available endpoints.

        This method traverses the specified directory for connector endpoints, reads the information of each endpoint
        from its corresponding JSON file, and assembles a list of endpoint IDs along with their respective details.
        It excludes any files that are not valid endpoints (for instance, system files that begin with "__").
        The method returns a tuple comprising a list of endpoint IDs and a list of ConnectorEndpointArguments objects,
        each encapsulating the details of an endpoint.

        Returns:
            tuple[list[str], list[ConnectorEndpointArguments]]: A tuple containing a list of endpoint IDs and a list of
            ConnectorEndpointArguments objects with endpoint details.
        """
        try:
            retn_eps = []
            retn_eps_ids = []

            eps = Storage.get_objects(EnvVariables.CONNECTORS_ENDPOINTS.name, "json")
            for ep in eps:
                if "__" in ep:
                    continue

                ep_info = ConnectorEndpointArguments(
                    **ConnectorEndpoint._read_endpoint(Path(ep).stem)
                )
                retn_eps.append(ep_info)
                retn_eps_ids.append(ep_info.id)

            return retn_eps_ids, retn_eps

        except Exception as e:
            print(f"Failed to get available endpoints: {str(e)}")
            raise e
