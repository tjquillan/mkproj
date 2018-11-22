# import crayons
import crayons

from click import echo

from . import environment

def print_info(string: str, indent: bool = False):
    full_string = "{0} {1}".format(crayons.blue("=>"), string)
    if indent:
        full_string = "   {0}".format(full_string)
    echo(full_string)

def print_warning(string: str, indent: bool = False):
    full_string = "{0} {1}".format(crayons.yellow("=>"), string)
    if indent:
        full_string = "   {0}".format(full_string)
    echo(full_string)

def print_error(string: str, indent: bool = False):
    full_string = "{0} {1}".format(crayons.red("=>"), string)
    if indent:
        full_string = "   {0}".format(full_string)
    echo(full_string)

def print_verbose(string: str, indent: bool = False):
    if environment.verbosity:
        full_string = "{0} {1}".format(crayons.magenta("=>"), string)
        if indent:
            full_string = "   {0}".format(full_string)
        echo(full_string)