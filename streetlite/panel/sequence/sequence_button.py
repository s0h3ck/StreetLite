from kivy.uix.button import Button

from streetlite.panel.sequence.sequence import Sequence

class SequenceButton(Button):
    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        is_default = self.text == "Default"
        self.sequence = Sequence(is_default, start, end)
