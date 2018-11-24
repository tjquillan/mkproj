import sys

from pathlib import Path

from click import echo

from . import config, printer, subprocess, templates
from .base_lang import BaseLang
from .environment import langs
from .subprocess import call


def gather_langs():
    from .langs import python

    for lang in BaseLang.__subclasses__():
        langs[lang().lang] = lang()


from .cli.options import State  # isort:skip


def create_project(project_name: str, state: State):
    # If langs have not been gathered yet gather them
    if not len(langs) > 0:
        gather_langs()

    project_path = Path("{0}/{1}".format(Path.cwd(), project_name))

    if project_path.exists():
        printer.print_error("Project already exists. Aborting...")
        sys.exit(1)

    # Allways make a project dir
    printer.print_info(
        "Creating project '{0}' at '{1}'".format(project_name, project_path.absolute())
    )
    project_path.mkdir()

    # If a language is supplied run creation tasks for the language
    if state.lang is not None:
        langs[state.lang].create(project_name, project_path)

    # Run generic creation tasks that apply to all projects
    if state.readme:
        printer.print_info("Creating file 'README.md'")
        with open("{0}/README.md".format(str(project_path.absolute())), "w") as file:
            templates.write_to_file(
                file, templates.get("base", "README.md"), {"name": project_name}
            )

    if state.git:
        printer.print_info("Initializing project as git repository")
        call(["git", "-C", project_path.absolute(), "init"])
