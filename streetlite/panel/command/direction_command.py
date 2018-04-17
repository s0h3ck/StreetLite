from kivy.uix.spinner import Spinner

from streetlite.common.constants import Direction

class DirectionCommand(Spinner):
    def __init__(self):
        super(DirectionCommand, self).__init__()

        self.text='North'
        self.values=('North', 'East', 'West', 'South')
        self.size_hint=(None, None)
        self.size=(60, 44)
        self.pos_hint=({'center_x': .5, 'center_y': .5})

    def show_selected_value(self, *args):
        print("Switching direction to", self.text)

    def get_current_direction(self):
        if self.text == 'North':
            return Direction.NORTH
        if self.text == 'East':
            return Direction.EAST
        if self.text == 'West':
            return Direction.WEST
        if self.text == 'South':
            return Direction.SOUTH
