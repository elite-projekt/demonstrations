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
import webbrowser
import importlib

from nativeapp.controller import demo_controller
from nativeapp.controller.demo_controller import (
    DemoStates,
    ErrorCodes)

from nativeapp.utils.locale import locale
from nativeapp.utils.admin import admin_app
from nativeapp.utils.browser import browser_program

from nativeapp.config import config


class EvilTwinController(demo_controller.DemoController):
    def __init__(self):
        super().__init__("uhh_evil_twin",
                        "uhh_evil_twin/native/stacks/docker-compose.yml") # noqa: 501
        localedir = pathlib.Path(__file__).parent.parent / "locales"
        self.locale = locale.Locale()
        self.locale.add_locale_dir(localedir)
        self.admin_client = admin_app.NativeappAdminClient()
        with importlib.resources.path(
                "demos.uhh_ducky_mitm.resources.edge",
                "profile_uhh.zip") as browser_profile:
            self.browser_program = browser_program.BrowserProgramEdge(
                    "elite.uhh_mitm", browser_profile)

    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        try:
            self.set_state(DemoStates.STOPPING,
                           DemoStates.STOPPING_APPLICATIONS)
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
            self.set_state(DemoStates.STARTING,
                           DemoStates.STARTING_CONTAINER)
            lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}

            self.start_container(lang_env)
            self.admin_client.send_command(
                    admin_app.NativeappCommands.SET_REDIRECT,
                    admin_app.create_host_payload(
                        True, "nimbus.de", "127.0.0.1"))
            self.browser_program.copy_profile()
            self.browser_program.set_default()
            self.set_state(DemoStates.READY)
        except Exception as e:
            logging.error(e)
            self.set_state(DemoStates.ERROR, str(e))
            return ErrorCodes.no_docker_error
        return ErrorCodes.start_success

    def enter(self, subpath):
        webbrowser.open('https://nimbus.de', new=1)
        self.set_state(DemoStates.RUNNING)
        return ErrorCodes.start_success

    def get_data(self, subpath):
        ret_val = {}
        if subpath == "translations":
            locale_strings = [
                              "uhh_evil_twin_step_one_heading",
                              "uhh_evil_twin_step_one_text",
                              "uhh_evil_twin_step_two_heading",
                              "uhh_evil_twin_step_two_text",
                              "uhh_evil_twin_step_three_heading",
                              "uhh_evil_twin_step_three_text",
                              "uhh_evil_twin_step_four_heading",
                              "uhh_evil_twin_step_four_text",
                              "uhh_evil_twin_step_five_heading",
                              "uhh_evil_twin_step_five_text",
                              "uhh_evil_manual_button",
                              "uhh_evil_twin_heading",
                              "uhh_evil_twin_text",
                              "uhh_evil_own_device_button",
                              "uhh_evil_provided_device_button",
                              "uhh_evil_twin_begin_heading",
                              "uhh_evil_twin_begin_text"
                             ]
            translation_dict = {
                    s: self.locale.translate(s) for s in locale_strings
                    }
            ret_val = {"translations": translation_dict}
        return ret_val


def get_controller():
    return EvilTwinController()
