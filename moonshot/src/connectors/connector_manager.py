import asyncio
import datetime
import glob
import json
import os
import time
from functools import partial
from pathlib import Path
from typing import Any, Callable, Union

import aiometer
from pydantic.v1 import validate_arguments
from slugify import slugify

from moonshot.src.configs.env_variables import EnvironmentVars
from moonshot.src.connectors.connector import Connector
from moonshot.src.connectors.connector_endpoint_arguments import (
    ConnectorEndpointArguments,
)
from moonshot.src.connectors.connector_prediction_arguments import (
    ConnectorPredictionArguments,
)


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
            endpoint_id = slugify(ep_args.name, lowercase=False)
            endpoint_info = {
                "id": endpoint_id,
                "name": ep_args.name,
                "connector_type": ep_args.connector_type,
                "uri": ep_args.uri,
                "token": ep_args.token,
                "max_calls_per_second": ep_args.max_calls_per_second,
                "max_concurrency": ep_args.max_concurrency,
                "params": ep_args.params,
            }
            endpoint_filepath = (
                f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{endpoint_id}.json"
            )
            with open(endpoint_filepath, "w") as json_file:
                json.dump(endpoint_info, json_file, indent=2)

        except Exception as e:
            print(f"Failed to create endpoint: {str(e)}")
            raise e

    @staticmethod
    @validate_arguments
    def read_endpoint(ep_id: str) -> ConnectorEndpointArguments:
        """
        Reads and returns the information of a specified endpoint.

        This method reads the endpoint information from a JSON file based on the provided endpoint ID. It constructs
        the file path using the endpoint ID, reads the file, and loads the JSON content. Additionally, it fetches the
        creation timestamp of the file, converts it to a datetime object, and adds the creation date to the endpoint
        information before returning it as a ConnectorEndpointArguments object.

        Args:
            ep_id (str): The ID of the endpoint to read.

        Returns:
            ConnectorEndpointArguments: An object containing the endpoint's information, including its creation date.
        """
        try:
            # Construct the file path
            connector_endpoint_filepath = (
                f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/{ep_id}.json"
            )
            with open(connector_endpoint_filepath, "r") as json_file:
                creation_timestamp = os.path.getctime(connector_endpoint_filepath)
                creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)
                endpoints_info = json.load(json_file)
                endpoints_info["created_date"] = (
                    creation_datetime.replace(microsecond=0)
                    .isoformat()
                    .replace("T", " ")
                )
                return ConnectorEndpointArguments(**endpoints_info)

        except Exception as e:
            print(f"Failed to read endpoint: {str(e)}")
            raise e

    @staticmethod
    def update_endpoint(ep_args: ConnectorEndpointArguments) -> bool:
        # TODO: Update endpoint
        return False

    @staticmethod
    @validate_arguments
    def delete_endpoint(ep_id: str) -> bool:
        # TODO: Delete endpoint
        return False

    @staticmethod
    def get_available_endpoints() -> tuple[list[str], list[ConnectorEndpointArguments]]:
        """
        Retrieves a list of available endpoints and their details.

        This method scans the designated directory for JSON files representing connector endpoints, excluding any
        files that are marked as hidden or temporary (denoted by "__" in their filename). It reads each file, extracts
        the endpoint information, including the creation date, and constructs a list of ConnectorEndpointArguments
        objects. Additionally, it compiles a list of endpoint IDs. Both lists are returned as a tuple.

        Returns:
            tuple[list[str], list[ConnectorEndpointArguments]]: A tuple containing a list of endpoint IDs and a list
            of ConnectorEndpointArguments objects, each representing the details of an available endpoint.
        """
        try:
            endpoints = []
            endpoints_id = []
            filepaths = glob.glob(f"{EnvironmentVars.CONNECTORS_ENDPOINTS}/*.json")
            for filepath in filepaths:
                if "__" in filepath:
                    continue

                with open(filepath, "r") as json_file:
                    creation_timestamp = os.path.getctime(filepath)
                    creation_datetime = datetime.datetime.fromtimestamp(
                        creation_timestamp
                    )
                    endpoints_info = json.load(json_file)
                    endpoints_info["created_date"] = (
                        creation_datetime.replace(microsecond=0)
                        .isoformat()
                        .replace("T", " ")
                    )
                    endpoints.append(ConnectorEndpointArguments(**endpoints_info))
                    endpoints_id.append(endpoints_info["id"])

            return endpoints_id, endpoints

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
    def get_available_connectors() -> list[str]:
        """
        Retrieves a list of available connectors by scanning a specified directory for Python files.

        This method scans the directory specified by the `EnvironmentVars.CONNECTORS` environment variable for
        Python files, excluding any that are special or private files (denoted by "__" in their names). It
        extracts and returns the stem (the filename without the extension) of each Python file found, which
        represents the available connector names.

        Returns:
            list[str]: A list of the names of available connectors.
        """
        try:
            return [
                Path(fp).stem
                for fp in glob.iglob(f"{EnvironmentVars.CONNECTORS}/*.py")
                if "__" not in fp
            ]

        except Exception as e:
            print(f"Failed to get available connectors: {str(e)}")
            raise e

    # @staticmethod
    # async def get_multiple_predictions(args: ConnectorPredictionArguments) -> Any:
    #     """
    #     Retrieves multiple predictions based on the given prompts.

    #     Args:
    #         args (ConnectorPredictionArguments): The arguments for making predictions.

    #     Returns:
    #         list: A list of results from the predictions.
    #     """
    #     try:
    #         print("Performing multiple predictions")

    #         # Store all the needed tasks
    #         coroutines = []
    #         for (
    #                 prompt_template_name,
    #                 prompts_template_info,
    #         ) in args.prompts_template_info.items():
    #             prompts_tasks = [
    #                 partial(
    #                     ConnectorManager._get_async_predictions_helper,
    #                     prompt_index,
    #                     prompt_info,
    #                     args.connector,
    #                     partial(
    #                         args.prompts_callback_function,
    #                         prompt_template_name,
    #                     ),
    #                 )
    #                 for prompt_index, prompt_info in enumerate(prompts_template_info["data"])
    #             ]

    #             # Run predictions async
    #             print(
    #                 f"Total number of prompts {len(prompts_tasks)} "
    #                 f"and concurrency {args.connector.api_max_concurrency} "
    #                 f"and calls per second {args.connector.api_max_calls_per_second}"
    #             )

    #             # Add to coroutines
    #             coroutines.append(
    #                 ConnectorManager._get_async_predictions(
    #                     prompts_tasks,
    #                     args.connector.api_max_concurrency,
    #                     args.connector.api_max_calls_per_second,
    #                 )
    #             )

    #         # Return results
    #         return await asyncio.gather(*coroutines)

    #     except Exception as e:
    #         print(f"Failed to get multiple predictions: {str(e)}")
    #         raise e

    @staticmethod
    def get_predictions(pred_args: ConnectorPredictionArguments) -> list:
        """
        Synchronously gets predictions for a set of prompts using the specified connector.

        This method orchestrates the process of making asynchronous prediction requests for each prompt
        defined in the `pred_args`. It utilizes the connector's capabilities to manage API call concurrency
        and rate limiting, ensuring efficient and compliant use of the external prediction service.

        Args:
            pred_args (ConnectorPredictionArguments): An object containing all necessary information
                for making prediction requests, including the connector instance, prompts information,
                and an optional callback function for handling individual prompt predictions.

        Returns:
            list: A list of prediction results, where each result corresponds to a prompt in the order
                they were provided.

        Raises:
            Exception: If any error occurs during the prediction process.
        """
        try:
            print("Performing predictions")

            # Store all the needed tasks
            prompts_tasks = [
                partial(
                    ConnectorManager._get_async_predictions_helper,
                    prompt_index,
                    prompt_info,
                    pred_args.connector,
                    pred_args.prompts_callback_function,
                )
                for prompt_index, prompt_info in enumerate(
                    pred_args.prompts_template_info["data"]
                )
            ]

            # Run predictions async
            print(
                f"Total number of prompts {len(prompts_tasks)} "
                f"and concurrency {pred_args.connector.max_concurrency} "
                f"and calls per second {pred_args.connector.max_calls_per_second}"
            )
            prediction_results = asyncio.run(
                ConnectorManager._get_async_predictions(
                    prompts_tasks,
                    pred_args.connector.max_concurrency,
                    pred_args.connector.max_calls_per_second,
                )
            )

            # Return results
            return prediction_results

        except Exception as e:
            print(f"Failed to get predictions: {str(e)}")
            raise e

    @staticmethod
    async def _get_async_predictions_helper(
        prompt_index: int,
        prompt_info: dict,
        connector: Connector,
        prompt_callback: Union[Callable, None],
    ) -> dict:
        """
        Asynchronously helps in getting predictions for a single prompt.

        This function is a helper function designed to work within an asynchronous context to fetch predictions
        for a single prompt. It checks if the prediction result already exists in the prompt information; if not,
        it proceeds to predict using the provided connector. The function also measures the duration of the prediction
        process and updates the prompt information with the prediction result and the duration. If a prompt callback
        is provided, it will be called with the updated prompt information and the connector ID.

        Args:
            prompt_index (int): The index of the prompt in the list of prompts being processed.
            prompt_info (dict): A dictionary containing information about the prompt, including any pre-existing
                                prediction results.
            connector (Connector): The connector instance to use for making the prediction.
            prompt_callback (Union[Callable, None]): An optional callback function that, if provided, is called with
                                                     the updated prompt information and the connector ID.

        Returns:
            dict: The updated prompt information dictionary, including the prediction result and the duration of the
                  prediction process.
        """
        if "predicted_result" not in prompt_info:
            print(f"Predicting prompt {prompt_index} [{connector.id}]")
            start_time = time.perf_counter()

            predicted_result = await connector.get_response(prompt_info["prompt"])
            duration = time.perf_counter() - start_time
            print(f"[Prompt {prompt_index}] took {duration:.4f}s")

            # Update prompt info
            prompt_info.update(
                {
                    "predicted_result": predicted_result,
                    "duration": duration,
                }
            )

            # Call prompt callback
            if prompt_callback:
                prompt_callback(prompt_info, connector.id)

        return prompt_info

    @staticmethod
    async def _get_async_predictions(
        prompts_tasks: list, max_at_once: int, max_calls_per_second: int
    ) -> list[Any]:
        """
        Asynchronously gathers predictions for a batch of prompts.

        This method is responsible for managing the asynchronous execution of prediction tasks for a batch of prompts.
        It leverages aiometer's run_all function to concurrently execute a given number of tasks at once, adhering to
        the specified maximum number of calls per second. This method ensures that the predictions are efficiently
        gathered by controlling the concurrency level and the rate of making prediction calls, which can be crucial
        for adhering to rate limits of external APIs or services.

        Args:
            prompts_tasks (list): A list of coroutine objects, each representing a task for getting a prediction for
                                  a single prompt.
            max_at_once (int): The maximum number of tasks that should be run concurrently.
            max_calls_per_second (int): The maximum number of calls that should be made per second.

        Returns:
            list[Any]: A list containing the results of the prediction tasks. The contents of the list depend on the
                       implementation of the tasks provided in `prompts_tasks`.
        """
        return await aiometer.run_all(
            prompts_tasks, max_at_once=max_at_once, max_per_second=max_calls_per_second
        )
