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
    elif option == "cli":
        cli_instance = CommandLineInterface()
        if "interactive" in sys.argv:
            cli_instance.debug = False
            cli_instance.cmdloop("Starting moonshot interactive prompt.")
        else:
            arguments = sys.argv[2:]
            if arguments:
                arguments = " ".join(arguments)
                cli_instance.onecmd(arguments)
            else:
                cli_instance.onecmd("help")
    else:
        print(
            "Unrecognised arguments. Available arguments are web-api, cli <cli command>, cli interactive.\n"
        )
        print("e.g. python -m moonshot web-api")
        print("e.g. python -m moonshot cli list_sessions")
        print("e.g. python -m moonshot cli interactive\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
