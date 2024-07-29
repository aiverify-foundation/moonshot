import argparse
import os
import platform
import subprocess
import sys
import threading
import warnings

from dotenv import dotenv_values

from moonshot.api import api_set_environment_variables
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)

"""
Run the Moonshot application
"""


def run_subprocess(*args, **kwargs):
    """
    Run a subprocess with the option to use shell=True on Windows.
    """
    if platform.system() == "Windows":
        kwargs["shell"] = True
    return subprocess.run(*args, **kwargs)


def ms_lib_env_file(data_repo_name):
    """
    Writes the env file to be used for moonshot library
    """
    env_content_data = f"""
    # For Data
    ATTACK_MODULES="./{data_repo_name}/attack-modules"
    BOOKMARKS="./{data_repo_name}/generated-outputs/bookmarks"
    CONNECTORS="./{data_repo_name}/connectors"
    CONNECTORS_ENDPOINTS="./{data_repo_name}/connectors-endpoints"
    CONTEXT_STRATEGY="./{data_repo_name}/context-strategy"
    COOKBOOKS="./{data_repo_name}/cookbooks"
    DATABASES="./{data_repo_name}/generated-outputs/databases"
    DATABASES_MODULES="./{data_repo_name}/databases-modules"
    DATASETS="./{data_repo_name}/datasets"
    IO_MODULES="./{data_repo_name}/io-modules"
    METRICS="./{data_repo_name}/metrics"
    PROMPT_TEMPLATES="./{data_repo_name}/prompt-templates"
    RECIPES="./{data_repo_name}/recipes"
    RESULTS="./{data_repo_name}/generated-outputs/results"
    RESULTS_MODULES="./{data_repo_name}/results-modules"
    RUNNERS="./{data_repo_name}/generated-outputs/runners"
    RUNNERS_MODULES="./{data_repo_name}/runners-modules"
    TOKENIZERS_PARALLELISM = false
    """

    env_content_web_api = """
    # For Web API
    HOST_ADDRESS=127.0.0.1 # The interface the server will bind to
    HOST_PORT=5000

    # Below is the uri of the Web UI webhook.
    # In the next section, if Web UI listens on a different port,
    # update this uri accordingly and restart.

    MOONSHOT_UI_CALLBACK_URL=http://localhost:3000/api/v1/benchmarks/status
    """
    with open(".env", "w") as env_file:
        combined_content = env_content_data + env_content_web_api
        env_file.write(combined_content.strip())


def ms_ui_env_file(ui_repo):
    """
    Write the env file to be used with moonshot ui
    """
    env_content = """
    # This should be the URL of the Moonshot Web Api module which was started in the previous section.
    # Check the startup logs to determine the hostname and port number.
    MOONSHOT_API_URL=http://127.0.0.1:5000
    """
    # Write the .env content to a file
    with open(os.path.join(ui_repo, ".env"), "w") as env_file:
        env_file.write(env_content.strip())


def moonshot_data_installation():
    # Code for moonshot-data installation
    logger.info("Installing Moonshot Data from GitHub")
    repo = "https://github.com/aiverify-foundation/moonshot-data.git"
    folder_name = repo.split("/")[-1].replace(".git", "")

    # Check if the directory already exists
    if not os.path.exists(folder_name):
        logger.info(f"Cloning {repo}")
        # Clone the repository
        run_subprocess(["git", "clone", repo], check=True)

        # Create .env to point to installed folder
        ms_lib_env_file(folder_name)

        # Change directory to the folder
        os.chdir(folder_name)

        logger.info(f"Installing requirements for {folder_name}")
        # Install the requirements if they exist
        if os.path.exists("requirements.txt"):
            run_subprocess(["pip", "install", "-r", "requirements.txt"], check=True)
            import nltk

            nltk.download("punkt")
            nltk.download("stopwords")
            nltk.download("averaged_perceptron_tagger")
            nltk.download("universal_tagset")

        # Change back to the base directory
        os.chdir("..")

    else:
        logger.warning(f"Directory {folder_name} already exists, skipping clone.")


def moonshot_ui_installation():
    # Code for moonshot-ui installation
    repo = "https://github.com/aiverify-foundation/moonshot-ui.git"
    folder_name = repo.split("/")[-1].replace(".git", "")

    # Check if the directory already exists
    if not os.path.exists(folder_name):
        logger.info(f"Cloning {repo}")
        # Clone the repository
        run_subprocess(["git", "clone", repo], check=True)

        # Change directory to the folder
        os.chdir(folder_name)

        logger.info(f"Installing requirements for {folder_name}")
        # Install the requirements if they exist
        if os.path.exists("package.json"):
            run_subprocess(["npm", "install"], check=True)
            run_subprocess(["npm", "run", "build"], check=True)

        # Change back to the base directory
        os.chdir("..")

        # Create .env for ui
        ms_ui_env_file(folder_name)
    else:
        logger.warning(
            f"Directory {folder_name} already exists, skipping installation."
        )


def run_moonshot_ui_dev():
    """
    To start a thread to run the Moonshot UI
    """
    base_directory = os.getcwd()
    ui_dev_dir = os.path.join(base_directory, "moonshot-ui")

    if not os.path.exists(ui_dev_dir):
        logger.error(
            "moonshot-ui does not exist. Please run with '-i moonshot-ui' to install moonshot-ui first."
        )
        sys.exit(1)
    # ms_ui_env_file(ui_dev_dir)
    run_subprocess(["npm", "start"], cwd=ui_dev_dir)


def main():
    parser = argparse.ArgumentParser(description="Run the Moonshot application")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["web-api", "cli", "web", "help"],
        help="Mode to run Moonshot in",
        default=help,
    )
    parser.add_argument(
        "cli_command", nargs="?", help='The CLI command to run (e.g., "interactive")'
    )
    parser.add_argument(
        "-i",
        "--install",
        action="append",
        choices=["moonshot-data", "moonshot-ui"],
        help="Modules to install",
        default=[],
    )
    parser.add_argument(
        "-e", "--env", type=str, help="Path to the .env file", default=".env"
    )

    args = parser.parse_args()

    # Handle installations based on the -i include arguments
    if "moonshot-data" in args.install:
        moonshot_data_installation()

    if "moonshot-ui" in args.install:
        moonshot_ui_installation()

    # If mode is not specified, skip running any modes
    if args.mode is None:
        return

    if args.mode == "help":
        parser.print_help()
        sys.exit(1)

    api_set_environment_variables(dotenv_values(args.env))

    if args.mode == "web-api":
        from moonshot.integrations.web_api import __main__ as web_api

        web_api.start_app()
    elif args.mode == "web":
        # Create and start the UI dev server thread
        ui_thread = threading.Thread(target=run_moonshot_ui_dev)
        ui_thread.start()
        ui_thread.join(timeout=0.1)  # Wait briefly for the thread to become alive
        if not ui_thread.is_alive():
            sys.exit(1)
        from moonshot.integrations.web_api import __main__ as web_api

        web_api.start_app()
    elif args.mode == "cli":
        from moonshot.integrations.cli import __main__ as cli

        cli.start_app(args.cli_command)

        # Handle CLI mode here, possibly also with additional arguments
        pass
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()
