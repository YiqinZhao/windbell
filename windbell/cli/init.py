import os
from windbell.utils import sample_windfile


def cli_init(args):
    with open('windfile', 'w+') as f:
        f.write(sample_windfile)

    print('Inited windfile at %s/%s' % (os.getcwd(),
                                        'windfile'))

    return 0
