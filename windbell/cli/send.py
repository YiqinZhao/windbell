from windbell.core.mail import submit
from windbell.core.windfile import Windfile


def cli_send(args):
    submit(Windfile(open(args.file, 'r').read()))
    return 0
