# import crayons
import crayons

from click import echo

from .environment import verbosity

def print_info(string: str):
    echo("{0} {1}".format(crayons.blue("=>"), string))

def print_warning(string: str):
    echo("{0} {1}".format(crayons.yellow("=>"), string))

def print_error(string: str):
    echo("{0} {1}".format(crayons.red("=>"), string))

def log(string: str):
    if verbosity:
        echo("{0} {1}".format(crayons.magenta("=>"), string))