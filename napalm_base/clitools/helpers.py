# -*- coding: utf-8 -*-
'''
NAPALM CLI Tools: helpers
=========================

Defines helpers for the CLI tools.
'''
from __future__ import absolute_import

# stdlib
import sys
import logging
import getpass
import argparse


def build_help(connect_test=False):
    parser = argparse.ArgumentParser(
        description='Command line tool to handle configuration on devices using NAPALM.'
                    'The script will print the diff on the screen',
        epilog='Automate all the things!!!'
    )
    parser.add_argument(
        dest='hostname',
        action='store',
        help='Host where you want to deploy the configuration.'
    )
    parser.add_argument(
        '--user', '-u',
        dest='user',
        action='store',
        default=getpass.getuser(),
        help='User for authenticating to the host. Default: user running the script.'
    )
    parser.add_argument(
        '--password', '-p',
        dest='password',
        action='store',
        help='Password for authenticating to the host.'
             'If you do not provide a password in the CLI you will be prompted.',
    )
    parser.add_argument(
        '--vendor', '-v',
        dest='vendor',
        action='store',
        required=True,
        help='Host Operating System.'
    )
    parser.add_argument(
        '--optional_args', '-o',
        dest='optional_args',
        action='store',
        help='String with comma separated key=value pairs passed via optional_args to the driver.',
    )
    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        help='Enables debug mode; more verbosity.'
    )
    if not connect_test:
        parser.add_argument(
            '--strategy', '-s',
            dest='strategy',
            action='store',
            choices=['replace', 'merge'],
            default='replace',
            help='Strategy to use to deploy configuration. Default: replace.'
        )
        parser.add_argument(
            dest='config_file',
            action='store',
            help='File containing the configuration you want to deploy.'
        )
        parser.add_argument(
            '--dry-run', '-d',
            dest='dry_run',
            action='store_true',
            default=None,
            help='Only returns diff, it does not deploy the configuration.',
        )
    args = parser.parse_args()

    if args.password is None:
        password = getpass.getpass('Enter password: ')
        setattr(args, 'password', password)

    return args


def configure_logging(logger, debug):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def parse_optional_args(optional_args):

    if optional_args is not None:
        return {x.split('=')[0]: x.split('=')[1] for x in optional_args.replace(' ', '').split(',')}
    return {}
