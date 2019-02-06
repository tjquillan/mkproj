import sys

from pathlib import Path

from . import printer, templates
from .base_lang import BaseLang
from .environment import langs
from .subprocess import call


def gather_langs():
    from .langs import python  # noqa: F401

    for lang in BaseLang.__subclasses__():
        langs[lang.lang_id()] = lang


def constuct_langs(project_name: str, project_path: Path):
    for lang in langs:
        langs[lang] = langs[lang](project_name, project_path)


from .cli.options import State  # isort:skip # noqa: E402


def create_project(project_name: str, state: State):
    project_path = Path("{0}/{1}".format(Path.cwd(), project_name))

    @printer.report(
        "Creating project '{0}' at '{1}'".format(project_name, project_path.absolute())
    )
    def make_proj_dir():
        project_path.mkdir()

    @printer.report("Creating file 'README.md'")
    def make_readme():
        with open("{0}/README.md".format(str(project_path.absolute())), "w") as file:
            templates.write_to_file(
                file, templates.get("base", "README.md"), {"name": project_name}
            )

    @printer.report("Initializing project as git repository")
    def init_git():
        call(["git", "-C", project_path.absolute(), "init"])

    if project_path.exists():
        printer.print_error("Project already exists. Aborting...")
        sys.exit(1)

    # Allways make a project dir
    make_proj_dir()

    # If a language is supplied run creation tasks for the language
    if state.lang is not None:
        # If langs have not been gathered yet gather them
        if not langs:
            gather_langs()
        constuct_langs(project_name, project_path)
        langs[state.lang].create()

    # Run generic creation tasks that apply to all projects
    if state.readme:
        make_readme()

    if state.git:
        init_git()
