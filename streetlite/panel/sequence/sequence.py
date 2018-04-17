class Sequence():
    def __init__(self, default, start, end):
        self.time_start = start
        self.time_end = end
        self.commands = []
        self.is_default = default

    def add_command(self, cmd):
        self.commands.append(cmd)

    def to_string(self):
        str_sequence = ''

        for cmd in self.commands:
            str_sequence += cmd.to_string()
        return str_sequence