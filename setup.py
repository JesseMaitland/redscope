import sys
import os
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '0.2.10'


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

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
    discription='A database migration and introspection tool for AWS Redshift',
    include_package_data=True,
    long_description=readme(),
    install_requires=[
        'rambo-py',
        'psycopg2-binary',
        'pandas',
        'python-dotenv'
    ],
    license='MIT',
    packages=find_packages(exclude=('tests*', 'venv', 'database*')),
    entry_points={
        'console_scripts': ['redscope = redscope.__main__:main']
    },
    download_url="https://github.com/JesseMaitland/redscope",
    long_description_content_type="text/markdown",
    python_requires='>=3',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
