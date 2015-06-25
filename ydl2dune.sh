#!/bin/bash

#DUNE=127.0.0.1:8000
DUNE=192.168.1.8

OUTTMPL='[%(extractor)s-%(id)s][%(format)s]%(title)s.%(ext)s'
OUTDIR='/vols/tmpbuf/torrents/cinema/_download'
NET='nfs://192.168.1.7:/myworld/cinema/_download'

_OPT='--restrict-filenames -f bestvideo+bestaudio --write-description'
FN=$(youtube-dl $_OPT --print-json -o $OUTDIR/$OUTTMPL $1 | jq -r '._filename')
MEDIA=${FN/$OUTDIR/$NET}


echo "Starting play on Dune HD..."
echo "---------------------------"
echo "[$FN]"
echo "[$MEDIA]"
echo "---------------------------"
#curl "http://$DUNE/cgi-bin/do?cmd=start_file_playback&media_url=$MEDIA" | grep "command_status"


#URL=$(youtube-dl -g $1)
#curl "http://$DUNE/cgi-bin/do?cmd=start_file_playback&media_url=$URL" 
#curl "http://$DUNE/cgi-bin/do?cmd=status"
#curl "http://$DUNE/cgi-bin/do?cmd=main_screen"
