from enum import Enum

from yaspin import yaspin
from yaspin.core import Yaspin

import crayons

from log_symbols import LogSymbols

from . import environment


INDENT_SIZE = 1


class PrintLevel(Enum):
    INFO: str = crayons.blue("=>")
    WARNING: str = crayons.yellow("=>")
    ERROR: str = crayons.red("=>")
    VERBOSE: str = crayons.magenta("=>")
    SPECIAL: str = crayons.cyan("=>")


def _format_string(level: PrintLevel, string: str, indent: bool = False) -> str:
    formated_str: str = "{0} {1}".format(level, string)
    if indent:
        formated_str = "{0}{1}".format(("\t" * INDENT_SIZE), formated_str)
    return formated_str


SPINNER: Yaspin = yaspin(
    text=_format_string(PrintLevel.SPECIAL, "Setting up project..."), side="right"
)


def start():
    SPINNER.start()


def stop():
    SPINNER.stop()


def ok():
    SPINNER.ok(LogSymbols.SUCCESS.value)


def fail():
    SPINNER.fail(LogSymbols.ERROR.value)


def _print(level: PrintLevel, string: str, indent: bool = False):
    SPINNER.write(_format_string(level, string, indent))


def print_info(string: str, indent: bool = False):
    _print(PrintLevel.INFO, string, indent)


def print_warning(string: str, indent: bool = False):
    _print(PrintLevel.WARNING, string, indent)


def print_error(string: str, indent: bool = False):
    _print(PrintLevel.ERROR, string, indent)


def print_verbose(string: str, indent: bool = False):
    if environment.verbosity:
        _print(PrintLevel.VERBOSE, string, indent)
