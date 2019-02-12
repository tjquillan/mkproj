from click import BadParameter, make_pass_decorator, option

from ..bases import BaseTask


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class State(object):
    def __init__(self):
        self.git = False
        self.lang = None
        self.readme = False


pass_state = make_pass_decorator(State, ensure=True)


def lang_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)

        if value is not None:
            # Regardless of input lang names should be handled as all lower case
            value = value.lower()
            state.lang = check_lang(ctx, param, value)
        return value

    return option(
        "--lang",
        "-l",
        default=None,
        nargs=1,
        callback=callback,
        help="Specify which language to create project with. If none is specified a generic template will be generated.",  # noqa
        expose_value=False,
    )(f)


def check_lang(ctx, param, value):
    langs = set(task.lang_id() for task in BaseTask.__subclasses__())

    if value not in langs:
        raise BadParameter("{0} is not a supported language".format(value))
    return value
