#! /usr/bin/env python3
import os
import sys
import datetime
import uuid
import argparse
import subprocess
import logging
logger = logging.getLogger(__name__)

def create_new_post(parent_dir):
    now = datetime.datetime.now()
    date_iso = now.date().isoformat()
    timezone_name = now.astimezone().tzname()
    new_uuid = uuid.uuid4()
    filename = '{}.rst'.format(new_uuid)
    filepath = os.path.join(parent_dir, filename)
    logging.info("filepath = '{}'".format(filepath))
    if os.path.exists(filepath):
        # This shouldn't happen,
        # but don't overwrite the file if it does.
        raise FileExistsError('{} already exists.'.format(filepath))
    with open(filepath, 'w', newline='\n') as f:
        f.write(":date: {}\n".format(date_iso))
        f.write(":timezone: {}\n".format(timezone_name))
        f.write(":uuid: {}\n".format(new_uuid))
    return filepath

def open_with_text_editor(filepath, text_editor=None, editor_args=None):
    if text_editor is None:
        logging.debug("text_editor not specified, using OS default")
        open_with_default_text_editor(filepath)
    elif editor_args is None:
        logging.info("text_editor = '{}'".format(text_editor))
        logging.info("text_editor = '{}'".format(text_editor))
        call_args = [text_editor, filepath]
        logging.info("call_args = '{}'".format(call_args))
        subprocess.call(call_args)
    else:
        logging.info("text_editor = '{}'".format(text_editor))
        logging.info("editor_args = '{}'".format(editor_args))
        call_args = [text_editor] + editor_args + [filepath]
        logging.info("call_args = '{}'".format(call_args))
        subprocess.call(call_args)

def open_with_default_text_editor(filepath):
    logging.debug("os.name = '{}'".format(os.name))
    if os.name == 'nt':
        try:
            os.startfile(filepath, 'open')
        except OSError as e:
            logging.warning("e.errno = {}".format(e.errno))
            if e.errno == 22:
                # Handle WinError 1155:
                # "No application is associated with the specified file
                # for this operation"
                logging.info("os.startfile failed, using notepad instead")
                subprocess.call(['notepad', filepath])
            else:
                raise
    elif os.name == 'posix':
        default_editor = os.getenv('EDITOR', default='vi')
        logging.info("default_editor = '{}'".format(default_editor))
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
    parser.add_argument(
        '-e',
        '--editor',
        help='Editor to use',
        default=None,
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='More verbose logging',
        dest="loglevel",
        default=logging.WARNING,
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Enable debugging logs',
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    logger.setLevel(args.loglevel)

    logging.info("args.post_dir = '{}'".format(args.post_dir))

    post_filepath = create_new_post(args.post_dir)

    open_with_text_editor(post_filepath, text_editor=args.editor)

if __name__ == '__main__':
    main()
