import sys
import warnings

from moonshot.integrations.cli.cli import CommandLineInterface


def start_app():
    """
    Run the Moonshot application
    """
    # Setting the warnings to be ignored
    warnings.filterwarnings("ignore")

    cli_instance = CommandLineInterface()
    if "interactive" in sys.argv:
        # Run in interactive mode
        cli_instance.debug = False
        cli_instance.cmdloop("Starting moonshot interactive prompt...")
    else:
        # Run in non-interactive mode
        arguments = sys.argv[2:]
        if arguments:
            arguments = " ".join(arguments)
            cli_instance.onecmd(arguments)
        else:
            cli_instance.onecmd("help")


if __name__ == "__main__":
    start_app()
