import sys
import argparse

from windbell.cli.dev import cli_dev
from windbell.cli.send import cli_send
from windbell.cli.init import cli_init


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
p_config.set_defaults(func=cli_init)

# send command
p_send = subparsers.add_parser('send', help='send email')
p_send.add_argument('-f', '--file', default='windfile', type=str,
                    help='Windfile path (default: windfile)')
p_send.set_defaults(func=cli_send)

# dev command
p_send = subparsers.add_parser('dev', help='start dev server')
p_send.add_argument('-f', '--file', default='windfile', type=str,
                    help='windfile path')
p_send.add_argument('-p', '--port', default=9000, type=int,
                    help='dev service port')
p_send.set_defaults(func=cli_dev)
