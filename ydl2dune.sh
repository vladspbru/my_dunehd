#!/usr/bin/sh

URL=$(youtube-dl -g $1)
DUNE=127.0.0.1:8000

curl "http://$DUNE/cgi-bin/do?cmd=start_file_playback&media_url=$URL"


