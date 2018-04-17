from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.logger import Logger

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from streetlite.common.constants import Action, Direction
from streetlite.panel.sequence.scroll_layout import ScrollLayout
from streetlite.panel.sequence.sequence_button import SequenceButton
from streetlite.panel.command.command import Command

import streetlite.app
from streetlite.panel.sequence.spinner_time_selector import hours


class SequenceListLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SequenceListLayout, self).__init__(**kwargs)
        
        self.orientation = "vertical"
        self.padding = 10
        self.margin = 2

        self.build_layout()
    
    def build_layout(self):
        
        self.add_button = Button(text="Add Sequence", background_color=(0.0,1.0,0.388,1.0), height=40, size_hint_y=None)
        self.button_clear = Button(text="Clear", height=40, size_hint_y=None)
        self.scroll_layout = ScrollLayout(orientation='vertical', size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
 
        self.default_button = SequenceButton(0,0,text="Default")
        
        cmd = Command(Direction.NORTH, Action.GREEN, 10)
        self.default_button.sequence.add_command(cmd)
        
        cmd = Command(Direction.EAST, Action.GREEN, 10)
        self.default_button.sequence.add_command(cmd)
        
        cmd = Command(None, Action.PEDESTRIAN, 10)
        self.default_button.sequence.add_command(cmd)

        self.scroll_layout.set_default(self.default_button)
        self.default_button.fbind('on_press', self.update_selected_sequence)
     
        scrollview = ScrollView(do_scroll_x=False)
        scrollview.add_widget(self.scroll_layout)
       
        self.add_widget(scrollview)
        self.add_widget(self.add_button)
        self.add_widget(self.button_clear)

        self.add_button.bind(on_press=self.add_new_sequence)
        self.button_clear.bind(on_press=self.scroll_layout.clear)

    def add_new_sequence(self, instance):
        time_selector = streetlite.app.kivy_root.panel_layout.sequence_layout.time_layout
        starttime = time_selector.spinner_begin.text
        endtime = time_selector.spinner_end.text
        seq_name = "{} {} {}".format(starttime, "to", endtime)
        
        b = SequenceButton(hours.index(starttime), hours.index(endtime), text=seq_name)

        if self.scroll_layout.validate_sequence(b.sequence.time_start, b.sequence.time_end):
            b.fbind('on_press', self.update_selected_sequence)
            self.scroll_layout.add_element(b)
        else:
            close_button = Button(text="Close", font_size=12)
            popup = Popup(title='Error: sequence time conflict', content=(close_button), size_hint=(.4,.1))
            close_button.bind(on_press=popup.dismiss)  
            popup.open()

    def add_sequence(self, button):
        self.layout.add_element(button)

    def update_selected_sequence(self, instance):
        self.parent.sequence_layout.select_sequence(instance)
        Logger.info("Selecting the sequence")
