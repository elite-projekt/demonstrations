import logging

from nativeapp.controller import demo_controller
from demos.iao_ransomware_email.native import iao_ransomware_email_code, iao_ransomware_email_demo  # noqa: E501


class RansomwareController(demo_controller.DemoController):
    def __init__(self):
        super().__init__("iao_ransomware_email",
                         "iao_ransomware_email/native/stacks/docker-compose.yml")  # noqa: E501
        self.ransomware_service = iao_ransomware_email_demo.RansomwareDemo()

    def start(self, subpath, params):
        secure_mode = False
        self.set_state("starting")
        if subpath == "run_code":
            iao_ransomware_email_code.run()
        else:
            try:
                logging.info("Starting ransomware demo stack")
                self.start_container()
                iao_ransomware_email_code.prep()
                self.ransomware_service.thunderbird_init()
                self.ransomware_service.check_mail_server_online()
                self.ransomware_service.change_client_profile(secure_mode)
                self.ransomware_service.delete_mailbox()
                self.ransomware_service.send_mail_files(secure_mode)
                self.ransomware_service.start_mail_application()
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
        iao_ransomware_email_code.reset()
        self.stop_container()
        self.ransomware_service.stop_mail_application()
        self.set_state("offline")
        return demo_controller.ErrorCodes.stop_success


def get_controller():
    return RansomwareController()
