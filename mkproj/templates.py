from jinja2 import Environment, PackageLoader, Template, select_autoescape


ENV = Environment(
    loader=PackageLoader("mkproj", "templates"), autoescape=select_autoescape(["j2"])
)


def get(section: str, template: str):
    template_path = "{0}/{1}.j2".format(section, template)
    return ENV.get_template(template_path)


def write_to_file(file, template: Template, data: dict):
    file.write(template.render(data))
