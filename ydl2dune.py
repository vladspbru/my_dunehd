#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl
import time
import os
import sys
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


def ctrl_c(signum, frame):
    """Catch Ctrl-C key sequence and set a shutdown_event for our threaded
    operations
    """
    global shutdown_event
    raise SystemExit('\nCancelling...')

# Some global variables we use
dune_ip = '192.168.1.8'
media_pc_netshared_dir = '/vols/tmpbuf/torrents/cinema/_download'
outtmpl = '%(title)s.%(ext)s'
netshared_dir_for_dune = 'nfs://192.168.1.7:/myworld/cinema/_download'
url = 'http://www.youtube.com/watch?v=BaW_jenozKc'

filename = None


def ydl_hook(d):
    global filename
    filename = None
    if d['status'] == 'finished':
        filename = d['filename']


def ydl2dune():
    pass
    global dune_ip, media_pc_netshared_dir, outtmpl, netshared_dir_for_dune, url, filename
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

    if not args.url:
        print('Empty URL string.')
        sys.exit(1)

    # If specified bind to a specific IP address
    if args.dune:
        dune_ip = args.dune

    ydl_opts = {
        # 'simulate': True,
        'outtmpl': "%s/%s" % (media_pc_netshared_dir, outtmpl),
        'restrictfilenames': True,
        # 'forcefilename': True,
        'progress_hooks': [ydl_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        res = ydl.download([url])

    if int(res) != 0:
        print('Could not download')
        sys.exit(1)

    media = filename.replace(media_pc_netshared_dir, netshared_dir_for_dune)
    print("Sending [%s] to DuneHD" % (media))

    apiData = ['cmd=%s' % 'status', ]
    req = Request('http://%s/cgi-bin/do?' % (dune_ip), data='&'.join(apiData).encode())
    f = urlopen(req)
    print(f.read().decode())
    f.close()

    apiData = [
        'cmd=%s' % 'launch_media_url',
        'media_url=%s' % media,
    ]
    req = Request('http://%s/cgi-bin/do?' % (dune_ip), data='&'.join(apiData).encode())
    f = urlopen(req)
    response = f.read()
    code = f.code
    f.close()

    if int(code) != 200:
        print('Could not submit results to DuneHD')
        sys.exit(1)

    print(response.decode())


def main():
    try:
        ydl2dune()
    except KeyboardInterrupt:
        print('\nCancelling...')


if __name__ == '__main__':
    main()
