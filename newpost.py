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

def writable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError('not an existing directory: {}'.format(path))
    if not os.access(path, os.W_OK):
        raise argparse.ArgumentTypeError('not a writable directory: {}'.format(path))
    return path

if __name__ == '__main__':

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Generates a new post.')
        parser.add_argument('post_dir', type=writable_directory, help='Path to directory to store new post.')
        args = parser.parse_args()
        post_dir = args.post_dir
    else:
        post_dir = os.getcwd()

    post_filepath = create_new_post(post_dir)

    open_with_default_text_editor(post_filepath)
