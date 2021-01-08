from setuptools import setup, find_packages

VERSION = '0.3.10'


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
