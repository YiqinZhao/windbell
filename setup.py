from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='windbell',
    version='0.1.1',
    description='Fast email delivery in the wind.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Hawkins Zhao',
    author_email='hawkinszhao@outlook.com',
    url='https://github.com/HawkinsZhao/windbell',
    license=license,
    packages=find_packages(exclude=('tests')),
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': ['windbell=windbell.cli:_cli_main']
    },
    include_package_data=True
)
