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

from nativeapp.controller import demo_controller

from nativeapp.controller.demo_controller import (
    DemoStates,
    ErrorCodes)

from nativeapp.config import config

from demos.uhh_keylogger.native import uhh_keylogger_demo


class KeyloggerController(demo_controller.DemoController):
    def __init__(self):
        super().__init__("uhh_keylogger",
                        "uhh_keylogger/native/stacks/docker-compose.yml") # noqa: 501
        self.keylog_service = uhh_keylogger_demo.KeyloggerDemo()

    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        try:
            self.set_state(DemoStates.STOPPING,
                           DemoStates.STOPPING_APPLICATIONS)
            self.keylog_service.stop()
            self.set_state(DemoStates.STOPPING, DemoStates.STOPPING_CONTAINER)
            self.stop_container()
        except Exception:
            pass
        self.set_state(DemoStates.OFFLINE)
        return ErrorCodes.stop_success

    def start(self, subpath, params) -> int:
        """
        Start the demo
        """
        try:
            if subpath == "open":
                self.keylog_service.execute()
            else:
                logging.info("Starting uhh_keylogger demo stack"
                             f"with {params} and language "
                             f"{config.EnvironmentConfig.LANGUAGE}")
                if self.get_state() != DemoStates.OFFLINE:
                    self.set_state(DemoStates.ERROR)
                    return ErrorCodes.invalid_state
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_CONTAINER)
                lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}

                # For setting hosts entry
                self.keylog_service.prepare()

                self.start_container(lang_env)
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_APPLICATIONS)
                self.keylog_service.start()
                self.set_state(DemoStates.READY)
        except Exception as e:
            logging.error(e)
            self.set_state(DemoStates.ERROR, str(e))
            return ErrorCodes.no_docker_error
        return ErrorCodes.start_success

    def enter(self, subpath):
        if self.get_state() == DemoStates.READY:
            self.set_state(DemoStates.RUNNING)
            self.keylog_service.keylog()
            self.keylog_service.send_mails()
        return ErrorCodes.start_success


def get_controller():
    return KeyloggerController()
