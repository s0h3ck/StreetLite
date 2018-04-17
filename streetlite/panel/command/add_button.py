from kivy.uix.button import Button

class AddButton(Button):
    def __init__(self):
        super(AddButton, self).__init__()
        self.text = 'Add'

    def add_to_sequence(self, instance, signal_value, slider_value, log):
        print("The button {} will sent {} {}".format(instance.text, signal_value, slider_value))
        print(log.text)
