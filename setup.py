import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '0.4.2'


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CI_COMMIT_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(tag, VERSION)
            sys.exit(info)


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='redscope',
    version=VERSION,
    author='Jesse Maitland',
    discription='A cli tool for introspecting AWS redshift schema ddl',
    long_description=readme(),
    install_requires=[
        'psycopg2-binary',
        'python-dotenv',
        'pyyaml',
        'sqlparse'
    ],
    include_package_data=True,
    packages=find_packages(exclude=('tests*', 'venv')),
    entry_points={'console_scripts': ['redscope = redscope.__main__:main']},
    python_requires='>=3',
    long_description_content_type="text/markdown",
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
