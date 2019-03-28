import os

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    Template,
    select_autoescape,
)

from . import LockingDict, config, environment


ENV: Environment = Environment(
    loader=ChoiceLoader(
        [
            FileSystemLoader(
                [os.sep.join([environment.APP_DIRS.user_data_dir, "templates"])],
                followlinks=True,
            ),
            PackageLoader("mkproj", "templates"),
        ]
    ),
    autoescape=select_autoescape(["j2"]),
)


def get_template(section: str, template: str) -> Template:
    template_path: str = "{0}/{1}.j2".format(section, template)
    return ENV.get_template(template_path)


def render(template: Template, task_data: LockingDict) -> str:
    return template.render({"config": config.get_config, "data": task_data.get})


def write_to_file(file, template: Template, task_data: LockingDict):
    file.write(render(template, task_data))
