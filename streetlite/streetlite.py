#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from threading import Thread

from streetlite.panel.panel_layout import PanelLayout
from streetlite.map.map_layout import MapLayout
from streetlite.websocket.ws_server import WsServer

class StreetLite(BoxLayout):
    def __init__(self):
        super(StreetLite, self).__init__()

        self.orientation = 'vertical'
        self.clients = []
        self.is_live_enabled = False

        self.build_layout()
        self.start_server()
 
    def build_layout(self):
        self.action_bar = ActionBar()
        self.panel_layout = PanelLayout()
        self.map_layout = MapLayout()

        self.add_widget(self.action_bar)
        self.add_widget(self.panel_layout)
        self.add_widget(self.map_layout)
    
    def start_server(self):
        server = SimpleWebSocketServer('', 8000, WsServer)
        t = Thread(target=server.serveforever)
        t.setDaemon(True)                                   # close threads when app is closed
        t.start()
