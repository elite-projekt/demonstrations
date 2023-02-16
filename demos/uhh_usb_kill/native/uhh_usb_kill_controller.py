# SPDX-License-Identifier: AGPL-3.0-only

"""
Copyright (C) 2022 Kevin Köster

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""
import logging

from nativeapp.config import config
from nativeapp.controller.demo_controller import (
    DemoController,
    DemoStates,
    ErrorCodes)

from demos.uhh_usb_kill.native import uhh_usb_kill_demo
from nativeapp.utils.thread_helper import lock_function


class KillController(DemoController):
    def __init__(self):
        super().__init__("uhh_usb_kill",
                         "uhh_usb_kill/native/stacks/docker-compose.yml")
        self.kill_service = uhh_usb_kill_demo.KillDemo()

    @lock_function
    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        if (self.get_state() != DemoStates.STOPPING and
           self.get_state() != DemoStates.OFFLINE):
            self.set_state(DemoStates.STOPPING)
            self.stop_container()
            self.kill_service.stop()
            self.set_state(DemoStates.OFFLINE)
        return ErrorCodes.stop_success

    @lock_function
    def start(self, subpath, params):
        """
        Start the demo
        """
        if self.get_state() == DemoStates.OFFLINE:
            try:
                if "language" in params:
                    config.EnvironmentConfig.LANGUAGE = params["language"]

                logging.info("Starting uhh_usb_kill demo stack")
                if self.get_state() != "offline":
                    return ErrorCodes.invalid_state
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_CONTAINER)
                lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
                self.start_container(lang_env)
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_APPLICATIONS)
                self.kill_service.start()
                self.set_state(DemoStates.READY)
            except Exception as e:
                logging.error(e)
                return ErrorCodes.no_docker_error
        return ErrorCodes.start_success

    @lock_function
    def enter(self, subpath):
        if self.get_state() == DemoStates.READY:
            self.kill_service.send_mails()
            self.set_state(DemoStates.RUNNING)
        return ErrorCodes.start_success


def get_controller():
    return KillController()
