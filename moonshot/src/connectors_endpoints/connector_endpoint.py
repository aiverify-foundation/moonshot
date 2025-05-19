from pathlib import Path

from pydantic import constr, validate_call
from slugify import slugify

from moonshot.src.configs.env_variables import EnvVariables
from moonshot.src.connectors_endpoints.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.storage.storage import Storage
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)


class ConnectorEndpoint:
    CONNECTOR_ENDPOINT_CREATE_ERROR = (
        "[ConnectorEndpoint] Failed to create connector endpoint: {message}"
    )
    CONNECTOR_ENDPOINT_DELETE_ERROR = (
        "[ConnectorEndpoint] Failed to delete connector endpoint: {message}"
    )
    CONNECTOR_ENDPOINT_GET_AVAILABLE_ITEMS_ERROR = (
        "[ConnectorEndpoint] Failed to get available connector endpoints: {message}"
    )
    CONNECTOR_ENDPOINT_READ_ERROR = (
        "[ConnectorEndpoint] Failed to read connector endpoint: {message}"
    )
    CONNECTOR_ENDPOINT_READ_INVALID = "Invalid connector endpoint id - {ep_id}"
    CONNECTOR_ENDPOINT_UPDATE_ERROR = (
        "[ConnectorEndpoint] Failed to update connector endpoint: {message}"
    )

    @staticmethod
    @validate_call
    def create(ep_args: ConnectorEndpointArguments) -> str:
        """
        Creates a new connector endpoint and stores its details as a JSON object.

        This method accepts a ConnectorEndpointArguments object, generates a unique slugified ID from the endpoint's
        name, and stores the endpoint's details in a JSON file within a specified directory.

        The directory path is determined by the `EnvVariables.CONNECTORS_ENDPOINTS` environment variable.
        Upon successful creation, the method returns the unique ID of the endpoint.
        If an error occurs during the creation process, the method raises an exception and logs the error message.

        Args:
            ep_args (ConnectorEndpointArguments): The details of the endpoint to be created,
            encapsulated in a ConnectorEndpointArguments object.

        Returns:
            str: The unique ID of the newly created endpoint, derived from slugifying the endpoint's name.

        Raises:
            Exception: If an error occurs during the creation process, including issues with storing the endpoint's
            details.
        """
        try:
            ep_id = slugify(ep_args.name, lowercase=True)
            ep_info = {
                "name": ep_args.name,
                "connector_type": ep_args.connector_type,
                "uri": ep_args.uri,
                "token": ep_args.token,
                "max_calls_per_second": ep_args.max_calls_per_second,
                "max_concurrency": ep_args.max_concurrency,
                "model": ep_args.model,
                "params": ep_args.params,
            }

            # Write as json output
            Storage.create_object(
                EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, ep_info, "json"
            )
            return ep_id

        except Exception as e:
            logger.error(
                ConnectorEndpoint.CONNECTOR_ENDPOINT_CREATE_ERROR.format(message=str(e))
            )
            raise e

    @staticmethod
    @validate_call
    def read(ep_id: constr(min_length=1)) -> ConnectorEndpointArguments:
        """
        Retrieves the details of a specified endpoint by its ID.

        This method searches for the endpoint's corresponding JSON file within the directory defined by the
        `EnvVariables.CONNECTORS_ENDPOINTS` environment variable. It then constructs and returns a
        ConnectorEndpointArguments object populated with the endpoint's details. If the endpoint ID is not found or
        any other error occurs, an exception is raised with an appropriate error message.

        Args:
            ep_id (constr(min_length=1)): The unique identifier of the endpoint whose details are to be retrieved.

        Returns:
            ConnectorEndpointArguments: An instance filled with the endpoint's details.

        Raises:
            RuntimeError: If the specified endpoint does not exist.
            Exception: For any issues encountered during the file reading or data parsing process.
        """
        try:
            endpoint_details = ConnectorEndpoint._read_endpoint(ep_id)
            if not endpoint_details:
                raise RuntimeError(
                    ConnectorEndpoint.CONNECTOR_ENDPOINT_READ_INVALID.format(
                        ep_id=ep_id
                    )
                )

            return ConnectorEndpointArguments(**endpoint_details)

        except Exception as e:
            logger.error(
                ConnectorEndpoint.CONNECTOR_ENDPOINT_READ_ERROR.format(message=str(e))
            )
            raise e

    @staticmethod
    def _read_endpoint(ep_id: str) -> dict:
        """
        Retrieves the endpoint's information from a JSON file, including its creation datetime.

        This internal method is designed to fetch the details of a specific endpoint by its ID. It searches for the
        corresponding JSON file within the directory specified by `EnvVariables.CONNECTORS_ENDPOINTS`. The method
        returns a dictionary containing the endpoint's information, enriched with the creation datetime. Errors
        encountered during this process are managed by the method that invokes this one.

        Args:
            ep_id (str): The unique identifier of the endpoint whose information is being retrieved.

        Returns:
            dict: A dictionary with the endpoint's information, including its creation datetime.
        """
        connector_endpoint_info = {"id": ep_id}
        connector_endpoint_info.update(
            Storage.read_object(EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, "json")
        )
        creation_datetime = Storage.get_creation_datetime(
            EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, "json"
        )
        connector_endpoint_info["created_date"] = creation_datetime.replace(
            microsecond=0
        ).isoformat(" ")
        return connector_endpoint_info

    @staticmethod
    @validate_call
    def update(ep_args: ConnectorEndpointArguments) -> bool:
        """
        Updates the endpoint information in the storage based on the provided ConnectorEndpointArguments object.

        This method serializes the provided ConnectorEndpointArguments object into a dictionary, excluding the 'id' and
        'created_date' keys. It then persists the updated information to the corresponding JSON file within the
        directory defined by `EnvVariables.CONNECTORS_ENDPOINTS`.

        This operation ensures that the endpoint's mutable attributes are updated according to the provided arguments.

        Args:
            ep_args (ConnectorEndpointArguments): The object encapsulating the updated attributes of the endpoint.

        Returns:
            bool: True if the update was successfully persisted to the storage; otherwise, an exception is raised.

        Raises:
            Exception: If the update process encounters an error, potentially due to issues with data serialization or
            storage access.
        """
        try:
            # Serialize the ConnectorEndpointArguments object to a dictionary and remove derived properties
            ep_info = ep_args.to_dict()
            ep_info.pop("id", None)  # The 'id' is derived and should not be written
            ep_info.pop(
                "created_date", None
            )  # The 'created_date' is derived and should not be written

            # Write the updated endpoint information to the storage
            Storage.create_object(
                EnvVariables.CONNECTORS_ENDPOINTS.name, ep_args.id, ep_info, "json"
            )
            return True

        except Exception as e:
            logger.error(
                ConnectorEndpoint.CONNECTOR_ENDPOINT_UPDATE_ERROR.format(message=str(e))
            )
            raise e

    @staticmethod
    @validate_call
    def delete(ep_id: constr(min_length=1)) -> bool:
        """
        Deletes the endpoint with the specified ID.

        This method attempts to delete the endpoint corresponding to the given ID from the storage.
        If the deletion is successful, it returns True. If an error occurs, it logs an error message
        and re-raises the exception.

        Args:
            ep_id (constr(min_length=1)): The unique identifier of the endpoint to be deleted

        Returns:
            bool: True if the endpoint was successfully deleted; otherwise, an exception is raised.

        Raises:
            Exception: If the deletion process encounters an error.
        """
        try:
            Storage.delete_object(EnvVariables.CONNECTORS_ENDPOINTS.name, ep_id, "json")
            return True

        except Exception as e:
            logger.error(
                ConnectorEndpoint.CONNECTOR_ENDPOINT_DELETE_ERROR.format(message=str(e))
            )
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

        Raises:
            Exception: If the process of fetching available items encounters an error.
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
            logger.error(
                ConnectorEndpoint.CONNECTOR_ENDPOINT_GET_AVAILABLE_ITEMS_ERROR.format(
                    message=str(e)
                )
            )
            raise e
