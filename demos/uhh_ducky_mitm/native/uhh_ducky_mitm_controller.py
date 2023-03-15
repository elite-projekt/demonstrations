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
import traceback

from nativeapp.controller.demo_controller import (
    DemoController,
    DemoStates,
    ErrorCodes)
from nativeapp.config import config

from demos.uhh_ducky_mitm.native import uhh_ducky_mitm_demo


class DuckyController(DemoController):
    def __init__(self):
        super().__init__("uhh_ducky_mitm",
                         "uhh_ducky_mitm/native/stacks/docker-compose.yml")
        self.ducky_service = uhh_ducky_mitm_demo.DuckyDemo()
        self.logged_in = False

    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        try:
            self.set_state(DemoStates.STOPPING,
                           DemoStates.STOPPING_APPLICATIONS)
            self.logged_in = False
            self.ducky_service.stop()
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
        logging.info(f"Ducky start with {subpath=} and {params=}")

        if subpath == "script_downloaded":
            self.ducky_service.add_cert()
            self.ducky_service.show_error_box()
            self.ducky_service.send_second_mail()
            return ErrorCodes.start_success
        elif subpath == "login":
            self.ducky_service.add_credentials(params["user"], params["pw"])
            if not self.logged_in:
                self.logged_in = True
                self.ducky_service.send_attacked_mails()
            return ErrorCodes.start_success
        else:
            try:
                if "language" in params:
                    config.EnvironmentConfig.LANGUAGE = params["language"]

                logging.info("Starting uhh_ducky_mitm demo stack"
                             f"with {params} and language "
                             f"{config.EnvironmentConfig.LANGUAGE}")
                if self.get_state() != DemoStates.OFFLINE:
                    self.set_state(DemoStates.ERROR)
                    return ErrorCodes.invalid_state
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_CONTAINER)
                lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
                self.ducky_service.prepare()
                self.start_container(lang_env)
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_APPLICATIONS)
                self.ducky_service.start()
                self.set_state(DemoStates.READY)
            except Exception as e:
                logging.error(traceback.format_exc())
                logging.error(e)
                self.set_state(DemoStates.ERROR, str(e))
                return ErrorCodes.no_docker_error
            return ErrorCodes.start_success

    def enter(self, subpath):
        if self.get_state() == DemoStates.READY:
            self.set_state(DemoStates.RUNNING)
            self.ducky_service.send_mails()
        return ErrorCodes.start_success

    def get_data(self, subpath):
        if subpath == "translations":
            locale = self.ducky_service.locale
            locale_strings = ["uhh_web_loading",
                              "uhh_web_loading_error",
                              "uhh_web_stolen_data",
                              "uhh_web_table_link",
                              "uhh_web_status_button",
                              "nimbus_login_button",
                              "nimbus_password",
                              "nimbus_username",
                              "nimbus_login_text",
                              "nimbus_login_header",
                              "uhh_web_status_after_images",
                              "uhh_web_status_after_button",
                              "uhh_web_status_before_button",
                              "uhh_web_table_after_link",
                              "uhh_web_table_before_link"]
            translation_dict = {s: locale.translate(s) for s in locale_strings}
            ret_val = {"translations": translation_dict}
        else:
            ret_val = {"credentials": self.ducky_service.logged_credentials}
        return ret_val


def get_controller():
    return DuckyController()
