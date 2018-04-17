from kivy.uix.slider import Slider

class DurationSlider(Slider):
    def __init__(self, **kwargs):
        super(DurationSlider, self).__init__(**kwargs)

        self.min = 0
        self.max = 180
        self.value = 15
        self.step = 5

    def show_slider_value(self, *args):
        print('Duration is set to', int(self.value), 'seconds') 
