from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import time
from threading import Thread

from streetlite import app
from streetlite.common.constants import Action, Direction, Intersection
from streetlite.panel.command.command import Command

class WsServer(WebSocket):

    def handleMessage(self):
        for client in app.kivy_root.clients:
            if client != self:
                client.sendMessage(self.data)

        print('Message received: ' + self.data)

        if app.kivy_root.is_live_enabled and len(self.data) > 0:
            cmd = Command(None, None, None)
            cmd.action = Action.from_value(ord(self.data[0]))

            is_valid = True

            if cmd.action == Action.PEDESTRIAN and len(self.data) == 3:
                cmd.duration = ord(self.data[1])
                cmd.intersection = Intersection.from_value(ord(self.data[2]))
                is_valid = True
            elif cmd.action == Action.EMERGENCY and len(self.data) == 4:
                cmd.action = Action.from_value(ord(self.data[1]))
                cmd.direction = Direction.from_value(ord(self.data[2]))
                cmd.intersection = Intersection.from_value(ord(self.data[3]))
                is_valid = True
            elif (cmd.action == Action.FLASH_GREEN or cmd.action == Action.GREEN) and len(self.data) == 3:
                cmd.direction = Direction.from_value(ord(self.data[1]))
                cmd.intersection = Intersection.from_value(ord(self.data[2]))
                is_valid = True
            else:
                print('unknown command')
                print(hex(cmd.action))
                print(len(self.data))

            if is_valid:
                self.command = cmd
                launch_thread = Thread(target=self.launch_command_thread)
                launch_thread.setDaemon(True)                                   # close threads when app is closed
                launch_thread.start()

    def handleConnected(self):
        print(self.address, 'connected')
        app.kivy_root.clients.append(self)
        self.init_threads_if_needed()

    def handleClose(self):
        app.kivy_root.clients.remove(self)
        print(self.address, 'closed')

    def launch_command_thread(self):
        intersection_index = 0 if self.command.intersection == Intersection.A else 1
        app.kivy_root.map_layout.live_intersection_blinking[intersection_index] = False

        # If a thread is running for this intersection, wait for it to die (should take less than 1s)
        if self.intersection_threads[intersection_index] != None:
            self.intersection_threads[intersection_index].join()

        self.intersection_threads[intersection_index] = Thread(target=self.execute_stored_command)
        self.intersection_threads[intersection_index].setDaemon(True)                                   # close threads when app is closed
        self.intersection_threads[intersection_index].start()

    def execute_stored_command(self):
        app.kivy_root.map_layout.apply_live_command(self.command)

    def init_threads_if_needed(self):
        if not hasattr(self, 'intersection_threads'):
            self.intersection_threads = [None, None]