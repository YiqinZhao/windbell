# windbell

![Pypi](https://img.shields.io/pypi/wheel/windbell.svg?style=flat)
![Travis](https://travis-ci.org/HawkinsZhao/windbell.svg?branch=master)

**windbell** is an email delivery tool which is easy to use via CLI and easy to integrate as a python package. **windbell** also features a flexible email development and testing environment.

![screenshot](https://github.com/HawkinsZhao/windbell/blob/dev/docs/images/windbell.png?raw=true)

**windbell is still under early development. Issues or pull requests are welcome!**

# Best Practice

**windbell** requires no system or user level configuration, and produce nothing after installation either. All you need is a **windfile**. So, you could just place it to where you need, then run `windbell send`.

If you want to send email in a CI pipeline of a git repo, you could just place your windfile in the root of your repo, then use a windbell docker to send the email. Windbell officially provide instructions for [Drone CI](https://drone.io).


# Usage

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


# License

**windbell** © [Hawkins Zhao](https://github.com/HawkinsZhao), Released under the MIT License.

Authored and maintained by Hawkins Zhao with help from contributors.
