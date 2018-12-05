from click import echo

import crayons

from . import environment


INDENT_SIZE = 3


def _print(prefix: str, string: str, indent: bool = False):
    full_string = "{0} {1}".format(prefix, string)
    if indent:
        full_string = "{0}{1}".format((" " * INDENT_SIZE), full_string)
    echo(full_string)


def print_info(string: str, indent: bool = False):
    _print(crayons.blue("=>"), string, indent)


def print_warning(string: str, indent: bool = False):
    _print(crayons.yellow("=>"), string, indent)


def print_error(string: str, indent: bool = False):
    _print(crayons.red("=>"), string, indent)


def print_verbose(string: str, indent: bool = False):
    if environment.verbosity:
        _print(crayons.magenta("=>"), string, indent)
