#!/usr/bin/python

# SPDX-License-Identifier: AGPL-3.0-only

import struct

from nativeapp.utils.net import network_control_protocol

REMOTE_PORT = 5486
REMOTE_HEADER = 0xFABD


class RemoteCommands:
    SET_MINIMIZE = 1
    SET_ALWAYS_TOP = 2
    SET_POSITION = 3
    SET_FULLSCREEN = 4


class RemoteControlClient(network_control_protocol.NativeappControlClient):
    def __init__(self):
        super().__init__(REMOTE_HEADER, REMOTE_PORT)

    def set_val(self, cmd, enable):
        self.send_command(cmd, struct.pack("<I", enable))

    def set_minimize(self, enable):
        self.set_val(RemoteCommands.SET_MINIMIZE, enable)

    def set_fullscreen(self, enable):
        self.set_val(RemoteCommands.SET_FULLSCREEN, enable)

    def set_on_top(self, enable=True):
        self.set_val(RemoteCommands.SET_ALWAYS_TOP, enable)
