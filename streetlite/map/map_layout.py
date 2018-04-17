from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.garden.mapview import MapView
from kivy.uix.togglebutton import ToggleButton

import time
from threading import Thread

from streetlite import app
from streetlite.map.lamp import Lamp
from streetlite.map.line_map_layer import LineMapLayer
from streetlite.common.constants import Action, Direction, Intersection, Mode
from streetlite.panel.command.command import Command
from streetlite.panel.sequence.sequence import Sequence
from streetlite.panel.command.direction_tools import DirectionTools

class MapLayout(BoxLayout):
    SIMULATOR_DELAY = 0.25                                  # seconds
    YELLOW_DELAY = 3                                        # seconds
    POST_YELLOW_DELAY = 1                                   # seconds
    TOTAL_YELLOW_DELAY = YELLOW_DELAY + POST_YELLOW_DELAY   # seconds

    def __init__(self, **kwargs):
        super(MapLayout, self).__init__(**kwargs)
        
        self.orientation='vertical'
        self.padding = 10
        self.mapview = MapView(zoom=18, lat=49.26040, lon=-123.11400)
        self.layer = LineMapLayer()
        self.mapview.add_layer(self.layer, mode="scatter")  # window scatter
        self.add_widget(self.mapview)

        mode_layout = BoxLayout(height='48dp',size_hint_y=None)
        self.live_button = ToggleButton(text='Live', group='live_mode')
        self.live_button.fbind('on_press', self.click_live)
        self.simulation_button = ToggleButton(text='Simulation', group='live_mode')
        self.simulation_button.fbind('on_press', self.click_simulation)

        mode_layout.add_widget(self.live_button)
        mode_layout.add_widget(self.simulation_button)

        self.add_widget(mode_layout)
        
        self.lamps = []
        self.init_lamps()

        self.sequence = None
        self.simulation_thread = Thread(target=self.run_simulation)

        self.mode_stop_flags = [False, False]
        self.live_intersection_blinking = [False, False]

    def init_lamps(self):

        # TODO: Should be based on an algorithm to retrieve the coordinate intersections

        self.lamps.append(Lamp(Intersection.A, Direction.NORTH, 49.26049, -123.11507))
        self.lamps.append(Lamp(Intersection.A, Direction.SOUTH, 49.26025, -123.11507))
        self.lamps.append(Lamp(Intersection.A, Direction.WEST, 49.26037, -123.11523))
        self.lamps.append(Lamp(Intersection.A, Direction.EAST, 49.26035, -123.11490))
        self.lamps.append(Lamp(Intersection.B, Direction.NORTH, 49.26044, -123.11308))
        self.lamps.append(Lamp(Intersection.B, Direction.SOUTH, 49.26022, -123.11309))
        self.lamps.append(Lamp(Intersection.B, Direction.WEST, 49.26033, -123.11324))
        self.lamps.append(Lamp(Intersection.B, Direction.EAST, 49.26033, -123.11292))

        for lamp in self.lamps:
            self.layer.add_circle(lamp)

    def set_lamp(self, intersection, direction, status):
     
        if intersection == Intersection.BOTH:
            self.set_lamp(intersection.A, direction, status)
            self.set_lamp(intersection.B, direction, status)
        else:
            lamp = self.find_lamp(intersection, direction)

            if lamp != None:
                lamp.change_status(status)
                self.layer.add_circle(lamp)
                self.layer.update()         #TODO éventuellement faire un seul refresh pour tous les feux

    def set_intersection_lamps(self, intersection, status):
        if intersection == Intersection.BOTH:
            for lamp in self.lamps:
                lamp.change_status(status)
                self.layer.add_circle(lamp)
        else:
            for lamp in self.lamps:
                if lamp.intersection == intersection:
                    lamp.change_status(status)
                    self.layer.add_circle(lamp)
        self.layer.update()

    def apply_command(self, command):
        if app.kivy_root.is_live_enabled:
            apply_live_command(command)
        else:
            apply_simulator_command(command)

    def apply_live_command(self, command):
        print("Live command: ")
        print(command.action)
        print(command.direction)
        print(command.intersection)
        print('')

        self.apply_yellow_lights(command)
        if command.action == Action.PEDESTRIAN:
            self.set_intersection_lamps(command.intersection, 'white')
        elif command.action == Action.GREEN:
            next_direction = DirectionTools.get_next_direction(command.direction)
            self.set_lamp(command.intersection, command.direction, 'green')
            self.set_lamp(command.intersection, DirectionTools.get_facing_direction(command.direction), 'green')
            self.set_lamp(command.intersection, next_direction, 'red')
            self.set_lamp(command.intersection, DirectionTools.get_facing_direction(next_direction), 'red')
        elif command.action == Action.FLASH_GREEN:
            next_direction = DirectionTools.get_next_direction(command.direction)

            self.set_lamp(command.intersection, DirectionTools.get_facing_direction(command.direction), 'red')
            self.set_lamp(command.intersection, next_direction, 'red')
            self.set_lamp(command.intersection, DirectionTools.get_facing_direction(next_direction), 'red')

            blinking_index = 0 if command.intersection == Intersection.A else 1
            self.live_intersection_blinking[blinking_index] = True

            next_color = "green"
            while app.kivy_root.is_live_enabled and self.live_intersection_blinking[blinking_index]:
                time.sleep(MapLayout.SIMULATOR_DELAY)

                self.set_lamp(command.intersection, command.direction, next_color)
                next_color = "transparent" if next_color == "green" else "green"
            self.set_lamp(command.intersection, command.direction, "green")

    def apply_simulator_command(self, command):
        self.apply_yellow_lights(command)

        effective_duration = command.duration - MapLayout.TOTAL_YELLOW_DELAY

        if command.action == Action.PEDESTRIAN:
            self.set_intersection_lamps(command.intersection, 'white')
            self.sleep_if_mode_enabled(command.duration, Mode.SIMULATION)
        elif command.action == Action.GREEN:
            next_direction = DirectionTools.get_next_direction(command.direction)

            self.set_lamp(Intersection.BOTH, command.direction, 'green')
            self.set_lamp(Intersection.BOTH, DirectionTools.get_facing_direction(command.direction), 'green')
            self.set_lamp(Intersection.BOTH, next_direction, 'red')
            self.set_lamp(Intersection.BOTH, DirectionTools.get_facing_direction(next_direction), 'red')
            self.sleep_if_mode_enabled(effective_duration, Mode.SIMULATION)
        elif command.action == Action.FLASH_GREEN:
            next_direction = DirectionTools.get_next_direction(command.direction)

            self.set_lamp(Intersection.BOTH, DirectionTools.get_facing_direction(command.direction), 'red')
            self.set_lamp(Intersection.BOTH, next_direction, 'red')
            self.set_lamp(Intersection.BOTH, DirectionTools.get_facing_direction(next_direction), 'red')

            next_color = "green"
            if effective_duration > 0:
                sim_time = time.time()
                elapsed_time = 0

                while elapsed_time < effective_duration and not self.mode_stop_flags[Mode.SIMULATION.value]:
                    time.sleep(MapLayout.SIMULATOR_DELAY)
                    elapsed_time = time.time() - sim_time

                    self.set_lamp(Intersection.BOTH, command.direction, next_color)
                    next_color = "transparent" if next_color == "green" else "green"

    def apply_yellow_lights(self, command):
        next_direction = DirectionTools.get_next_direction(command.direction)
        directions_to_check = []
        yellow_lamps = []

        if command.action == Action.PEDESTRIAN:
            directions_to_check = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        else:
            directions_to_check.append(next_direction)
            directions_to_check.append(DirectionTools.get_facing_direction(next_direction))

            if command.action == Action.FLASH_GREEN:
                directions_to_check.append(DirectionTools.get_facing_direction(command.direction))

        if command.intersection == Intersection.BOTH:
            for lamp in self.lamps:
                if lamp.direction in directions_to_check and (lamp.status == 'green' or lamp.status == 'transparent'):
                    lamp.change_status('yellow')
                    self.layer.add_circle(lamp)
                    yellow_lamps.append(lamp)
        else:
            for lamp in self.lamps:
                if lamp.direction in directions_to_check and (lamp.status == 'green' or lamp.status == 'transparent') and lamp.intersection == command.intersection:
                    lamp.change_status('yellow')
                    self.layer.add_circle(lamp)
                    yellow_lamps.append(lamp)

        if len(yellow_lamps) > 0:
            active_mode = Mode.LIVE if app.kivy_root.is_live_enabled else Mode.SIMULATION
            self.layer.update()
            self.sleep_if_mode_enabled(MapLayout.YELLOW_DELAY, active_mode)

            for lamp in yellow_lamps:
                lamp.change_status('red')
                self.layer.add_circle(lamp)
            self.layer.update()
            self.sleep_if_mode_enabled(MapLayout.POST_YELLOW_DELAY, active_mode)

    def find_lamp(self, intersection, direction):
        found_lamp = None

        for lamp in self.lamps:
            if lamp.intersection == intersection and lamp.direction == direction:
                found_lamp = lamp
                break

        return found_lamp

    def click_simulation(self, btn):
        if btn.state == "down":
            app.kivy_root.is_live_enabled = False
            self.launch_simulation()
        else:
            self.stop_simulation()

    def click_live(self, btn):
        if btn.state == "down":
            self.stop_simulation()
            self.mode_stop_flags[Mode.LIVE.value] = False
            app.kivy_root.is_live_enabled = True
        else:
            app.kivy_root.is_live_enabled = False
            self.set_intersection_lamps(Intersection.BOTH, 'red')

    def launch_simulation(self):
        self.mode_stop_flags[Mode.SIMULATION.value] = False
        self.set_intersection_lamps(Intersection.BOTH, 'red')
        
        commands = self.parent.panel_layout.sequence_layout.layout.get_commands()
        if len(commands) > 0:
            self.sequence = Sequence(False, 0, 0)
            self.sequence.commands = commands

        if self.simulation_thread.is_alive():
            self.simulation_thread.join()

        if self.sequence != None:
            self.simulation_thread = Thread(target=self.run_simulation)
            self.simulation_thread.setDaemon(True)                                   # close threads when app is closed
            self.simulation_thread.start()

    def stop_simulation(self):
        self.mode_stop_flags[Mode.SIMULATION.value] = True
        if self.simulation_thread != None and self.simulation_thread.is_alive():
            self.simulation_thread.join()
        self.set_intersection_lamps(Intersection.BOTH, 'red')

    def run_simulation(self):
        while not self.mode_stop_flags[Mode.SIMULATION.value]:
            for cmd in self.sequence.commands:
                if not self.mode_stop_flags[Mode.SIMULATION.value]:
                    self.apply_simulator_command(cmd)

    def sleep_if_mode_enabled(self, delay, mode):
        if delay > 0:
            sim_time = time.time()
            elapsed_time = 0

            while elapsed_time < delay and not self.mode_stop_flags[mode.value]:
                time.sleep(MapLayout.SIMULATOR_DELAY)
                elapsed_time = time.time() - sim_time