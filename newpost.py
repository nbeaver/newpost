#! /usr/bin/env python
import os
import sys
import datetime
import uuid
import argparse
import subprocess
import subprocess

if __name__ == '__main__':
    now = datetime.datetime.now()
    date_iso = now.date().isoformat()

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Generates a new post.')
        parser.add_argument('post_dir', default=os.getcwd(), help='Path to post directory.')
        args = parser.parse_args()
        post_dir = args.post_dir
    else:
        post_dir = os.getcwd()

    if not os.path.isdir(post_dir):
        sys.stderr.write("Error: not a directory: {}\n".format(post_dir))
        sys.exit(1)

    new_uuid = uuid.uuid4()
    filename = '{}.rst'.format(new_uuid)
    filepath = os.path.join(post_dir, filename)
    with open(filepath, 'w') as f:
        f.write(":date: {}\n".format(date_iso))
        f.write(":slug: {}\n".format(new_uuid))

    if os.name == 'nt':
        os.startfile(filepath, 'open')
        sys.exit(0)
    elif os.name == 'posix':
        default_editor = os.getenv('EDITOR', default='vi')
        subprocess.call([default_editor, filepath])
