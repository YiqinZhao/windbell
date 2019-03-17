# CLI

## Installation

```bash
pip install windbell
```

## Start Your Project

```bash
windbell init
```

`init` command will create a `windfile` in current working dictronary. A `windfile` is the key to your email delivery workflow, it contains email template and configurations.

```bash
windbell dev
```

`dev` command allows you develop your email project in the browser under a flexible intergrated environment. More detailed structure about `windfile` please refer to doc.

```bash
windbell send
```

`send` command will read the `windfile` at current dictionary and send to the receviers defined in `windfile`.

# Python Library

## Installation
```bash
pip install windbell
```

## Integrate in Your Code

```Python
from windbell import send

config = {
    'author': {
        'smtp_server': 'server:port',
        'name': 'YOUR NAME',
        'address': 'your-address@example.com',
        'password': 'YOUR PASSWORD'
    },
    to: ['somewhere@example.com'],
    data: {
        # Your Data
    }
}

template = open('some_template.html', 'r').read()

send(config, template)
```
