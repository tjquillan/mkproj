from click import argument, command, option, pass_context, version_option

import crayons

from .. import environment
from ..__version__ import __version__
from ..config import set_config
from ..core import create_project
from .options import CONTEXT_SETTINGS, lang_option, mixins_option, pass_state


@command(context_settings=CONTEXT_SETTINGS)
@lang_option
@mixins_option
@pass_state
@pass_context
@option("--verbose", "-v", is_flag=True)
@version_option(prog_name=crayons.normal("mkproj", bold=True), version=__version__)
@argument("project_name", nargs=1)
def cli(ctx, state, project_name, lang=False, verbose=False):
    environment.verbosity = verbose

    create_project(project_name, state)


@command(context_settings=CONTEXT_SETTINGS)
@argument("config", nargs=1)
@argument("value", nargs=1)
def mkproj_config(config, value):
    section, key = str(config).split(".")
    set_config(section, key, value)


if __name__ == "__main__":
    cli()
