import subprocess

from .environment import verbosity

def call(command: list):
    if verbosity:
        subprocess.call(command)
    else:
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)