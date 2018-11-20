from click import echo
from pathlib import Path
import sys

from . import config, subprocess, printer
from .environment import langs
from .base_lang import BaseLang
from .subprocess import call

def gather_langs():
    from .langs import (python)

    for lang in BaseLang.__subclasses__():
        langs[lang().lang] = lang()

def create_project(project_name: str, state):
    # If langs have not been gathered yet gather them
    if not len(langs) > 0:
        gather_langs()

    project_path = Path("{0}/{1}".format(Path.cwd(), project_name))

    if project_path.exists():
        printer.print_error("Project already exists. Aborting...")
        sys.exit(1)

    langs[state.lang].create(project_name, project_path)

    if state.git:
        printer.print_info("Initializing project as git repository")
        call(["git", "-C", project_path.absolute(),"init"])


