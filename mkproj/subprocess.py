import subprocess

from . import environment


def call(command: list):
    if environment.verbosity:
        subprocess.call(command)
    else:
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
