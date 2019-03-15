import pystache
from datetime import datetime

from windbell.core.mail import send_email
from windbell.core.windfile import Windfile


def cli_send(args):
    windfile = open(args.file, 'r').read()
    windfile = Windfile(windfile)

    config = windfile.config.value

    if 'attachement' in config:
        attachment = [open(v, 'r').read() for v in config['attachement']]
    else:
        attachment = []

    t = config['to']
    receiver_list = t if type(t) == list else [t]

    for receiver in receiver_list:
        content, cfg = windfile.render(
            data_injected={
                'meta': {
                    'to': receiver,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        )
        send_email(cfg['author'],
                   receiver,
                   cfg['subject'],
                   content,
                   attachment=attachment)

    return 0
