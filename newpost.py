#! /usr/bin/env python
import os
import sys
import datetime
import uuid
import argparse
import subprocess
import subprocess

def create_new_post(parent_dir):
    now = datetime.datetime.now()
    date_iso = now.date().isoformat()
    new_uuid = uuid.uuid4()
    filename = '{}.rst'.format(new_uuid)
    filepath = os.path.join(parent_dir, filename)
    with open(filepath, 'w') as f:
        f.write(":date: {}\n".format(date_iso))
        f.write(":slug: {}\n".format(new_uuid))
    return filepath

def open_with_default_text_editor(filepath):
    if os.name == 'nt':
        os.startfile(filepath, 'open')
        sys.exit(0)
    elif os.name == 'posix':
        default_editor = os.getenv('EDITOR', default='vi')
        subprocess.call([default_editor, filepath])

class ExistingDirectory(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs > 1:
            raise ValueError("Pass only one directory.")
        super(ExistingDirectory, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, value, option_string=None):
        if not os.path.isdir(value):
            raise ValueError('Not an existing directory: {}'.format(value))
        setattr(namespace, self.dest, value)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Generates a new post.')
        parser.add_argument('post_dir', action=ExistingDirectory, help='Path to post directory.')
        args = parser.parse_args()
        post_dir = args.post_dir
    else:
        post_dir = os.getcwd()

    post_filepath = create_new_post(post_dir)

    open_with_default_text_editor(post_filepath)
