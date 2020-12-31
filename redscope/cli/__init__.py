from argparse import ArgumentParser

from .init import init


def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    init_parser = sub_parsers.add_parser('init')
    init_parser.set_defaults(func=init)

    return parser.parse_args()
