#!/usr/bin/python

from nativeapp.utils.net import network_control_protocol

REMOTE_PORT = 5486
REMOTE_HEADER = 0xFABD


class RemoteCommands:
    SET_MINIMIZE = 1
    SET_ALWAYS_TOP = 2
    SET_POSITION = 3
    SET_RESTORE = 4


class RemoteControlClient(network_control_protocol.NativeappControlClient):
    def __init__(self):
        super().__init__(REMOTE_HEADER, REMOTE_PORT)

    def set_minimize(self):
        self.send_command(RemoteCommands.SET_MINIMIZE, b"1")

    def set_maximize(self):
        self.send_command(RemoteCommands.SET_MAXIMIZE, b"1")

    def set_on_top(self, enable=True):
        state = b"0" if enable else b"1"
        self.send_command(RemoteCommands.SET_ALWAYS_TOP, state)
