#! /usr/bin/env python3
import os
import sys
import datetime
import uuid
import argparse
import subprocess

def create_new_post(parent_dir):
    now = datetime.datetime.now()
    date_iso = now.date().isoformat()
    timezone_name = now.astimezone().tzname()
    new_uuid = uuid.uuid4()
    filename = '{}.rst'.format(new_uuid)
    filepath = os.path.join(parent_dir, filename)
    if os.path.exists(filepath):
        # This shouldn't happen,
        # but don't overwrite the file if it does.
        raise FileExistsError('{} already exists.'.format(filepath))
    with open(filepath, 'w') as f:
        f.write(":date: {}\n".format(date_iso))
        f.write(":timezone: {}\n".format(timezone_name))
        f.write(":uuid: {}\n".format(new_uuid))
    return filepath

def open_with_default_text_editor(filepath):
    if os.name == 'nt':
        os.startfile(filepath, 'open')
        sys.exit(0)
    elif os.name == 'posix':
        default_editor = os.getenv('EDITOR', default='vi')
        subprocess.call([default_editor, filepath])

def writable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError('not an existing directory: {}'.format(path))
    # TODO: create a tempfile to check if it is actually possible to write to this directory.
    if not os.access(path, os.W_OK):
        raise argparse.ArgumentTypeError('not a writable directory: {}'.format(path))
    # Normally we would return the converted value here,
    # but this is already a path, so there is no need.
    return path


def main():
    parser = argparse.ArgumentParser(description='Generates a new post.')
    parser.add_argument(
        'post_dir',
        nargs='?',
        type=writable_directory,
        default=os.getcwd(),
        help='Path to directory to store new post.',
    )
    args = parser.parse_args()
    post_filepath = create_new_post(args.post_dir)

    open_with_default_text_editor(post_filepath)

if __name__ == '__main__':
    main()
