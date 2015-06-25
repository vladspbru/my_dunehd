#!/bin/bash

DUNE_IP=192.168.1.8
NETSRV_=192.168.1.7:/myworld
OUTDIR='/vols/tmpbuf/torrents/cinema/_download'
NET="nfs://$NETSRV_/cinema/_download"
OUTTMPL='[%(extractor)s-%(id)s][%(format)s]%(title)s.%(ext)s'


_OPT='--restrict-filenames -f bestvideo+bestaudio --write-description'
FN=$(youtube-dl $_OPT --print-json -o $OUTDIR/$OUTTMPL $1 | jq -r '._filename')
MEDIA=${FN/$OUTDIR/$NET}

echo "Starting play on Dune HD..."
echo "---------------------------"
echo "[$FN]"
echo "[$MEDIA]"
echo "---------------------------"
curl "http://$DUNE_IP/cgi-bin/do?cmd=start_file_playback&media_url=$MEDIA" | grep "command_status"


#URL=$(youtube-dl -g $1)
#curl "http://$DUNE_IP/cgi-bin/do?cmd=start_file_playback&media_url=$URL" 
#curl "http://$DUNE_IP/cgi-bin/do?cmd=status"
#curl "http://$DUNE_IP/cgi-bin/do?cmd=main_screen"
