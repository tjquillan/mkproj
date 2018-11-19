import os
import sys

from .cli import cli

# Taken from pipenv
# see https://github.com/pypa/pipenv/blob/master/pipenv/__init__.py
ROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
VENDOR = os.sep.join([ROOT, "vendor"])
PATCHED = os.sep.join([ROOT, "patched"])
# Inject vendored libraries into system path.
sys.path.insert(0, VENDOR)
# Inject patched libraries into system path.
sys.path.insert(0, PATCHED)

if __name__ == '__main__':
    cli()
