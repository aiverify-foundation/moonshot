import cmd2

from moonshot.interface.cli.initialisation.connection import *
from moonshot.src.common.env_variables import __app_name__, __version__


@cmd2.with_default_category("Initialisation")
class InitialisationCommandSet(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    def do_interactive(self, _: cmd2.Statement) -> None:
        """
        Run the interactive shell.
        """
        # To prevent 'interactive is not a recognized command, alias, or macro' from triggering.
        pass

    def do_list_connect_types(self, _: cmd2.Statement) -> None:
        list_connect_types()

    def do_list_endpoints(self, _: cmd2.Statement) -> None:
        list_endpoints()

    def do_version(self, _: cmd2.Statement) -> None:
        """
        Get the version of the application.
        """
        print(f"{__app_name__} v{__version__}")
