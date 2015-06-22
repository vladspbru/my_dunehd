#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl


media_pc_netshared_dir='/vols/tmpbuf/torrents/cinema/_download'
outtmpl='%(title)s.%(ext)s'


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'outtmpl': outtmpl,
    'format': 'bestaudio/best',
    'simulate': 1,
    'restrictfilenames': 1,
    'forcefilename': 1,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])