import logging

from nativeapp.controller import demo_controller
from demos.phishing.native import phishing_demo


class PhishingController(demo_controller.DemoController):
    def __init__(self):
        super().__init__("phishing",
                         "phishing/native/stacks/docker-compose.yml")
        self.phishing_service = phishing_demo.PhishingDemo()

    def start(self, subpath, params):
        secure_mode = False
        self.set_state("starting")
        if "secureMode" in params:
            secure_mode = params["secureMode"]
        try:
            logging.info("Starting phishing demo stack")
            self.start_container()
            self.phishing_service.thunderbird_init()
            self.phishing_service.check_mail_server_online()
            self.phishing_service.change_client_profile(secure_mode)
            self.phishing_service.delete_mailbox()
            self.phishing_service.send_mail_files(secure_mode)
            self.phishing_service.start_mail_application()
        except Exception as e:
            logging.error(e)
            self.set_state("offline")
            return demo_controller.ErrorCodes.no_docker_error
        except (ConnectionRefusedError, FileNotFoundError):
            logging.error(ConnectionRefusedError, FileNotFoundError)
            self.set_state("offline")
            return demo_controller.ErrorCodes.no_mail_server_error
        self.set_state("running")
        return demo_controller.ErrorCodes.start_success

    def stop(self, subpath):
        self.set_state("stopping")
        self.stop_container()
        self.phishing_service.stop_mail_application()
        self.set_state("offline")
        return demo_controller.ErrorCodes.stop_success


def get_controller():
    return PhishingController()
