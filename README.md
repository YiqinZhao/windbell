# windbell

**windbell** is a Python email delivery tool which is easy to use and easy to integrate. Your can use windbell via both CLI and Python code.

![Pypi](https://img.shields.io/pypi/wheel/windbell.svg?style=flat)

# Usage

## Installation
```bash
pip install windbell

# Run with no args for the first time initialization.
windbell
```

## Send email

### CLI:

```bash
windbell send -t /path/to/template.mst -d '{"foo": "bar"}' -s 'some_subject'
```

Arguments
- -t, --template Mustache syntax template file path
- -d, --data JSON data for rendering
- -s, --subject Email subject

### Python:

```python
import windbell as wb

t = open('base.mst', 'r').read()
d = {'foo': 'bar'}

wb.send('windbell lib test', t, d)
```

### Parameters
- `subject` email subject
- `template` mustache syntax template
- `data` dict data for rendering
- `attachment` *[optional]* attachment content tuple, default is `()`
- `receiver` *[optional]* email receiver, default is `None`
- `smtp_server` *[optional]* SMTP server, default is None
- `sender_email` *[optional]* sender email, default is None
- `sender_pwd` *[optional]* sender password, default is None
- `sender_name` *[optional]* sender name, default is None

optional parameters will fetch its value from config file when it is set to `None`

## Change configs

*Config change only support in CLI. To change config in Python, you could pass config dict in send function.*

```bash
windbell config -k foo -v value
```

### Arguments
- -l, --list list all configs
- -k, --key config item key
- -v, --value config item value
