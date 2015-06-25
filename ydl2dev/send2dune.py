#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vladislav'
__version__ = '0.1'


class HomeConfiguration(object):
    DUNE_IP = '192.168.1.8'


import time
import os
import sys
import threading
import signal

# Begin import game to handle Python 2 and Python 3
try:
    from argparse import ArgumentParser as ArgParser
except ImportError:
    from optparse import OptionParser as ArgParser

try:
    from urllib2 import urlopen, Request, HTTPError, URLError
except ImportError:
    from urllib.request import urlopen, Request, HTTPError, URLError


# Some global variables we use
shutdown_event = None
def ctrl_c(signum, frame):
    """Catch Ctrl-C key sequence and set a shutdown_event for our threaded
    operations
    """
    global shutdown_event
    shutdown_event.set()
    raise SystemExit('\nCancelling...')

def version():
    """Print the version"""
    raise SystemExit(__version__)


def send2dune():
    global shutdown_event, dune_ip
    shutdown_event = threading.Event()
    signal.signal(signal.SIGINT, ctrl_c)


    description = (
        'Command line interface for Dune IP control.\n'
        '-------------------------------------------\n'
    )

    parser = ArgParser(description=description)
    # Give optparse.OptionParser an `add_argument` method for compatibility with argparse.ArgumentParser
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass

    parser.add_argument('--url', help='Media URL to play')
    parser.add_argument('--dune', help='DuneHD IP address to bind to')
    parser.add_argument('--version', action='store_true', help='Show the version number and exit')

    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options

    # Print the version and exit
    if args.version:
        version()

    # If specified bind to a specific IP address
    if args.dune:
        dune_ip = args.dune






    apiData = [
        'cmd=%s' % 'launch_media_url',
        'media_url=%s' % 2,
        'speed=%s' % 0,
        'position=%s' % 0,
        'hide_osd=%s' % 1,
        'black_screen=%s' % 0,
        'action_on_finish=%s' % 'restart_playback'
    ]


    req = Request('http://%s/cgi-bin/do?' % (dune_ip), data='&'.join(apiData).encode())
    f = urlopen(req)
    response = f.read()
    code = f.code
    f.close()

    if int(code) != 200:
        print('Could not submit results to DuneHD')
        sys.exit(1)

    print (response.decode())
    # qsargs = parse_qs(response.decode())
    # resultid = qsargs.get('resultid')
    # if not resultid or len(resultid) != 1:
    #     print_('Could not submit results to DuneHD')
    #     sys.exit(1)


def main():
    try:
        send2dune()
    except KeyboardInterrupt:
        print('\nCancelling...')


if __name__ == '__main__':
    main()
