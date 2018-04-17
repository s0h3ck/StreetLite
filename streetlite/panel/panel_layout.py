from kivy.uix.boxlayout import BoxLayout

from streetlite.panel.sequence.sequence_list_layout import SequenceListLayout
from streetlite.panel.sequence.sequence_layout import SequenceLayout

class PanelLayout(BoxLayout):
    def __init__(self):
        super(PanelLayout, self).__init__()

        self.build_layout()

    def build_layout(self):
        self.sequence_list_layout = SequenceListLayout(size_hint_x=.5)
        self.sequence_layout = SequenceLayout()

        self.add_widget(self.sequence_list_layout)
        self.add_widget(self.sequence_layout)
