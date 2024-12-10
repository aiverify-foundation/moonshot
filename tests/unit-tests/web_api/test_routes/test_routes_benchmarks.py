import pytest
from moonshot.integrations.web_api.services.utils.exceptions_handler import ServiceException

@pytest.mark.parametrize("benchmark_data, benchmark_type, exception,expected_status,expected_response",[
    # Success Scenario 
    (
        {
            "run_name": "test-benchmark-1",
            "description": "norman testing benchmark",
            "inputs": ["common-risk-easy"],
            "endpoints": ["openai-gpt35-turbo","openai-gpt35-turbo-16k"],
            "prompt_selection_percentage": 1,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "random_seed" : 0
        },
        "cookbook", None, 200 , {"id":"test-benchmark-1"}
    ),
    (
        {
            "run_name": "test-benchmark-1",
            "description": "norman testing benchmark",
            "inputs": ["common-risk-easy"],
            "endpoints": ["openai-gpt35-turbo","openai-gpt35-turbo-16k"],
            "prompt_selection_percentage": 100,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "random_seed" : 0
        },
        "cookbook", None, 200 , {"id":"test-benchmark-1"}
    ),
    #RECIPE
    (
        {
            "run_name": "test-benchmark-1",
            "description": "norman testing benchmark",
            "inputs": ["common-risk-easy"],
            "endpoints": ["openai-gpt35-turbo","openai-gpt35-turbo-16k"],
            "prompt_selection_percentage": 3,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "random_seed" : 0
        },
        "recipe", None, 200 , {"id":"test-benchmark-1"}
    ),
    # Exception Scenario Cookbook
    (
        {
            "run_name": "test-benchmark-1",
            "description": "norman testing benchmark",
            "inputs": ["common-risk-easy"],
            "endpoints": ["openai-gpt35-turbo","openai-gpt35-turbo-16k"],
            "prompt_selection_percentage": 3,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "random_seed" : 0
        },
        "cookbook", 
        ServiceException("An unexpected error occurred", "execute_cookbook", "UnknownError"), 500 , None
    ),
    # Exception Scenario RECIPE
    (
        {
            "run_name": "test-benchmark-1",
            "description": "norman testing benchmark",
            "inputs": ["common-risk-easy"],
            "endpoints": ["openai-gpt35-turbo","openai-gpt35-turbo-16k"],
            "prompt_selection_percentage": 3,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "random_seed" : 0
        },
        "recipe", 
        ServiceException("An unexpected error occurred", "execute_cookbook", "UnknownError"), 500 , None
    ),
    # Exception Prompt Selection <1 or >100 
    (
        {
            "run_name": "test-benchmark-range-0",
            "description": "test benchmark range 0",
            "inputs": ["common-risk-easy"],
            "endpoints": ["openai-gpt35-turbo","openai-gpt35-turbo-16k"],
            "prompt_selection_percentage": 0,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "random_seed" : 0
        },
        "cookbook", None, 422 , None
    ),
    (
        {
            "run_name": "test-benchmark-range-101",
            "description": "test benchmark range 101",
            "inputs": ["common-risk-easy"],
            "endpoints": ["openai-gpt35-turbo","openai-gpt35-turbo-16k"],
            "prompt_selection_percentage": 101,
            "system_prompt": "",
            "runner_processing_module": "benchmarking",
            "random_seed" : 0
        },
        "cookbook", None, 422 , None
    ),
])
def test_execute_benchmark_cb(test_client, mock_bm_service, benchmark_data, benchmark_type, exception, expected_status, expected_response):
    if exception:
        if benchmark_type == "cookbook":
            mock_bm_service.execute_cookbook.side_effect = exception
        elif benchmark_type == "recipe":
            mock_bm_service.execute_recipe.side_effect = exception
    else:
        if benchmark_type == "cookbook":
            mock_bm_service.execute_cookbook.return_value = benchmark_data.get("run_name")
        elif benchmark_type == "recipe":
            mock_bm_service.execute_recipe.return_value = benchmark_data.get("run_name")

    response = test_client.post(f"/api/v1/benchmarks?type={benchmark_type}", json=benchmark_data)
    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]
    else:
        if expected_status == 200:
            assert response.json() == expected_response

# not mocking response cause response too long
@pytest.mark.parametrize("exception,expected_status",[
    # Successful cases
    (None, 200),
    # Exception cases
    (ServiceException("A file not found error occurred", "get_all_progress_status", "FileNotFound"), 404),
    (ServiceException("A validation error occurred", "get_all_progress_status", "ValidationError"), 400),
    (ServiceException("An server error occurred", "get_all_progress_status", "ServerError"), 500),
])
def test_get_benchmark_progress(test_client, mock_bm_test_state, exception, expected_status):
    if exception:
        mock_bm_test_state.get_all_progress_status.side_effect = exception

    mock_bm_test_state.get_all_progress_status.return_value = {}
    response = test_client.get(f"/api/v1/benchmarks/status")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]

@pytest.mark.parametrize("runner_id, exception,expected_status",[
    ("runner_id", None, 200),
    ("runner_id", ServiceException("An server error occurred", "cancel_executor", "ServerError"), 500), 
])
def test_cancel_benchmark(test_client, mock_bm_service, runner_id, exception, expected_status):
    if exception:
        mock_bm_service.cancel_executor.side_effect = exception

    mock_bm_service.cancel_executor.return_value = {}
    response = test_client.post(f"/api/v1/benchmarks/cancel/{runner_id}")

    assert response.status_code == expected_status
    if exception:
        assert exception.msg in response.json()["detail"]

