import logging

from nativeapp.controller import demo_controller


class PasswordController(demo_controller.DemoController):

    def __init__(self):
        super().__init__("hda_password",
                         "hda_password/native/stacks/"
                         + "secure/docker-compose.yml")

    def start(self, subpath, params):
        secure_mode = True
        self.set_state("starting")
        if "secureMode" in params:
            secure_mode = params["secureMode"]
        if secure_mode is True:
            super().__init__("hda_password",
                             "hda_password/native/stacks/"
                             + "secure/docker-compose.yml")
        else:
            super().__init__("hda_password",
                             "hda_password/native/stacks/"
                             + "secure/docker-compose.yml")
        try:
            logging.info("Starting password demo stack")
            self.start_container()
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
