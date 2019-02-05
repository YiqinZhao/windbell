import os
import sys

import argparse
import configparser

from pathlib import Path

config = None
home = str(Path.home())


def cli_main():
    init_check()
    args = parser.parse_args()
    return args.func(args)


def cli_send(args):
    print(args)
    print('send')

    print(config)


def cli_config(args):
    """CLI config entry

    Parameters
    ----------
    args : Namespace
        func: handler function,
        key: config key
        value: config value
    """
    if args.list:
        config.write(sys.stdout)
    else:
        if not args.key or not args.value:
            sys.stderr.write('You must give key and value.')

        config['basic'][args.key] = args.value
        with open('%s/.windbell/windbell.conf' % home, 'w') as configfile:
            config.write(configfile)


# Parser
parser = argparse.ArgumentParser(prog='windbell')
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='sub-command help')

# windbell [send] command
p_send = subparsers.add_parser('send', help='send email')
p_send.add_argument('-t', '--template', default=None, type=str,
                    help='Mustache syntax template file.')
p_send.add_argument('-d', '--data', default=None, type=str,
                    help='JSON data')
p_send.add_argument('-c', '--config', default=None, type=str,
                    help='optional, if you use other config than default')
p_send.set_defaults(func=cli_send)

# windbell [config] command
p_config = subparsers.add_parser('config', help='change config')
p_config.add_argument('-l', '--list', default=False, action='store_true',
                      help='Show all configs')
p_config.add_argument('-k', '--key', default=None, type=str,
                      help='Config key')
p_config.add_argument('-v', '--value', default=None, type=str,
                      help='Value of key')
p_config.set_defaults(func=cli_config)


def init_check():
    global config

    conf_dir = os.path.exists('%s/.windbell' % home)
    if not conf_dir:
        os.mkdir('%s/.windbell' % home)

    conf_dir = os.path.isdir('%s/.windbell' % home)
    if not conf_dir:
        raise Exception('Config file initialization error.')

    conf = configparser.ConfigParser()
    conf_file = os.path.exists('%s/.windbell/windbell.conf' % home)
    if not conf_file:
        print('Initializing Windbell, please input following configs.')

        smtp_server = input('SMTP server [server:port] ')
        sender_email = input('Sender email [xxx@x.x] ')
        sender_pwd = input('Sender password ')
        sender_name = input('Sender name ')
        default_receiver = input('Default receiver [yyy@y.y] ')

        conf['basic'] = {
            'smtp_server': smtp_server,
            'sender_email': sender_email,
            'sender_pwd': sender_pwd,
            'sender_name': sender_name,
            'default_receiver': default_receiver
        }

        with open('%s/.windbell/windbell.conf' % home, 'w') as configfile:
            conf.write(configfile)

    else:
        conf.read('%s/.windbell/windbell.conf' % home)

    config = conf
