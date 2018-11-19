from ..vendor import crayons

from click import (
    argument, command, echo, edit, group, option, pass_context, secho, version_option
)

from ..__version__ import __version__
from ..subprocess import set_verbosity
from .options import (
    CONTEXT_SETTINGS, LANG_MANAGER, lang_option, pass_state
)

@command(context_settings=CONTEXT_SETTINGS)
@lang_option
@option("--git", "-g", is_flag=True)
@pass_state
@pass_context
@option("--verbose", "-v", is_flag=True)
@version_option(prog_name=crayons.normal("mkproj", bold=True), version=__version__)
@argument('project_name', nargs=1)
def cli(ctx, state, project_name, lang=False, git=False, verbose=False):
    set_verbosity(verbose)
    LANG_MANAGER.create(project_name, state.lang, git)
