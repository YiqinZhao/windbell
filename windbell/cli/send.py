from windbell.core.mail import submit
from windbell.core.windfile import Windfile


def cli_send(args):
    windfile = open(args.file, 'r').read()
    submit(windfile)
    return 0
