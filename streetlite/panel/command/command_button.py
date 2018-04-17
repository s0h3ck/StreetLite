from kivy.uix.button import Button

from streetlite.panel.command.command import Command

class CommandButton(Button):
    def __init__(self, direction, action, duration, **kwargs):
        super().__init__(**kwargs)
        self.command = Command(direction, action, duration)