import warnings

from moonshot.integrations.cli.cli import CommandLineInterface


def start_app(cli_command=None):
    """
    Run the Moonshot application
    """
    # Setting the warnings to be ignored
    warnings.filterwarnings("ignore")

    cli_instance = CommandLineInterface()
    if cli_command == "interactive":
        # Run in interactive mode
        cli_instance.debug = False
        cli_instance.cmdloop("Starting moonshot interactive prompt...")
    elif cli_command:
        # Run a specific command
        cli_instance.onecmd(cli_command)
    else:
        # Show help if no command is provided
        cli_instance.onecmd("help")
