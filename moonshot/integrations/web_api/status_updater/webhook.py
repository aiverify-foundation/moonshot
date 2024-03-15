import json
import logging
import requests

from dependency_injector.wiring import inject
from ..services.benchmark_test_state import BenchmarkTestState
from .interface.benchmark_callback_handler import InterfaceBenchmarkCallbackHandler
from ..types.types import CookbookTestRunProgress

class Webhook(InterfaceBenchmarkCallbackHandler):
  @inject
  def __init__(self, benchmark_test_state: BenchmarkTestState) -> None:
      self.benchmark_test_state = benchmark_test_state

  def on_executor_update(self, progress_data: CookbookTestRunProgress) -> None:
    logger = logging.getLogger();
    print("\033[94m" + "-"*100 + "\033[0m")
    logger.debug(json.dumps(progress_data, indent=2))
    
    self.benchmark_test_state.update_state(progress_data)

    try:
        response = requests.post("http://localhost:3000/api/v1/status", json=progress_data) # TODO - move url to config and use pydantic to validate progress_data because it's going across the wire
        response.raise_for_status()
        logger.log(level=logging.DEBUG, msg=response.json());
        logger.log(level=logging.INFO, msg="Progress data successfully sent to the server.")
    except requests.RequestException as e:
        logger.critical(msg=f"Failed to send progress data: {e}")


