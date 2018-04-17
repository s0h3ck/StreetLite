from streetlite.common.constants import Action, Direction, Intersection

class Command():
    def __init__(self, direction, action, duration):
        self.direction = direction
        self.action = action
        self.duration = duration
        self.intersection = Intersection.BOTH

    def to_string(self):
        if self.action != Action.PEDESTRIAN:
            str_cmd = chr(self.action.value) + \
                      chr(self.direction.value) + \
                      chr(int(self.duration))
        else:
            str_cmd = chr(self.action.value) + \
                      chr(int(self.duration))
        return str_cmd

    def is_valid(self):
        return (self.direction in Direction         or self.direction in [item.value for item in Direction]) and \
                (self.action in Action              or self.direction in [item.value for item in Action]) and \
                (self.intersection in Intersection  or self.direction in [item.value for item in Intersection]) and \
                self.duration >= 0 and \
                self.duration <= 255
