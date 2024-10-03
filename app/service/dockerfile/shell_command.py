from typing import Union


class ShellCommand:
    _text: str

    def __init__(self, cmd: str):
        self._text = cmd

    def line_num(self) -> int:
        """
        Returns the line number in the Dockerfile on which is resides.
        :return: int
        """
        pass

    def program(self) -> str:
        """
        Returns the main program invoked as part of this command, ie, the first word in the text.
        eg- In "npm install", the program is "npm".
        """
        pass

    def subcommand(self) -> str:
        """
        Returns the subcommand invoked for the program.
        eg- For "npm --hello=world install --production --foo=bar ./", the subcommand is "install".
        """
        pass

    def options(self) -> dict:
        """
        Returns a dict of all options specified in this command.
        eg- "npm install --production --foo=bar --lorem=false" -> {"production": True, "foo": "bar", "lorem": False}
        """
        pass

    def text(self) -> str:
        """
        :return: the complete shell command as a string
        """
        return self._text

    def add_option(self, name: str, value: Union[str, bool]):
        """
        Adds the specified option to the command.
          eg- add_option("omit", "dev") -> "npm ci --omit=dev"
        If the value is bool and set to True, the option is added as a flag.
          If False, this method exits without making any changes to the command.
          eg- add_option("production", True) -> "npm install --production"
        """
        pass
