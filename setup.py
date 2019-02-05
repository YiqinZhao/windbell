from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='windbell',
    version='0.0.1',
    description='Fastest way to deliver your notification email.',
    long_description=readme,
    author='Hawkins Zhao',
    author_email='hawkinszhao@outlook.com',
    url='https://github.com/HawkinsZhao/windbell',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': ['windbell=windbell:cli_main']
    }
)
