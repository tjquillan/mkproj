from click import BadParameter, make_pass_decorator, option

from ..bases import BaseTask


CONTEXT_SETTINGS: dict = {"help_option_names": ["-h", "--help"]}


class State():  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.lang = None
        self.mixins = []


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
        help="Specify which language to create project with. If none are specified a generic template will be generated.",  # pylint: disable=line-too-long
        expose_value=False,
    )(f)


def mixins_option(f):
    def callback(ctx, param, value):  # pylint: disable=unused-argument
        state = ctx.ensure_object(State)

        if value is not None:
            # Regardless of input mixin names should be handled as all lower case
            value = value.lower()
            value.strip(" ")
            value = value.split(",")
            state.mixins = value
        return value

    return option(
        "--mixins",
        "-m",
        default=None,
        nargs=1,
        callback=callback,
        help="""Specify which mixins to create project with. Mixins should be seperated with a comma. If none are specified no mixins will be used.""",  # pylint: disable=line-too-long
        expose_value=False,
    )(f)


def check_lang(ctx, param, value):  # pylint: disable=unused-argument
    langs: set = {task.lang_id() for task in BaseTask.__subclasses__()}

    if value not in langs:
        raise BadParameter("{0} is not a supported language".format(value))
    return value
