import pytest
from pydantic import ValidationError

from moonshot.src.connectors.connector_response import ConnectorResponse


class TestCollectionConnectorResponse:
    # ------------------------------------------------------------------------------
    # Test ConnectorResponse functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "response, context",
        [
            ("", []),
            ("Response A", ["Context A"]),
            ("Response A", []),
        ],
    )
    def test_create_connector_response(self, response, context):
        # Test creating a valid connector response instance
        connector_response_args = ConnectorResponse(response=response, context=context)
        assert connector_response_args.response == response
        assert connector_response_args.context == context

    @pytest.mark.parametrize(
        "response",
        [
            ("Response A"),
        ],
    )
    def test_create_connector_response_1(self, response):
        # Test creating a valid connector response instance
        connector_response_args = ConnectorResponse(response=response)
        assert connector_response_args.response == response
        assert connector_response_args.context == []

    @pytest.mark.parametrize(
        "response, context",
        [
            (123, ["Context A"]),  # Invalid response
            ([], ["Context A"]),  # Invalid response
            ({}, ["Context A"]),  # Invalid response
            (None, ["Context A"]),  # Invalid response
            ((), ["Context A"]),  # Invalid response
            ("Response A", ""),  # Invalid context
            ("Response A", 123),  # Invalid context
            ("Response A", {}),  # Invalid context
            ("Response A", None),  # Invalid context
        ],
    )
    def test_create_connector_response_invalid(self, response, context):
        # Ensure that invalid inputs raise a ValidationError
        with pytest.raises(ValidationError):
            ConnectorResponse(response=response, context=context)

    # ------------------------------------------------------------------------------
    # Test to_dict functionality
    # ------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        "response, context",
        [
            ("Response A", ["Context A", "Context B"]),
            ("Response A", []),
        ],
    )
    def test_to_dict(self, response, context):
        connector_response_args = ConnectorResponse(response=response, context=context)
        assert connector_response_args.to_dict() == {
            "response": response,
            "context": context,
        }

    @pytest.mark.parametrize(
        "response",
        [
            ("Response A"),
        ],
    )
    def test_to_dict_1(self, response):
        # Test creating a valid connector response instance
        connector_response_args = ConnectorResponse(response=response)
        assert connector_response_args.to_dict() == {
            "response": response,
            "context": [],
        }
