import logging

from nativeapp.controller import demo_controller
from nativeapp.utils.admin import admin_app
from nativeapp.config import config


class PasswordController(demo_controller.DemoController):

    def __init__(self):
        super().__init__("hda_password",
                         "hda_password/native/stacks/"
                         "secure/docker-compose.yml")
        self.admin_client = admin_app.NativeappAdminClient()

    def start(self, subpath, params):
        secure_mode = True
        self.set_state("starting")
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

        try:
            if "language" in params:
                config.EnvironmentConfig.LANGUAGE = params["language"]
            logging.info("Starting password demo stack")
            lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
            self.start_container(lang_env)
        except Exception as e:
            logging.error(e)
            self.set_state("offline")
            return demo_controller.ErrorCodes.no_docker_error
        self.set_state("running")
        logging.info("Sucess")
        return demo_controller.ErrorCodes.start_success

    def stop(self, subpath):
        logging.info("Stopping Container")
        self.set_state("stopping")
        self.stop_container()
        logging.info("Stop done")
        self.set_state("offline")
        return demo_controller.ErrorCodes.stop_success


def get_controller():
    return PasswordController()
