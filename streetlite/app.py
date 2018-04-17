#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger

from streetlite.streetlite import StreetLite

kivy_root = None

class StreetLiteApp(App):
    title = 'StreetLite'

    def build(self):
        Config.set('kivy', 'log_level', 'debug')
        return StreetLite()

    def on_start(self):
        global kivy_root
        kivy_root = self.root
        Logger.info('App: I\'m on start!')

    def on_stop(self):
        Logger.critical('App: I\'m on stop!')

if __name__ == '__main__':
    StreetLiteApp().run()
