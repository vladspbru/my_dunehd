#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl, sys


class AudioConfiguration(object):
    OUT_DIR = '/vols/tmpbuf/torrents/cinema/_download'
    OUT_TEMPL = '%(title)s.%(ext)s'


class TestConfiguration(object):
    OUT_DIR = '~'
    OUT_TEMPL = '[%(extractor)s][%(format)s]%(title)s.%(ext)s'


conf = TestConfiguration()



audio_opts = {
    'outtmpl': '%s/%s' % (conf.OUT_DIR,conf.OUT_TEMPL),
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}





class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now run postprocessors ...')


def main( url ):
    ex_opts = {
        'simulate': True,
        'restrictfilenames': True,
        'forcefilename': True,
        # 'forceurl': True,
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    opts = audio_opts.join(ex_opts)
    print opts
    # with youtube_dl.YoutubeDL( opts ) as ydl:
    #     ydl.download([url])


if __name__ == '__main__':
    if len(sys.argv)==2:
        main( sys.argv[1] )
    else:
        print "Bad url"
        main( 'http://www.youtube.com/watch?v=BaW_jenozKc' )
