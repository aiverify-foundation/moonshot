from moonshot.src.configs.env_variables import EnvironmentVars


# ------------------------------------------------------------------------------
# Environment Variables APIs
# ------------------------------------------------------------------------------
def api_set_environment_variables(env_vars: dict) -> None:
    """
    Sets the environment variables for the current session.

    This function takes a dictionary of environment variables and sets them for the current session
    by loading them into the EnvironmentVars configuration.

    Args:
        env_vars (dict): A dictionary containing the environment variables to set.

    Returns:
        None
    """
    EnvironmentVars.load_env(env_vars)
