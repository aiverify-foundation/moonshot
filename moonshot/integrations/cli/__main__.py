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
        cli_instance.debug = True
        cli_instance.cmdloop("Starting moonshot interactive prompt...")
    else:
        # Run in non-interactive mode
        arguments = sys.argv[1:]
        if arguments:
            arguments = f"{sys.argv[1]} "
            for arg in sys.argv[2:]:
                arguments += f'"{arg}" '
            cli_instance.onecmd(arguments)
        else:
            cli_instance.onecmd("help")


if __name__ == "__main__":
    start_app()
