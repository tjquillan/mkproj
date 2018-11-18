import click.types
from click import (
    make_pass_decorator, option
)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

class State(object):
    def __init__(self):
        self.lang = None

pass_state = make_pass_decorator(State, ensure=True)

def lang_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        if value is not None:
            state.lang = value
        return value
    return option("--lang", "-l", default=False, nargs=1, callback=callback,
                  help="Specify which language to create project with. If none is specified a generic\ntemplate will be generated.",
                  expose_value=False)(f)