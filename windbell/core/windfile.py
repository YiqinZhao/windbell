import os

import json
import yaml
import pystache

from windbell.core.exceptions import *


class WindfileConfig():
    def __init__(self, content):
        super(WindfileConfig)
        self.value = yaml.load(content)

    def check_schema(self):
        return True

    def calc_env_deps(self):
        def _fetch(config):
            envs = []
            for key in config.keys():
                if type(config[key]) == dict:
                    if 'from_env' in config[key].keys():
                        envs += [config[key]['from_env']]
                    else:
                        envs += _fetch(config[key])

            return envs

        return _fetch(self.value)

    def dump(self):
        return yaml.dump(self.value, default_flow_style=False)


class WindfileTemplate():
    def __init__(self, content):
        self.value = content

    def dump(self):
        return self.value


class Windfile():
    def __init__(self, content):
        super(Windfile)

        if not '---' in content:
            raise WindfileDamangedError()

        windfile = content.split('\n')
        split_idx = windfile.index('---')

        config = windfile[0:split_idx]
        config = '\n'.join(config)
        self._config = WindfileConfig(config)

        template = windfile[split_idx + 1:]
        template = '\n'.join(template).strip()
        self._template = WindfileTemplate(template)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config.value = yaml.load(value)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template.value = value

    def render(self, data_injected={}, env_injected={}):
        def _render_config(config):
            envs = {
                **dict(os.environ),
                **env_injected
            }

            def if_dict(element):
                if 'from_env' in element:
                    return envs[element['from_env']]
                else:
                    return _render_config(element)

            type_map = {
                dict: if_dict,
                str: lambda x: x,
                list: lambda x: x
            }

            return {
                key: type_map[type(config[key])](config[key])
                for key in config.keys()
            }

        config = _render_config(self.config.value)
        data = json.loads(json.dumps(config['data']))
        data = {**data, **data_injected}
        dist = pystache.render(self.template.value, data)

        return dist, config

    def dist(self):
        config = self.config.dump()
        template = self.template.dump()
        return config + '\n---\n' + template

    def json(self):
        return json.dumps({
            'envs': self.config.calc_env_deps(),
            'config': self.config.dump(),
            'template': self.template.dump()
        })
