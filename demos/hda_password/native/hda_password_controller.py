import logging
import webbrowser
import importlib.resources

from nativeapp.controller import demo_controller
from nativeapp.utils.browser import browser_program
from nativeapp.utils.admin import admin_app
from nativeapp.config import config
from nativeapp.controller.demo_controller import (
    DemoStates,
    ErrorCodes)
from nativeapp.utils.time import sync_wsl


class PasswordController(demo_controller.DemoController):

    def __init__(self):
        super().__init__("hda_password",
                         "hda_password/native/stacks/"
                         "secure/docker-compose.yml")
        self.admin_client = admin_app.NativeappAdminClient()

    def start(self, subpath, params):
        secure_mode = True
        self.set_state("starting")
        sync_wsl()
        if "secureMode" in params:
            secure_mode = params["secureMode"]
        if secure_mode is True:
            self.compose_file = "hda_password/native/stacks/"\
                             "secure/docker-compose.yml"
        else:
            self.compose_file = "hda_password/native/stacks/"\
                             "secure/docker-compose.yml"

        ip = "127.0.0.1"

        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    True, "nimbus.de", f"{ip}"))

        browser_profile = importlib.resources.path(
                "demos.hda_password.resources.edge", "profile_uhh.zip")
        self.browser_program = browser_program.BrowserProgramEdge(
                "elite.uhh_mitm", browser_profile)

        try:
            if "language" in params:
                config.EnvironmentConfig.LANGUAGE = params["language"]
            logging.info("Starting password demo stack")
            lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
            self.start_container(lang_env)
            self.browser_program.copy_profile()
        except Exception as e:
            logging.error(e)
            self.set_state(DemoStates.ERROR)
            return demo_controller.ErrorCodes.no_docker_error
        self.set_state(DemoStates.READY)
        logging.info("Sucess")
        return demo_controller.ErrorCodes.start_success

    def stop(self, subpath):
        """
        Stops the demo
        """
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    False, "nimbus.de"))
        try:
            self.set_state(DemoStates.STOPPING,
                           DemoStates.STOPPING_CONTAINER)
            logging.info("Stopping Container")
            self.stop_container()
            self.set_state(DemoStates.STOPPING,
                           DemoStates.STOPPING_APPLICATIONS)
            logging.info("Stopping Applications")
            self.browser_program.stop()
        except Exception:
            pass
        logging.info("Container stopped")
        self.set_state(DemoStates.OFFLINE)
        return ErrorCodes.stop_success

    def enter(self, subpath):
        if self.get_state() == DemoStates.READY:
            self.set_state(DemoStates.RUNNING)
            # Start Browser
            webbrowser.open('https://nimbus.de', new=1)
        return ErrorCodes.start_success


def get_controller():

    return PasswordController()
