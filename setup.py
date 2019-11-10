from os import linesep
from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as file:
        return [line.rstrip(linesep) for line in file.readlines()]


def get_long_description():
    with open('README.md') as file:
        return file.read()


setup(
    name='redscope',
    version='0.1.0',
    author='Jesse Maitland',
    discription='A database migration and introspection tool for AWS Redshift',
    include_package_data=True,
    long_description=get_long_description(),
    install_requires=[
        'rambo-py',
        'psycopg2-binary',
        'pandas',
        'python-dotenv'
    ],
    license='MIT',
    packages=find_packages(exclude=('tests*', 'venv', 'database*')),
    scripts=["bin/redscope"],
    download_url="",
    long_description_content_type="text/markdown"
)
