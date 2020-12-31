from redscope.cli import parse_args


def main():
    cmd = parse_args()

    if type(cmd.func) == list:
        for f in cmd.func:
            f(cmd)
    else:
        cmd.func(cmd)


if __name__ == '__main__':
    main()
