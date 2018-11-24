import os
import sys


# Taken from pipenv
# see https://github.com/pypa/pipenv/blob/master/pipenv/__init__.py
MKPROJ_ROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
MKPROJ_VENDOR = os.sep.join([MKPROJ_ROOT, "vendor"])
MKPROJ_PATCHED = os.sep.join([MKPROJ_ROOT, "patched"])

# Inject vendored libraries into system path.
sys.path.insert(0, MKPROJ_VENDOR)
# Inject patched libraries into system path.
sys.path.insert(0, MKPROJ_PATCHED)

from .cli import cli, mkproj_config  # isort:skip

if __name__ == "__main__":
    cli()
