from kivy.uix.spinner import Spinner
from streetlite.common.constants import Action

class SignalCommand(Spinner):
    def __init__(self, **kwargs):
        super(SignalCommand, self).__init__(**kwargs)

        self.text='Green'
        self.values=('Green', 'Flash Green', 'Pedestrian')
        self.size_hint=(None, None)
        self.size=(100, 44)
        self.pos_hint=({'center_x': .5, 'center_y': .5})

    def show_selected_value(self, *args):
        print("Switching command to", self.text)
        
    def get_current_action(self):
        if self.text == 'Green':
            return Action.GREEN
        if self.text == 'Flash Green':
            return Action.FLASH_GREEN
        if self.text == 'Pedestrian':
            return Action.PEDESTRIAN
