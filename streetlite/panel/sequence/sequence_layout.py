from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.logger import Logger
from kivy.uix.popup import Popup

from streetlite import app
from streetlite.common.constants import Action, Direction, Intersection
from streetlite.panel.sequence.spinner_time_selector import SpinnerTimeSelector
from streetlite.panel.sequence.spinner_time_selector import hours
from streetlite.panel.command.direction_command import DirectionCommand
from streetlite.panel.sequence.signal_command import SignalCommand
from streetlite.panel.sequence.sequence import Sequence
from streetlite.panel.command.command_layout import CommandLayout
from streetlite.panel.command.command import Command
from streetlite.panel.command.duration_slider import DurationSlider
from streetlite.panel.command.command_button import CommandButton

class SequenceLayout(BoxLayout):
    def __init__(self):
        super(SequenceLayout, self).__init__()
        self.orientation = "vertical"
        self.padding = 10
        self.margin = 10

        upper_layout = BoxLayout(size_hint_y=None, height=40)
        self.sequence_name_label = Label(text="Time Interval")
        self.time_layout = SpinnerTimeSelector()
        self.button_save = Button(text="Save", size_hint_x=None, width=60)
        self.button_save.fbind('on_press', self.save_sequence)

        upper_layout.add_widget(self.sequence_name_label)
        upper_layout.add_widget(self.time_layout)
        upper_layout.add_widget(self.button_save)

        middle_layout = BoxLayout(size_hint_y=None, height=40)

        self.signal = SignalCommand()
        self.signal.bind(text=self.signal.show_selected_value)
        
        self.direction = DirectionCommand()
        self.direction.bind(text=self.direction.show_selected_value)
        
        self.duration_slider = DurationSlider()
        self.duration_slider.bind(value=self.update_slider_value)
        self.duration_label = Label(text="15.0s", size_hint_x=None, width=60)
        self.add_button = Button(text="Add", size_hint_x=None, width=60)
        self.add_button.bind(on_press=self.add_command)
        
        middle_layout.add_widget(self.signal)
        middle_layout.add_widget(self.direction)
        middle_layout.add_widget(self.duration_slider)
        middle_layout.add_widget(self.duration_label)
        middle_layout.add_widget(self.add_button)

        lower_layout = BoxLayout()

        self.button_clear = Button(text = "Clear", size_hint_x=None, width=60)

        self.layout = CommandLayout(orientation="vertical", size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.button_clear.bind(on_press=self.clear_seq)
        sv = ScrollView()
        sv.add_widget(self.layout)

        lower_layout.add_widget(sv)
        lower_layout.add_widget(self.button_clear)

        send_button = Button(text="Send Sequence", size_hint_y=None, height=80)
        send_button.fbind('on_press', self.send_sequence)

        self.sequence = None

        self.add_widget(upper_layout)
        self.add_widget(middle_layout)
        self.add_widget(lower_layout)
        self.add_widget(send_button)

        self.current_selection = None

    def clear_seq(self, instance):
        self.layout.clear_all()

    def update_slider_value(self, instance, value):
        self.duration_label.text = str(value) + 's'
        Logger.debug(self.duration_label.text)

    def add_command(self, instance):
        btn = CommandButton(self.direction.get_current_direction(), self.signal.get_current_action(), self.duration_slider.value, size_hint_y=None, height=40)
        btn.text = self.text_command(btn.command)
        self.layout.add_command(btn)
        Logger.info("Add command")

    def save_sequence(self, instance):
        if self.sequence != None:
            print(self.sequence.to_string())
            new_time_start = hours.index(self.time_layout.spinner_begin.text)
            new_time_end = hours.index(self.time_layout.spinner_end.text)
            if (new_time_start != self.sequence.time_start) or (new_time_end != self.sequence.time_end):
                if not self.parent.sequence_list_layout.scroll_layout.validate_sequence(new_time_start, new_time_end, self.sequence.time_start, self.sequence.time_end):
                    close_button = Button(text="Close", font_size=12)
                    popup = Popup(title='Error: sequence time conflict', content=(close_button), size_hint=(.4,.1))
                    close_button.bind(on_press=popup.dismiss)  
                    popup.open()
                    return
            
            if self.sequence.time_start != new_time_start:
                seq_layout = self.current_selection.parent
                self.parent.sequence_list_layout.scroll_layout.remove_widget(seq_layout)
                self.sequence.time_start = new_time_start
                self.sequence.time_end = new_time_end
                self.parent.sequence_list_layout.scroll_layout.add_widget(seq_layout, self.parent.sequence_list_layout.scroll_layout.get_index(self.sequence))
            else:
                self.sequence.time_start = new_time_start
                self.sequence.time_end = new_time_end
            
            starttxt = hours[new_time_start]
            endtxt = hours[new_time_end]
            seq_name = "{} {} {}".format(starttxt, "to", endtxt)
            self.current_selection.text = seq_name
            
            self.sequence.commands.clear()
            for btn in self.layout.list_buttons:
                self.sequence.add_command(btn.command)

    def text_command(self, command):
        text_command = ""
        
        if command.action == Action.GREEN:
            text_command += "Green "
        elif command.action == Action.FLASH_GREEN:
            text_command += "Flash Green "
        else:
            text_command += "Pedestrian " 
            text_command += str(command.duration) + "s"
            return text_command

        if command.direction == Direction.NORTH:
            text_command += "North "
        elif command.direction == Direction.EAST:
            text_command += "East "
        elif command.direction == Direction.WEST:
            text_command += "West "
        else:
            text_command += "South "

        text_command += str(command.duration) + "s"
        
        return text_command

    def select_sequence(self, button):
        if self.current_selection != button:
            if button.text == "Default":
                for child in self.children[1:]:
                    child.disabled = True
            else:
                for child in self.children[1:]:
                    child.disabled = False
            self.layout.clear_all()
            self.sequence = button.sequence
            self.time_layout.spinner_begin.text = ("{}:00".format(button.sequence.time_start))
            self.time_layout.spinner_end.text = ("{}:00".format(button.sequence.time_end))
            for command in self.sequence.commands:
                self.layout.add_command(CommandButton(command.direction, command.action, command.duration, text=self.text_command(command), size_hint_y=None, height=40))
            Logger.info("Set the property")
            self.current_selection = button
        else:
            Logger.info("Already selected")

    def send_sequence(self, *args):
        sequence = Sequence(False, 0, 0)
        sequence.commands = self.layout.get_commands()

        if sequence != None:
            print(sequence.to_string())

            for client in app.kivy_root.clients:
                client.sendMessage(sequence.to_string())
