from setuptools import setup, find_packages

VERSION = '0.0.1'


setup(
    name='redscope',
    version=VERSION,
    author='Sly Stalone',
    discription='A great cli tool!',
    include_package_data=True,
    packages=find_packages(exclude=('tests*', 'venv')),
    entry_points={'console_scripts': ['redscope = redscope.__main__:main']},
    python_requires='>=3'
)
