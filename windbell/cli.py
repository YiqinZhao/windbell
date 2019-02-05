import sys
import json
import argparse
import pystache

from windbell.mail import send_email
from windbell.utils import home, config, reset_conf, write_conf


def _cli_main():
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    else:
        return args.func(args)


def _cli_send(args):
    """CLI send entry

    Parameters
    ----------
    args : Namespace
        data: json data
        template: template path
        subject: subject
        attachment: optional attachment
    """

    subject = args.subject

    data = json.loads(args.data)
    template = open(args.template, 'r').read()
    content = pystache.render(template, data)

    attachment = ()
    if args.attachment:
        attachment = (open(attachment, 'r').read())

    receiver = args.receiver if args.receiver else None
    conf = {v: config[v]['value'] for v in config}

    send_email(subject, content, attachment=attachment,
               receiver=receiver, config=conf)

    return 0


def _cli_config(args):
    """CLI config entry

    Parameters
    ----------
    args : Namespace
        func: handler function,
        key: config key
        value: config value
        reset: reset all configs
    """
    if args.list:
        for item in config.keys():
            t = item + '=' + config[item]['value'] + ' '
            t = t + ('(Inherited)' if config[item]['inherited'] else '')
            print(t)
    elif args.reset:
        reset_conf()
    else:
        if not args.key or not args.value:
            sys.stderr.write('You must give key and value.')

        conf = {v: config[v]['value'] for v in config}
        conf[args.key] = args.value
        write_conf(conf)

    return 0


# Parser
parser = argparse.ArgumentParser(prog='windbell')
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='sub-command help')

# windbell [send] command
p_send = subparsers.add_parser('send', help='send email')
p_send.add_argument('-s', '--subject', default=None, type=str,
                    help='email subject')
p_send.add_argument('-t', '--template', default=None, type=str,
                    help='Mustache syntax template file.')
p_send.add_argument('-d', '--data', default=None, type=str,
                    help='JSON data')
p_send.add_argument('-a', '--attachment', default=None, type=str,
                    help='optional attachment')
p_send.add_argument('-r', '--receiver', default=None, type=str,
                    help='optional receiver override default')
p_send.set_defaults(func=_cli_send)

# windbell [config] command
p_config = subparsers.add_parser('config', help='change config')
p_config.add_argument('-l', '--list', default=False, action='store_true',
                      help='Show all configs')
p_config.add_argument('-r', '--reset', default=False, action='store_true',
                      help='Reset all configs')
p_config.add_argument('-k', '--key', default=None, type=str,
                      help='Config key')
p_config.add_argument('-v', '--value', default=None, type=str,
                      help='Value of key')
p_config.set_defaults(func=_cli_config)
