import click.types
from click import (
    BadParameter, make_pass_decorator, option
)
from ..core import gather_langs
from ..environment import langs

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

class State(object):
    def __init__(self):
        self.git = False
        self.lang = None

pass_state = make_pass_decorator(State, ensure=True)

def git_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)

        if value:
            state.git = value
        return value
    return option("--git", "-g", is_flag=True, expose_value=False, callback=callback,
                  help="Specify whether to init project with git.", type=click.types.BOOL)(f)
            

def lang_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        
        # Regardless of input lang names should be handled as all lower case
        value = value.lower()

        if value is not None:
            state.lang = check_lang(ctx, param, value)
        return value
    return option("--lang", "-l", default=False, nargs=1, callback=callback,
                  help="Specify which language to create project with. If none is specified a generic template will be generated.",
                  expose_value=False)(f)

def check_lang(ctx, param, value):
    if not len(langs) > 0:
        gather_langs()
        
    if value not in langs:
        raise BadParameter("{0} is not a supported language".format(value))
    return value