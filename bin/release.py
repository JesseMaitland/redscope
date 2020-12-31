#!venv/bin/python3

import subprocess
import re
import argparse
from pathlib import Path

project_root = Path(__file__).absolute().parent.parent / 'monkeywrench'
setup_path = project_root / "__init__.py"
number_pattern = r"[0-9]+\.[0-9]+\.[0-9]+"
version_pattern = fr"__version__ = {number_pattern}"


commands = {
    '--version': {
        'help': 'OPTIONAL :: use this to explicitly set the version',
        'dest': 'version',
    },
}


def get_arg_parser():
    parser = argparse.ArgumentParser()
    for command, options in commands.items():
        parser.add_argument(command, **options)
    return parser.parse_args()


def validate_version(version):
    version_value = re.search(number_pattern, version)
    if version_value.string != '0.0.0':
        print(f"version {version} received from environment and being validated")
        return True
    else:
        print(f"no version found in environment. incrementing minor version")
        return False


def run_process(*args):
    process = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=project_root)
    output, error = process.communicate()

    if process.returncode != 0:
        if error:
            print(error.decode("utf-8"))
            exit()
        else:
            return (b'no output', b'no error')
    else:
        return (output, error)


def print_output_error(output, error):
    if output or error:
        print(output.decode('utf-8'), error.decode('utf-8'))


def split_output(output):
    return [x for x in output.decode('utf-8').split("\n") if x]


def sort_versions(versions):

    values = versions.copy()
    values = [value.split('.') for value in values]

    for i in range(2, -1, -1):
        values.sort(key=lambda x: int(x[i]))

    return ['.'.join(x) for x in values]


def is_on_master_branch():
    args = ['git', 'branch']
    current_branch = None

    output, error = run_process(*args)
    output = split_output(output)

    for line in output:
        if '*' in line:
            current_branch = line.replace('*', '').strip()

    if current_branch != 'master':
        print(f"current branch is {current_branch}, however you must be on master to deploy!")
        return False

    return True


def get_last_tag():
    args = ['git', 'tag', '--list']
    output, error = run_process(*args)
    print_output_error(output, error)
    output = split_output(output)
    output = sort_versions(output)
    if output:
        last_tag = output[-1]
    else:
        last_tag = '0.0.1'

    return last_tag


def increment_sub_version(tag):
    tag_parts = tag.split('.')
    tag_parts[-1] = str(int(tag_parts[-1]) + 1)
    tag = '.'.join(tag_parts)
    return tag


def create_git_tag(tag):
    print(f"setting git tag {tag}")
    args = ['git', 'tag', tag]
    output, error = run_process(*args)
    print_output_error(output, error)


def set_version_in_setup(tag):
    new_version = f"__version__ = '{tag}'"
    setup_py = setup_path.read_text()
    new_setup_py = re.sub(version_pattern, new_version, setup_py)
    setup_path.write_text(new_setup_py)
    print(f"__init__.py updated to {new_version}")


def git_fetch():
    print(f"running git pull to update local master branch before release....")
    args = ['git', 'fetch', '--all']
    output, error = run_process(*args)
    print_output_error(output, error)


def git_reset():
    print(f"hard resetting git head. Local changes are overridden....")
    args = ['git', 'reset', '--hard', 'origin/master']
    print(f"the args are {args}")
    output, error = run_process(*args)
    print_output_error(output, error)


def push_git_tag():
    print(f"pushing tags....")
    args = ['git', 'push', '--tags']
    output, error = run_process(*args)
    print_output_error(output, error)


def git_commit_all(version):
    args = ['git', 'commit', '-am', f'"update to release version {version}']
    output, error = run_process(*args)
    print_output_error(output, error)


def git_push_master():
    args = ['git', 'push']
    output, error = run_process(*args)
    print_output_error(output, error)


def validate_git_tag(tag):
    last_tag = get_last_tag()
    if tag == get_last_tag():
        print(f"git tag {tag} created successfully.")
        return True
    else:
        print(f"error setting git tag. expected tag was {tag}, however current tag is {last_tag}")
        exit()


def main():
    args = get_arg_parser()

    if not is_on_master_branch():
        exit()

    if args.version and validate_version(args.version):
        version = args.version
    else:
        version = get_last_tag()
        version = increment_sub_version(version)

    if not version:
        raise ValueError("there is no version")

    git_fetch()
    git_reset()
    set_version_in_setup(version)
    git_commit_all(version)
    git_push_master()
    create_git_tag(version)
    push_git_tag()


if __name__ == '__main__':
    main()
