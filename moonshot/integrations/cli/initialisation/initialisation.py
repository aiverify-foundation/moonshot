import cmd2


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
