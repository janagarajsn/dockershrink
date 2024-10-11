from typing import Union, List, Dict, TypeAlias, Tuple

ShellCommandFlagValue: TypeAlias = Union[str, bool]
ShellCommandFlags: TypeAlias = Dict[str, ShellCommandFlagValue]


def split_chained_commands(cmd_string: str) -> list:
    """
    Takes a string containing one or more shell commands chained together and splits them into individual commands.
    Also returns the operator between 2 commands.
    eg-
      "echo hello world && npx depcheck || apt-get install foo -y; /scripts/myscript.sh"
      => ["echo hello world", "&&", "npx depcheck", "||", "apt-get install foo -y", ";", "/scripts/myscript.sh"]
    """
    # TODO(p0)
    # https://github.com/djmattyg007/python-shell-parser
    # https://github.com/idank/bashlex
    pass


def parse_flags(raw: Tuple[str]) -> ShellCommandFlags:
    """
    Parses commandline flags.
    eg-
      "--foo --bar=true --bax=false" => {"foo": True, "bar": True}
      "--mount=type=cache,type=local" => {"mount": "type=cache,type=local"}
    :param raw:
    :return:
    """
    # TODO(p0)
    flags = {}
    for kv in raw:
        flags[key] = value

    return flags


class ShellCommand:
    _parent_layer = None
    _index: int
    _line: int
    _cmd: Tuple[str]
    _program: str
    _args: List[str]
    _flags: ShellCommandFlags

    def __init__(self, index: int, line_num: int, parent_layer, cmd: Tuple[str]):
        self._parent_layer = parent_layer
        self._index = index
        self._line = line_num
        self._cmd = cmd

        # TODO(p0): parse cmd into program, args, flags and assign
        # OR parse the command outside and just give to this class

    def line_num(self) -> int:
        """
        Returns the line number in the Dockerfile on which is resides.
        :return: int
        """
        return self._line

    def program(self) -> str:
        """
        Returns the main program invoked as part of this command, ie, the first word in the text.
        eg- In "npm install", the program is "npm".
        """
        return self._program

    def args(self) -> List[str]:
        """
        Returns a list of arguments passed to the program.
        eg-
          "npm --foo=bar run test --production" -> ["run", "test"]
          "npm" -> []
        """
        return self._args

    def subcommand(self) -> str:
        """
        Returns the subcommand invoked for the program.
        This method is a wrapper around args()[0]
        eg-
          For "npm --hello=world install --production --foo=bar ./", the subcommand is "install".
          For "npm", the subcommand is "".
        """
        args = self.args()
        return args[0] if len(args) > 0 else ""

    def options(self) -> ShellCommandFlags:
        """
        Returns a dict of all options specified in this command.
        eg- "npm install --production --foo=bar --lorem=false" -> {"production": True, "foo": "bar", "lorem": False}
        """
        return self._flags

    def text(self) -> str:
        """
        :return: the complete shell command as a string
        """
        return self._text

    # TODO(p0): Either remove this or return a new ShellCommand object with modifications
    def add_option(self, name: str, value: ShellCommandFlagValue):
        """
        Adds the specified option to the command.
          eg- add_option("omit", "dev") -> "npm ci --omit=dev"
        If the value is bool and set to True, the option is added as a flag.
          If False, this method exits without making any changes to the command.
          eg- add_option("production", True) -> "npm install --production"
        """
        pass

    def parent_layer(self):
        """
        Returns this shell command's parent Layer (specifically, RunLayer).
        :return: RunLayer
        """
        return self._parent_layer

    def index(self) -> int:
        """
        Returns the position of this command inside the RunLayer.
        ShellCommands are 0-indexed but their indices are unique only within their Layer.
        eg-
          FROM ubuntu:latest
          RUN npm run build \\               (command layer 0)
              apt-get install foobar \\      (command layer 1)
              npm start                      (command layer 2)

          RUN npm run build \\               (command layer 0)
              apt-get install foobar \\      (command layer 1)
              npm start                      (command layer 2)
        """
        return self._index

    def parsed_command(self) -> Tuple[str]:
        return self._cmd