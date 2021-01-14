import os
from setuptools import setup, find_packages


def version() -> str:
    version = os.getenv('CI_COMMIT_TAG')

    if not version:
        raise ValueError("version tag expected but not found in environment")

    return version


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='redscope',
    version=version(),
    author='Jesse Maitland',
    discription='A cli tool for introspecting AWS redshift schema ddl',
    long_description=readme(),
    install_requires=[
        'psycopg2-binary',
        'python-dotenv',
        'sqlparse'
    ],
    include_package_data=True,
    packages=find_packages(exclude=('tests*', 'venv')),
    entry_points={'console_scripts': ['redscope = redscope.__main__:main']},
    python_requires='>=3',
    long_description_content_type="text/markdown"
)
