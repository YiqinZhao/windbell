# windbell

windbell is a email Python delivery tool that easy to use and easy to integrate. Your can use windbell to render a mustache template with your JSON data, then send via command line or Python code.

# Usage

```bash
pip install windbell

# Just run with no args for first time initialization, you will need to setup some email configs.
windbell
```

## Send email

CLI:

```bash
windbell send -t base.mst -d '{"foo": "bar"}' -s 'some_subject'
```

Python:

```python
import windbell as wb

t = open('base.mst', 'r').read()
d = {'foo': 'bar'}

wb.send('windbell lib test', t, d)
```

## Manage configs

```bash
windbell config -k foo -v value
```

