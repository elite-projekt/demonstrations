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
import flask
import logging

from nativeapp.controller import orchestration_controller, demo_controller
from nativeapp.config import config

from demos.uhh_ducky_mitm.native import uhh_ducky_mitm_demo


class DuckyController(demo_controller.DemoController):
    def __init__(self):
        super().__init__("uhh_ducky_mitm",
                         "uhh_ducky_mitm/native/stacks/docker-compose.yml")
        self.ducky_service = uhh_ducky_mitm_demo.DuckyDemo()

    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        self.set_state("stopping")
        orchestration_controller.orchestration_service.\
            docker_compose_stop_file(self.compose_file)
        self.ducky_service.stop()
        self.set_state("offline")
        return orchestration_controller.stop_success

    def start(self, subpath) -> int:
        """
        Start the demo
        """
        if subpath == "script_downloaded":
            self.ducky_service.add_cert()
            self.ducky_service.show_error_box()
            self.ducky_service.send_second_mail()
            return 1

        else:
            try:
                try:
                    config.EnvironmentConfig.LANGUAGE = \
                            flask.request.json["language"]
                except Exception:
                    pass
                logging.info("Starting uhh_ducky_mitm demo stack")
                self.set_state("starting")
                lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
                orchestration_controller.orchestration_service \
                    .docker_compose_start_file(self.compose_file,
                                               additional_env=lang_env)
                orchestration_controller.orchestration_service \
                    .wait_for_container("uhh_ducky_mitm_mailserver")
                self.ducky_service.start()
                self.set_state("running")
            except Exception as e:
                logging.error(e)
                return orchestration_controller.no_docker_error
            return orchestration_controller.start_success


def get_controller():
    return DuckyController()
