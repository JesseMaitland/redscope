import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '0.4.2'


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(tag, VERSION)
            sys.exit(info)


setup(
    name='redscope',
    version=VERSION,
    author='Jesse Maitland',
    discription='A cli tool for introspecting AWS redshift schema ddl',
    include_package_data=True,
    packages=find_packages(exclude=('tests*', 'venv')),
    entry_points={'console_scripts': ['redscope = redscope.__main__:main']},
    python_requires='>=3'
)
