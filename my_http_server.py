#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vladislav'

import SocketServer
import SimpleHTTPServer
import urllib

PORT = 8000

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        # self.copyfile(urllib.urlopen(self.path), self.wfile)
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        self.wfile.write("hello !")

    def do_POST(self):
        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        self.wfile.write(
        """
        <?xml version="1.0" ?>
        <command_result>
        <param name="protocol_version" value="1"/>
        <param name="command_status" value="ok"/>
        <param name="player_state" value="dvd_playback"/>
        <param name="playback_speed" value="256"/>
        <param name="playback_duration" value="5183"/>
        <param name="playback_position" value="3000"/>
        <param name="playback_dvd_menu" value="0"/>
        <param name="playback_is_buffering" value="0"/>
        </command_result>
        """
        )


httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()
