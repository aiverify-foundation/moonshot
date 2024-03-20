import sys
import warnings

from moonshot.integrations.cli.cli import CommandLineInterface
from moonshot.integrations.web_api import __main__ as web_api

"""
Run the Moonshot application
"""
# Setting the warnings to be ignored
warnings.filterwarnings("ignore")


def main():
    if len(sys.argv) < 2:
        print("Invalid number of argument given.")
        sys.exit(1)
    option = sys.argv[1]
    if option == "web-api":
        web_api.start_app()
    elif option == "interactive":
        cli_instance = CommandLineInterface()
        cli_instance.debug = False
        cli_instance.cmdloop("Starting moonshot interactive prompt.")
    else:
        print("Unrecognised arguments. Please use web-api or CLI interactive.")
        sys.exit(1)


if __name__ == "__main__":
    main()
