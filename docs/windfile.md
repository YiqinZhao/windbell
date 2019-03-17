# Windfile in Depth

A `windfile` is composed by two parts: **config** and **template**.

## Config

Let's look at the default sample:

```yaml
author:
  smtp_server: server:port
  name: YOUR_NAME
  address: your-address@example.com
  password:
    from_env: WB_PASSWORD
data:
  info: Bold text from the windbell!
subject: sample_project
to:
  - hawkinszhao@outlook.com
```

## Template

windbell render email from mustache style template.
