import json

import tornado.ioloop
import tornado.web

import yaml
import pystache
from datetime import datetime

from windbell.utils import pkg_dir
from windbell.utils import extract_config_item


class WindfileHandler(tornado.web.RequestHandler):
    def initialize(self, windfile=None, **kwargs):
        self.windfile = windfile
        super().initialize(**kwargs)

    def get(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(self.windfile))

    def post(self):
        config = self.get_argument('config')
        config = yaml.load(config)

        data = extract_config_item(config['data'])
        data['meta'] = {
            'to': config['to'][0],
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        template = self.get_argument('template')
        content = pystache.render(template, data)

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps({'content': content}))


def cli_dev(args):
    f = open(args.file, 'r').read()
    f = f.split('---')

    windfile = {
        'config': f[0],
        'template': ''.join(f[1:]).strip()
    }

    dev_folder = pkg_dir + '/../etc/dev/'
    app = tornado.web.Application([
        (r'/windfile', WindfileHandler, {'windfile': windfile}),
        (r'/(.*)', tornado.web.StaticFileHandler,
         {'path': dev_folder, 'default_filename': 'index.html'}),
    ], debug=True)
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()
