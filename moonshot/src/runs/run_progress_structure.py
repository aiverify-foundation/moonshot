def create_run_progress_structure():
    """
    Create a common progress structure for tracking task and prompt progress.

    Returns:
        dict: A dictionary containing the initial progress structure.
    """
    return {
        "current_progress": 0,
        "current_error_messages": [],
        "num_of_tasks_total": 0,
        "num_of_prompts_cancelled": 0,
        "num_of_prompts_completed": 0,
        "num_of_prompts_error": 0,
        "num_of_prompts_pending": 0,
        "num_of_prompts_running_metrics_calculation": 0,
        "num_of_prompts_running_query": 0,
        "num_of_prompts_total": 0,
        "cancelled_prompts": [],
        "completed_prompts": [],
        "error_prompts": [],
        "pending_prompts": [],
        "running_prompts": [],
    }
