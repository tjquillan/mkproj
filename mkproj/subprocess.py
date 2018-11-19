import subprocess

verbose = False

def set_verbosity(verbosity):
    global verbose
    verbose = verbosity

def call(command: list):
    global verbose
    if verbose:
        subprocess.call(command)
    else:
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)