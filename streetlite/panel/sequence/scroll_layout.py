from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class ScrollLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_layout = []

    def set_default(self, button):
        layout = BoxLayout(orientation='horizontal', size_hint_y=None)
        layout.add_widget(button)
        self.add_widget(layout)

    def add_element(self, button):
        remove_button = Button(text="X", height='32dp', size_hint_x=0.3)
        layout = BoxLayout(orientation='horizontal', size_hint_y=None)

        layout.add_widget(button)
        layout.add_widget(remove_button)
        
        remove_button.fbind('on_release', self.remove_layout, layout=layout)

        idx = self.get_index(button.sequence)
        self.add_widget(layout, idx)
        self.list_layout.append(layout)

    def remove_layout(self, instance, layout):
        self.list_layout.remove(layout)
        self.remove_widget(layout)

    def clear(self, instance):
        for b in self.list_layout:
            self.remove_widget(b)
        self.list_layout.clear()

    def validate_sequence(self, start, end, old_start = None, old_end = None):
        for item in self.list_layout:
            item_start = item.children[1].sequence.time_start
            item_end = item.children[1].sequence.time_end
            
            if ( old_start != None ) and ( old_end != None ):
                if (item_start == old_start) and (item_end == old_end):
                    continue

            if (item_start == start) and (item_end == end):
                return False
            if item_start < item_end:
                if start < end:
                    if (end > item_start) and (start < item_end):
                        return False
                else:
                    if start < item_end:
                        return False
                    if end > item_start:
                        return False
            else:
                if start < end:
                    if end > item_start:
                        return False
                    if start < item_end:
                        return False
                else:
                    return False
        return True

    def get_index(self, seq):
        start = seq.time_start
        idx = 0
        for item in self.children[:-1]:
            if (item.children[1].sequence.time_start <= start):
                break
            idx = idx + 1
        return idx 
