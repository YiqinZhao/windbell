import json

from windbell.core.mail import submit
from windbell.core.windfile import Windfile


def send(config, template):
    """send email

    :param config: email configs
    :type config: dict
    :param template: email templates
    :type template: str
    """

    windfile = Windfile(json.dumps(config) + '\n---\n' + template)
    submit(windfile)
