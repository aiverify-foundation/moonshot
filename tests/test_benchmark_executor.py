from typing import Callable
from moonshot.src.benchmarking.executors.benchmark_executor import BenchmarkExecutor
from moonshot.src.benchmarking.executors.benchmark_executor_arguments import BenchmarkExecutorArguments
from moonshot.src.benchmarking.executors.benchmark_executor_types import BenchmarkExecutorTypes

def progress_callback_func(progress_dict: dict):
    print("Received new progress update:", progress_dict)

def create_new_executor(id, name, type):
    print(f"="*50)
    print(f"Create new executor id: {id}")
    bm_executor = BenchmarkExecutor.create_executor(BenchmarkExecutorArguments(id=id,name=name,type=type))
    print("Benchmark Executor Attributes:")
    print("ID:", bm_executor.id)
    print("Name:", bm_executor.name)
    print("Type:", bm_executor.type)
    print("Start Time:", bm_executor.start_time)
    print("End Time:", bm_executor.end_time)
    print("Duration:", bm_executor.duration)
    print("Database Instance:", bm_executor.database_instance)
    print("Database File:", bm_executor.database_file)
    print("Results File:", bm_executor.results_file)
    print("Recipes:", bm_executor.recipes)
    print("Cookbooks:", bm_executor.cookbooks)
    print("Endpoints:", bm_executor.endpoints)
    print("Number of Prompts:", bm_executor.num_of_prompts)
    print("Results:", bm_executor.results)
    print("Status:", bm_executor.status)
    print("Progress Callback Function:", bm_executor.progress_callback_func)

def load_current_executor(id):
    print(f"="*50)
    print(f"Loading current executor id: {id}")
    bm_executor = BenchmarkExecutor.load_executor(id)
    print("Benchmark Executor Attributes:")
    print("ID:", bm_executor.id)
    print("Name:", bm_executor.name)
    print("Type:", bm_executor.type)
    print("Start Time:", bm_executor.start_time)
    print("End Time:", bm_executor.end_time)
    print("Duration:", bm_executor.duration)
    print("Database Instance:", bm_executor.database_instance)
    print("Database File:", bm_executor.database_file)
    print("Results File:", bm_executor.results_file)
    print("Recipes:", bm_executor.recipes)
    print("Cookbooks:", bm_executor.cookbooks)
    print("Endpoints:", bm_executor.endpoints)
    print("Number of Prompts:", bm_executor.num_of_prompts)
    print("Results:", bm_executor.results)
    print("Status:", bm_executor.status)
    print("Progress Callback Function:", bm_executor.progress_callback_func)

def update_current_executor(id, name, type, recipes, endpoints, num_of_prompts, progress_callback):
    print(f"="*50)
    print(f"Update current executor id: {id}")
    BenchmarkExecutor.update_executor(
        BenchmarkExecutorArguments(
            id=id,
            name=name,
            type=type,
            recipes=recipes,
            endpoints=endpoints,
            num_of_prompts=num_of_prompts,
            progress_callback_func=progress_callback
        )
    )

def get_available_executors():
    print(f"="*50)
    print(f"Get available executor")
    be_ids, be_args = BenchmarkExecutor.get_available_executors()
    for bm_id, (be_id, be_arg) in enumerate(zip(be_ids, be_args), 1):
        print(bm_id, be_id, be_arg)

def delete_executor(id):
    print(f"="*50)
    print(f"Delete executor id: {id}")
    BenchmarkExecutor.delete_executor(id)

def create_new_and_run_recipe(name: str, type: BenchmarkExecutorTypes, recipes: list[str], endpoints: list[str], 
                              num_of_prompts: int, progress_callback: Callable):
    print(f"="*50)
    print(f"Create new executor and run: {name}")
    be_args = BenchmarkExecutorArguments(
        id="",
        name=name,
        type=type,
        recipes=recipes,
        endpoints=endpoints,
        num_of_prompts=num_of_prompts,
        progress_callback_func=progress_callback
    )
    benchmark_executor = BenchmarkExecutor.create_executor(be_args)
    benchmark_executor.execute()

def load_and_run_recipe(id: str):
    print(f"="*50)
    print(f"Load current executor and run: {id}")
    benchmark_executor = BenchmarkExecutor.load_executor(id)
    benchmark_executor.execute()

def run_test():
    id = "recipe-my-new-executor"
    name = "recipe_my_new executor"
    type = BenchmarkExecutorTypes.RECIPE
    recipes = ["bbq"]
    endpoints = ["openai-gpt35-lionel"]
    num_of_prompts = 1
    progress_callback=progress_callback_func

    create_new_executor(id, name, type)
    update_current_executor(id, name, type, recipes, endpoints, num_of_prompts, progress_callback)
    load_current_executor(id)
    get_available_executors()
    delete_executor(id)

    create_new_and_run_recipe(name, type, recipes, endpoints, num_of_prompts, progress_callback)
    load_and_run_recipe(id)
    delete_executor(id)

if __name__ == "__main__":
    run_test()