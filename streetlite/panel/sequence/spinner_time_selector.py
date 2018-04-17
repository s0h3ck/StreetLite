from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label

hours = ("0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", \
        "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00")

class SpinnerTimeSelector(BoxLayout):
    def __init__(self, **kwargs):
        super(SpinnerTimeSelector, self).__init__(**kwargs)
        self.orientation = "horizontal"

        self.spinner_begin = Spinner(text=hours[0], values=hours) 
        self.spinner_end = Spinner(text=hours[1], values = hours)

        self.add_widget(self.spinner_begin)
        self.add_widget( Label(text="to") )
        self.add_widget(self.spinner_end)
        
        self.spinner_begin.bind(text=self.on_spinner_begin_select)
        self.spinner_end.bind(text=self.on_spinner_end_select)

    def on_spinner_begin_select(self, spinner, text):
        print(self.spinner_begin.text)
        
    def on_spinner_end_select(self, spinner, text):
        print(self.spinner_end.text)

    def disable(self):
        self.spinner_begin.disabled = True
        self.spinner_end.disabled = True

    def enable(self):
        self.spinner_begin.disabled = False
        self.spinner_end.disabled = False
