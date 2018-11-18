from ..vendor import crayons

from click import (
    argument, command, echo, edit, group, option, pass_context, secho, version_option
)

import click_completion

from ..__version__ import __version__
from .options import (
    CONTEXT_SETTINGS, lang_option, pass_state
)

# Enable shell completion.
click_completion.init()

@command(context_settings=CONTEXT_SETTINGS)
@lang_option
@pass_state
@pass_context
@version_option(prog_name=crayons.normal("mkproj", bold=True), version=__version__)
@argument('project_name', nargs=1)
def cli(ctx, state, project_name, lang=False, **kwargs):
    print(project_name)