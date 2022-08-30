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
import pathlib

from nativeapp.controller import demo_controller
from nativeapp.config import config

from demos.uhh_usb_kill.native import uhh_usb_kill_demo


class KillController(demo_controller.DemoController):
    def __init__(self):
        super().__init__("uhh_usb_kill",
                        f"{pathlib.Path(uhh_usb_kill_demo.__file__).parent}/stacks/docker-compose.yml") # noqa: 501
        self.kill_service = uhh_usb_kill_demo.KillDemo()

    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        self.set_state("stopping")
        self.stop_container()
        self.kill_service.stop()
        self.set_state("offline")
        return demo_controller.ErrorCodes.stop_success

    def start(self, subpath, params) -> int:
        """
        Start the demo
        """
        try:
            if "language" in params:
                config.EnvironmentConfig.LANGUAGE = params["language"]

            logging.info("Starting uhh_usb_kill demo stack")
            self.set_state("starting")
            lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
            self.start_container(lang_env)
            self.kill_service.start()
            self.set_state("running")
        except Exception as e:
            logging.error(e)
            return demo_controller.ErrorCodes.no_docker_error
        return demo_controller.ErrorCodes.start_success


def get_controller():
    return KillController()
