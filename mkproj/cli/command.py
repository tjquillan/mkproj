import crayons

from click import (
    argument, command, echo, edit, group, option, pass_context, secho, version_option
)

from ..__version__ import __version__
from ..environment import verbosity
from ..core import create_project
from .options import (
    CONTEXT_SETTINGS, git_option, lang_option, pass_state
)

@command(context_settings=CONTEXT_SETTINGS)
@lang_option
@git_option
@pass_state
@pass_context
@option("--verbose", "-v", is_flag=True)
@version_option(prog_name=crayons.normal("mkproj", bold=True), version=__version__)
@argument('project_name', nargs=1)
def cli(ctx, state, project_name, lang=False, git=False, verbose=False):
    global verbosity
    verbosity = verbose
    create_project(project_name, state)

if __name__ == "__main__":
    cli()
