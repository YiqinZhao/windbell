import os
import sys

import json

import shutil
from pathlib import Path

home = str(Path.home())


def reset_conf():
    if os.path.exists('%s/.windbell' % home):
        shutil.rmtree('%s/.windbell' % home)

    _read_conf()

    print('Reset finished.')


def write_conf(value):
    f = open('%s/.windbell/config.json' % home, 'w')
    f.write(json.dumps(value))
    f.close()


def _read_conf():
    env_des = {
        'smtp_server': 'SMTP Server [server:port]: ',
        'sender_email': 'Sender email [sender@example.com]: ',
        'sender_pwd': 'Sender password: ',
        'sender_name': 'Sender name: '
    }

    # User config folder existence check
    conf_dir = os.path.exists('%s/.windbell' % home)
    if not conf_dir:
        os.mkdir('%s/.windbell' % home)

    # User config folder type check
    conf_dir = os.path.isdir('%s/.windbell' % home)
    if not conf_dir:
        raise Exception('Config file initialization error.')

    # User config file existence check
    conf_file = os.path.exists('%s/.windbell/config.json' % home)
    if not conf_file:
        print('Initializing windbell, please input following configs.\n')
        conf = {
            'default_receiver': input('Default receiver [receiver@example.com]: ')
        }

        # Fetch global configs
        for e in env_des.keys():
            key = 'WB_' + e.upper()
            env = os.environ[key] if key in os.environ else None
            if env is None:
                conf[e] = input(env_des[e])

        f = open('%s/.windbell/config.json' % home, 'w')
        f.write(json.dumps(conf))
        f.close()

        print()

    # Read config file
    conf = json.loads(open('%s/.windbell/config.json' % home, 'r').read())
    conf = {item: {
        'value': conf[item],
        'inherited': False
    } for item in conf}

    # Fetch global configs
    for e in env_des.keys():
        if not e in conf:
            key = 'WB_' + e.upper()
            env = os.environ[key] if key in os.environ else None
            conf[e] = {'value': env, 'inherited': True}

            if env is None:
                sys.stderr.write('Key config %s missing.' % e)
                print('\n')
                exit(-1)

    return conf


config = _read_conf()
