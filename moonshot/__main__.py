import argparse
import os
import platform
import shutil
import subprocess
import sys
import threading
import warnings
from typing import Any

from dotenv import dotenv_values

from moonshot.api import api_set_environment_variables
from moonshot.src.utils.log import configure_logger

# Create a logger for this module
logger = configure_logger(__name__)

"""
Run the Moonshot application
"""


def run_subprocess(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess:
    """
    Run a subprocess with the option to use shell=True on Windows.
    """
    if platform.system() == "Windows":
        kwargs["shell"] = True
    return subprocess.run(*args, **kwargs)


def ms_lib_env_file(data_repo_name: str) -> None:
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


def ms_ui_env_file(ui_repo: str) -> None:
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


def download_nltk_resources() -> None:
    """
    Download and verify necessary NLTK resources.

    This function downloads a predefined list of NLTK resources and verifies their availability.
    If a resource fails to download or verify, a warning is logged and an exception is raised.
    """
    import nltk

    resources = [
        "punkt",
        "stopwords",
    ]

    for resource in resources:
        try:
            nltk.download(resource)
            # Check if the resource is available
            nltk.data.find(
                f"tokenizers/{resource}"
            ) if resource == "punkt" else nltk.data.find(f"corpora/{resource}")
            logger.info(f"Successfully downloaded and verified {resource}")
        except LookupError:
            logger.warning(f"Failed to download {resource}")
            raise
        except Exception as e:
            logger.warning(f"An error occurred while downloading {resource}: {e}")
            raise


def download_spacy_model() -> None:
    """
    Downloads the en_core_web_lg model using the spacy module (for entity processor module).
    """
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_lg"])


def moonshot_data_installation(unattended: bool, overwrite: bool) -> None:
    """
    Install Moonshot Data from GitHub.

    This function clones the Moonshot Data repository from GitHub, installs its requirements,
    and sets up the necessary environment. If the target directory already exists, it handles
    the situation based on the 'unattended' and 'overwrite' flags.

    Args:
        unattended (bool): If True, the function will not prompt the user for input.
        overwrite (bool): If True, the existing directory will be removed before installation.
    """
    logger.info("Installing Moonshot Data from GitHub")
    repo = "https://github.com/aiverify-foundation/moonshot-data.git"
    folder_name = repo.split("/")[-1].replace(".git", "")
    do_install = True

    if os.path.exists(folder_name):
        if overwrite:
            logger.info(f"Removing directory {folder_name} due to --overwrite flag.")
            shutil.rmtree(folder_name)
        else:
            logger.warning(f"Directory {folder_name} already exists.")
            if not unattended:
                user_input = (
                    input(
                        f"Directory {folder_name} already exists. Do you want to remove it and reinstall? (Y/n): "
                    )
                    .strip()
                    .lower()
                )
                if user_input == "y":
                    logger.info(f"Removing directory {folder_name}.")
                    shutil.rmtree(folder_name)
                else:
                    logger.info("Skipping removal of directory.")
                    do_install = False
            else:
                do_install = False
                logger.info(
                    "Unattended mode detected. To reinstall, please use the --overwrite flag."
                )

    if do_install:
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
        download_nltk_resources()
        download_spacy_model()

    # Change back to the base directory
    os.chdir("..")


def check_node() -> bool:
    """
    Check if Node.js is installed on the user's machine.
    """
    try:
        result = subprocess.run(
            ["node", "--version"], capture_output=True, text=True, check=True
        )
        node_version = result.stdout.strip()
        logger.info(f"Node.js is installed. Version: {node_version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Node.js is not installed. Please install Node.js to proceed.")
        return False


def moonshot_ui_installation(unattended: bool, overwrite: bool) -> None:
    """
    Install Moonshot UI from GitHub.
    """
    if not check_node():
        logger.error("Node.js is not installed. Please install Node.js to proceed.")
        return

    logger.info("Installing Moonshot UI from GitHub")
    repo = "https://github.com/aiverify-foundation/moonshot-ui.git"
    folder_name = repo.split("/")[-1].replace(".git", "")
    do_install = True

    if os.path.exists(folder_name):
        if overwrite:
            logger.info(f"Removing directory {folder_name} due to --overwrite flag.")
            shutil.rmtree(folder_name)
        else:
            logger.warning(f"Directory {folder_name} already exists.")
            if not unattended:
                user_input = (
                    input(
                        f"Directory {folder_name} already exists. Do you want to remove it and reinstall? (Y/n): "
                    )
                    .strip()
                    .lower()
                )
                if user_input == "y":
                    logger.info(f"Removing directory {folder_name}.")
                    shutil.rmtree(folder_name)
                else:
                    logger.info("Skipping removal of directory.")
                    do_install = False
            else:
                do_install = False
                logger.info(
                    "Unattended mode detected. To reinstall, please use the --overwrite flag."
                )

    if do_install:
        logger.info(f"Cloning {repo}")
        # Clone the repository
        run_subprocess(["git", "clone", repo], check=True)

        # Create .env for UI
        ms_ui_env_file(folder_name)

    # Change directory to the folder
    os.chdir(folder_name)

    logger.info(f"Installing requirements for {folder_name}")
    # Install the requirements if they exist
    if os.path.exists("package.json"):
        run_subprocess(["npm", "install"], check=True)
        run_subprocess(["npm", "run", "build"], check=True)

    # Change back to the base directory
    os.chdir("..")


def run_moonshot_ui() -> None:
    """
    To start a thread to run the Moonshot UI
    """
    base_directory = os.getcwd()
    ui_dir = os.path.join(base_directory, "moonshot-ui")

    if not os.path.exists(ui_dir):
        logger.error(
            "moonshot-ui does not exist. Please run with '-i moonshot-ui' to install moonshot-ui first."
        )
        sys.exit(1)
    # ms_ui_env_file(ui_dev_dir)
    run_subprocess(["npm", "start"], cwd=ui_dir)


def main() -> None:
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
    parser.add_argument(
        "-u",
        "--unattended",
        action="store_true",
        help="Perform action without user interaction",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Force delete and reinstall the specified module",
    )

    args = parser.parse_args()

    # Handle installations based on the -i include arguments
    if "moonshot-data" in args.install:
        moonshot_data_installation(args.unattended, args.overwrite)

    if "moonshot-ui" in args.install:
        moonshot_ui_installation(args.unattended, args.overwrite)

    # If mode is not specified, skip running any modes
    if args.mode is None:
        return

    if args.mode == "help":
        parser.print_help()
        sys.exit(0)

    api_set_environment_variables(dotenv_values(args.env))

    if args.mode == "web-api":
        from moonshot.integrations.web_api import __main__ as web_api

        web_api.start_app()
    elif args.mode == "web":
        # Create and start the UI dev server thread
        ui_thread = threading.Thread(target=run_moonshot_ui)
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
        sys.exit(0)


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()
