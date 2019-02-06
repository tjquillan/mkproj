import functools

from enum import Enum

from click import echo

import crayons

from halo import Halo

from . import environment


INDENT_SIZE = 1

SPINNER = Halo(spinner="dots", placement="right")


class PrintLevel(Enum):
    INFO: str = crayons.blue("=>")
    WARNING: str = crayons.yellow("=>")
    ERROR: str = crayons.red("=>")
    VERBOSE: str = crayons.magenta("=>")


def _format_string(level: PrintLevel, string: str, indent: bool = False) -> str:
    formated_str = "{0} {1}".format(level, string)
    if indent:
        formated_str = "{0}{1}".format(("\t" * INDENT_SIZE), formated_str)
    return formated_str


def _print(level: PrintLevel, string: str, indent: bool = False):
    full_string = _format_string(level, string, indent)
    echo(full_string)


def print_info(string: str, indent: bool = False):
    _print(PrintLevel.INFO, string, indent)


def print_warning(string: str, indent: bool = False):
    _print(PrintLevel.WARNING, string, indent)


def print_error(string: str, indent: bool = False):
    _print(PrintLevel.ERROR, string, indent)


def print_verbose(string: str, indent: bool = False):
    if environment.verbosity:
        _print(PrintLevel.VERBOSE, string, indent)


def report(string: str, indent: bool = False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            SPINNER.start(_format_string(PrintLevel.INFO, string, indent))
            try:
                func_out = func(*args, **kwargs)
                SPINNER.succeed()
                return func_out
            except Exception:
                SPINNER.fail()

        return wrapper

    return decorator
