import yaml
import pystache
from datetime import datetime

from windbell.mail import send_email
from windbell.utils import extract_config_item


def cli_send(args):
    config = open(args.config, 'r').read()
    config = yaml.load(config)

    template = open(config['template'], 'r').read()

    if 'attachement' in config:
        attachment = [open(v, 'r').read() for v in config['attachement']]
    else:
        attachment = ()

    t = config['to']
    receiver_list = t if type(t) == list else [t]

    for receiver in receiver_list:
        data = extract_config_item(config['data'])
        data['meta'] = {
            'to': receiver,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        content = pystache.render(template, data)
        send_email(extract_config_item(config['author']),
                   receiver,
                   config['subject'],
                   content,
                   attachment=attachment)

    return 0
