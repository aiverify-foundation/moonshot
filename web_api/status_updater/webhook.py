from typing import Any
from web_api.status_updater.interface.benchmark_callback_handler import InterfaceBenchmarkCallbackHandler
from web_api.types.types import ExecutionInfo


class Webhook(InterfaceBenchmarkCallbackHandler):

  @staticmethod
  def on_executor_update(progress_data: ExecutionInfo) -> None:
    print("\033[94m" + "-"*100 + "\033[0m")
    print(f"Execution ID: {progress_data['exec_id']}")
    print(f"Execution Name: {progress_data['exec_name']}")
    print(f"Execution Type: {progress_data['exec_type']}")
    print(f"Current Duration: {progress_data['curr_duration']} seconds")
    print(f"Current Status: {progress_data['curr_status']}")
    print(f"Current Progress: {progress_data['curr_progress']}%")
    print(f"Current Recipe: {progress_data['curr_recipe_name']} (Index: {progress_data['curr_recipe_index']})")
    print("\033[94m" + "-"*100 + "\033[0m")
      

    

