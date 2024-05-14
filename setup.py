import os
import platform
import subprocess
import sys
import threading

# static variables
repos = [
    ("https://github.com/moonshot-admin/moonshot-ui", "dev-main"),
    ("https://github.com/moonshot-admin/moonshot-data", "main"),
]

base_directory = "moonshot"  # Directory where the repositories will be cloned
version = "0.3.5"  # Version number of the moonshot library to install


def run_subprocess(*args, **kwargs):
    """
    Run a subprocess with the option to use shell=True on Windows.
    """
    if platform.system() == "Windows":
        kwargs["shell"] = True
    return subprocess.run(*args, **kwargs)


def install_moonshot(version=version):
    """
    Install moonshot from pip
    """
    # Check if moonshot is already installed
    reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    installed_packages = [r.decode().split("==")[0] for r in reqs.split()]

    if "moonshot" not in installed_packages:
        print("Installing moonshot...")
        # run_subprocess(
        #     [
        #         sys.executable,
        #         "-m",
        #         "pip",
        #         "install",
        #         f"projectmoonshot-imda[all]=={version}",
        #     ],
        #     check=True,
        # )
        run_subprocess(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-i",
                "https://test.pypi.org/simple/",
                "--extra-index-url",
                "https://pypi.org/simple/",
                f"projectmoonshot-imda[all]=={version}",
            ],
            check=True,
        )

    else:
        print("Moonshot is already installed.")


def ms_lib_env_file(dir):
    """
    Writes the env file to be used for moonshot library
    """
    data_repo_name = "moonshot-data"
    env_content_data = f"""
    # For Data
    ATTACK_MODULES="{data_repo_name}/attack-modules"
    CONNECTORS="{data_repo_name}/connectors"
    CONNECTORS_ENDPOINTS="{data_repo_name}/connectors-endpoints"
    CONTEXT_STRATEGY="{data_repo_name}/context-strategy"
    COOKBOOKS="{data_repo_name}/cookbooks"
    DATABASES="{data_repo_name}/generated-outputs/databases"
    DATABASES_MODULES="{data_repo_name}/databases-modules"
    DATASETS="{data_repo_name}/datasets"
    IO_MODULES="{data_repo_name}/io-modules"
    METRICS="{data_repo_name}/metrics"
    PROMPT_TEMPLATES="{data_repo_name}/prompt-templates"
    RECIPES="{data_repo_name}/recipes"
    RESULTS="{data_repo_name}/generated-outputs/results"
    RESULTS_MODULES="{data_repo_name}/results-modules"
    RUNNERS="{data_repo_name}/generated-outputs/runners"
    RUNNERS_MODULES="{data_repo_name}/runners-modules"
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
    # Write the .env content to the file at the given directory
    with open(os.path.join(dir, ".env"), "w") as env_file:
        combined_content = env_content_data + env_content_web_api
        env_file.write(combined_content.strip())


def ms_ui_env_file(dir):
    """
    Write the env file to be used with moonshot ui
    """
    env_content = """
    # This should be the URL of the Moonshot Web Api module which was started in the previous section.
    # Check the startup logs to determine the hostname and port number.
    MOONSHOT_API_URL=http://127.0.0.1:5000
    """
    # Write the .env content to a file
    with open(os.path.join(dir, ".env"), "w") as env_file:
        env_file.write(env_content.strip())


def clone_and_install_repos(repositories, base_dir):
    """
    Clone the repo and install the dependency needed.
    """
    # Create the base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Change directory to the base directory
    os.chdir(base_dir)

    for repo, branch_name in repositories:
        folder_name = repo.split("/")[-1].replace(".git", "")

        # Check if the directory already exists
        if os.path.exists(folder_name):
            print(
                f"Directory {folder_name} already exists, skipping clone and installation."
            )
        else:
            print(f"Cloning {repo}")
            # Clone the repository
            subprocess.run(["git", "clone", repo], check=True)

            # Change directory to the folder
            os.chdir(folder_name)

            # Checkout the branch
            subprocess.run(["git", "checkout", branch_name], check=True)

            print(f"Installing requirements for {folder_name}")
            # Install the requirements if they exist
            if os.path.exists("requirements.txt"):
                subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
            elif os.path.exists("package.json"):
                subprocess.run(["npm", "install"], check=True)
                subprocess.run(["npm", "run", "build"], check=True)

            # Change back to the base directory
            os.chdir("..")


def run_moonshot_ui_dev():
    """
    To start a thread to run the Moonshot UI
    """
    base_directory = os.getcwd()
    ui_dev_dir = os.path.join(base_directory, "moonshot-ui")

    ms_ui_env_file(ui_dev_dir)
    subprocess.run(["npm", "start"], cwd=ui_dev_dir)


def run_moonshot_lib(action):
    base_directory = os.getcwd()

    ms_lib_env_file(base_directory)

    if action == "cli":
        subprocess.run(["python3", "-m", "moonshot", "cli", "interactive"])
    elif action == "web-api":
        subprocess.run(["python3", "-m", "moonshot", "web-api"])


if __name__ == "__main__":
    install_moonshot(version)
    clone_and_install_repos(repos, base_directory)
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "web":
            lib_thread = threading.Thread(
                target=run_moonshot_lib, args=("web-api",)
            ).start()
            ui_thread = threading.Thread(target=run_moonshot_ui_dev).start()
        elif action == "cli":
            cli_thread = threading.Thread(
                target=run_moonshot_lib, args=("cli",)
            ).start()

    else:
        print("No action specified for moonshot library.")
