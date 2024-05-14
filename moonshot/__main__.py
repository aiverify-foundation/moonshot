import sys
import warnings
import argparse
import platform
import subprocess
import os
import threading 

from dotenv import dotenv_values
from moonshot.api import api_set_environment_variables
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

def moonshot_data_installation():
    # Code for moonshot-data installation
    print("Installing Moonshot Data from GitHub")
    repo = "https://github.com/moonshot-admin/moonshot-data"
    branch_name = "main"
    folder_name = repo.split("/")[-1].replace(".git", "")
    
    # Check if the directory already exists
    if not os.path.exists(folder_name):
        print(f"Cloning {repo}")
        # Clone the repository
        run_subprocess(["git", "clone", repo], check=True)
        
        # Change directory to the folder
        os.chdir(folder_name)
        
        # Checkout the branch
        run_subprocess(["git", "checkout", branch_name], check=True)
        
        print(f"Installing requirements for {folder_name}")
        # Install the requirements if they exist
        if os.path.exists("requirements.txt"):
            run_subprocess(["pip", "install", "-r", "requirements.txt"], check=True)
        
        # Change back to the base directory
        os.chdir("..")
    else:
        print(f"Directory {folder_name} already exists, skipping clone.")

def moonshot_ui_installation():
    # Code for moonshot-ui installation
    repo = "https://github.com/moonshot-admin/moonshot-ui"
    branch_name = "dev-main"
    folder_name = repo.split("/")[-1].replace(".git", "")
    
    # Check if the directory already exists
    if not os.path.exists(folder_name):
        print(f"Cloning {repo}")
        # Clone the repository
        run_subprocess(["git", "clone", repo], check=True)

        # Change directory to the folder
        os.chdir(folder_name)

        # Checkout the branch
        run_subprocess(["git", "checkout", branch_name], check=True)

        print(f"Installing requirements for {folder_name}")        
        # Install the requirements if they exist
        if os.path.exists("package.json"):
            run_subprocess(["npm", "install"], check=True)
            run_subprocess(["npm", "run", "build"], check=True)
        # Change back to the base directory
        os.chdir("..")
    else:
        print(f"Directory {folder_name} already exists, skipping installation.")
def run_moonshot_ui_dev():
    """
    To start a thread to run the Moonshot UI
    """
    base_directory = os.getcwd()
    ui_dev_dir = os.path.join(base_directory, "moonshot-ui")

    if not os.path.exists(ui_dev_dir):
        print("moonshot-ui does not exist. Please run with '-i moonshot-ui' to install moonshot-ui first.")
        sys.exit(1)
    # ms_ui_env_file(ui_dev_dir)
    run_subprocess(['npm', 'start'], cwd=ui_dev_dir)

def main():
    parser = argparse.ArgumentParser(description="Run the Moonshot application")
    parser.add_argument('mode', choices=['web-api', 'cli', 'web'], help='Mode to run Moonshot in')
    parser.add_argument('cli_command', nargs='?', help='The CLI command to run (e.g., "interactive")')
    parser.add_argument('-i', '--include', action='append', help='Modules to include', default=[])
    parser.add_argument('-e', '--env', type=str, help='Path to the .env file', default='.env')
    
    args = parser.parse_args()
    
    api_set_environment_variables(dotenv_values(args.env))

    # Handle installations based on the -i include arguments
    if 'moonshot-data' in args.include:
        moonshot_data_installation()

    if 'moonshot-ui' in args.include:
        moonshot_ui_installation()

    if args.mode == "web-api":
        from moonshot.integrations.web_api import __main__ as web_api
        web_api.start_app()
    elif args.mode == "web":
    # Create and start the UI de}v server thread
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