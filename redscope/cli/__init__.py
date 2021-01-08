from argparse import ArgumentParser

from .init import init
from .inspect import inspect


def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    init_parser = sub_parsers.add_parser('init')
    init_parser.set_defaults(func=init)

    init_parser = sub_parsers.add_parser('inspect')
    init_parser.add_argument('-o', choices=['schemas', 'tables', 'functions',
                                            'procedures', 'views', 'all'], default='all')
    init_parser.set_defaults(func=inspect)

    return parser.parse_args()
