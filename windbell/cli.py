import sys
import json
import argparse
import pystache

import yaml
from windbell.mail import send_email

from windbell.utils import sample_windfile, sample_template, extract_config_item


def _cli_init(args):
    with open('windfile.yml', 'w+') as f:
        f.write(sample_windfile)

    with open('template.mst', 'w+') as f:
        f.write(sample_template)

    print('Initialzation Finished')
    print('windfile.yml - project config file')
    print('template.mst - email template')

    return 0


def _cli_send(args):
    config = open(args.config, 'r').read()
    config = yaml.load(config)

    template = open(config['template'], 'r').read()
    data = extract_config_item(config['data'])
    content = pystache.render(template, data)

    if 'attachement' in config:
        attachment = [open(v, 'r').read() for v in config['attachement']]
    else:
        attachment = ()

    send_email(extract_config_item(config['author']),
               config['to'],
               config['subject'],
               content,
               attachment=attachment)

    return 0


def _cli_main():
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    else:
        return args.func(args)


# Parser
parser = argparse.ArgumentParser(prog='windbell')
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='sub-command help')

# init command
p_config = subparsers.add_parser('init', help='init current dictionary')
p_config.set_defaults(func=_cli_init)

# send command
p_send = subparsers.add_parser('send', help='send email')
p_send.add_argument('-c', '--config', default='windfile.yml', type=str,
                    help='Windbell config file (default: windfile.yml)')
p_send.set_defaults(func=_cli_send)
