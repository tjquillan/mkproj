import os

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    PackageLoader,
    Template,
    select_autoescape,
)

from . import environment


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


def get(section: str, template: str):
    template_path: str = "{0}/{1}.j2".format(section, template)
    return ENV.get_template(template_path)


def write_to_file(file, template: Template, data: dict = None):
    file.write(template.render(data or {}))
