from moonshot.api import (
    api_create_connector_from_endpoint,
    api_create_connectors_from_endpoints,
    api_create_endpoint,
    api_delete_endpoint,
    api_get_all_connector_type,
    api_get_all_endpoint,
    api_get_all_endpoint_name,
    api_read_endpoint,
    api_update_endpoint,
)


# ------------------------------------------------------------------------------
# Connector and Connector endpoints APIs Test
# ------------------------------------------------------------------------------
def test_create_connector_endpoint():
    api_create_endpoint(
        name="My New GPT4",
        connector_type="openai-connector",
        uri="1234",
        token="1234",
        max_calls_per_second=256,
        max_concurrency=1,
        model="HelloWorld",
        params={"hello": "world"},
    )


def test_read_connector_endpoint():
    print(api_read_endpoint("my-new-gpt4"))


def test_update_connector_endpoint():
    api_update_endpoint(
        "my-new-gpt4", uri="4567", token="4567", params={"hello": "world1"}
    )


def test_delete_connector_endpoint():
    # Delete endpoint if do not exists
    try:
        api_delete_endpoint("endpoint123")
        print("Delete endpoint if exist: FAILED")
    except Exception:
        print("Delete endpoint if do not exist: PASSED")

    # Delete endpoint if exists
    try:
        api_delete_endpoint("my-new-gpt4")
        print("Delete endpoint if exist: PASSED")
    except Exception:
        print("Delete endpoint if exist: FAILED")


def test_get_all_connector_endpoint():
    print(api_get_all_endpoint())


def test_get_all_connector_endpoint_name():
    print(api_get_all_endpoint_name())


def test_create_connector_from_ep():
    # Recreate connector endpoint
    test_create_connector_endpoint()

    # Create new connector
    connector = api_create_connector_from_endpoint("my-new-gpt4")
    print(connector)
    print("Connector ID: ", connector.id)
    print("Connector Endpoint: ", connector.endpoint)
    print("Connector Token: ", connector.token)
    print("Max Concurrency: ", connector.max_concurrency)
    print("Max Calls Per Second: ", connector.max_calls_per_second)
    print("Additional Params: ", connector.params)
    print("Connector PrePrompt: ", connector.pre_prompt)
    print("Connector PostPrompt: ", connector.post_prompt)
    print("Rate Limiter: ", connector.rate_limiter)
    print("Tokens: ", connector.tokens)
    print("Updated at: ", connector.updated_at)
    print("Semaphore: ", connector.semaphore)
    print("Timeout: ", connector.timeout)
    print("Number of attempts: ", connector.max_attempts)

    # Delete connector endpoint
    test_delete_connector_endpoint()


def test_create_connectors_from_eps():
    # Recreate connector endpoint
    test_create_connector_endpoint()

    # Create new connector
    connectors = api_create_connectors_from_endpoints(
        ["my-new-gpt4", "my-new-gpt4", "my-new-gpt4"]
    )
    for connector_no, connector in enumerate(connectors, 1):
        print("-" * 100)
        print("Connector No. ", connector_no)
        print("Connector ID: ", connector.id)
        print("Connector Endpoint: ", connector.endpoint)
        print("Connector Token: ", connector.token)
        print("Max Concurrency: ", connector.max_concurrency)
        print("Max Calls Per Second: ", connector.max_calls_per_second)
        print("Additional Params: ", connector.params)
        print("Connector PrePrompt: ", connector.pre_prompt)
        print("Connector PostPrompt: ", connector.post_prompt)
        print("Rate Limiter: ", connector.rate_limiter)
        print("Tokens: ", connector.tokens)
        print("Updated at: ", connector.updated_at)
        print("Semaphore: ", connector.semaphore)
        print("Timeout: ", connector.timeout)
        print("Number of attempts: ", connector.max_attempts)

    # Delete connector endpoint
    test_delete_connector_endpoint()


def test_get_all_connector_type():
    print(api_get_all_connector_type())


def test_run_connector_endpoints_api():
    # ------------------------------------------------------------------------------
    # Connector endpoints APIs Test
    # ------------------------------------------------------------------------------
    # Create connector endpoint
    print("=" * 100, "\nTest creating connector endpoint")
    test_create_connector_endpoint()

    # Read connector endpoint
    print("=" * 100, "\nTest reading connector endpoint")
    test_read_connector_endpoint()

    # Update connector endpoint
    print("=" * 100, "\nTest updating connector endpoint")
    test_update_connector_endpoint()

    # Read connector endpoint
    print("=" * 100, "\nTest reading connector endpoint after updating")
    test_read_connector_endpoint()

    # Delete connector endpoint
    print("=" * 100, "\nTest deleting connector endpoint")
    test_delete_connector_endpoint()

    # List all connector endpoints
    print("=" * 100, "\nTest listing all connector endpoint")
    test_get_all_connector_endpoint()

    # List all connector endpoints names
    print("=" * 100, "\nTest listing all connector endpoint names")
    test_get_all_connector_endpoint_name()


def test_run_connector_api():
    # ------------------------------------------------------------------------------
    # Connector APIs Test
    # ------------------------------------------------------------------------------
    # Create new connector
    print("=" * 100, "\nTest creating new connector from endpoints")
    test_create_connector_from_ep()

    # Create new connectors
    print("=" * 100, "\nTest creating new connectors")
    test_create_connectors_from_eps()

    # Create new connectors
    print("=" * 100, "\nTest getting all connector type")
    test_get_all_connector_type()
