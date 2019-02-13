import os
import sys

from collections.abc import MutableMapping
from threading import Lock


# Taken from pipenv
# see https://github.com/pypa/pipenv/blob/master/pipenv/__init__.py
MKPROJ_ROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
MKPROJ_VENDOR = os.sep.join([MKPROJ_ROOT, "vendor"])
MKPROJ_PATCHED = os.sep.join([MKPROJ_ROOT, "patched"])

# Inject vendored libraries into system path.
sys.path.insert(0, MKPROJ_VENDOR)
# Inject patched libraries into system path.
sys.path.insert(0, MKPROJ_PATCHED)


class LockingDict(MutableMapping):
    def __init__(self, *args, **kw):
        self._dict: dict = dict(*args, **kw)
        self._lock: Lock = Lock()

    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value

    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]

    def __delitem__(self, key):
        while self._lock:
            del self._dict[key]

    def __iter__(self):
        with self._lock:
            return iter(self._dict)

    def __len__(self):
        with self._lock:
            return len(self._dict)

    def __repr__(self):
        with self._lock:
            return self._dict.__repr__()


from .cli import cli, mkproj_config  # isort:skip # noqa: E402,F401
from .tasks import *  # isort:skip # noqa: E402,F401,F403

if __name__ == "__main__":
    cli()
