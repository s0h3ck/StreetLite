from kivy.uix.boxlayout import BoxLayout

class CommandLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_buttons = []

    def add_command(self, button):
        self.list_buttons.append(button)
        self.add_widget(button)

    def remove_element(self, button):
        self.list_buttons.remove(button)
        self.remove_widget(button)

    def clear(self, instance):
        for b in self.list_buttons:
            self.remove_widget(b)

    def clear_all(self):
        for b in self.list_buttons:
            self.remove_widget(b)
        self.list_buttons.clear()

    def get_commands(self):
        commands = []
        for cmd_button in self.list_buttons:
            commands.append(cmd_button.command)

        return commands