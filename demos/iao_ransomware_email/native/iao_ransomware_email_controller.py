import logging

from nativeapp.controller import demo_controller
from demos.iao_ransomware_email.native import iao_ransomware_email_code, iao_ransomware_email_demo  # noqa: E501
from nativeapp.config import config
from nativeapp.controller.demo_controller import (
    DemoStates,
    ErrorCodes)


class RansomwareController(demo_controller.DemoController):
    def __init__(self):
        super().__init__("iao_ransomware_email",
                         "iao_ransomware_email/native/stacks/docker-compose.yml")  # noqa: E501
        self.ransomware_service = iao_ransomware_email_demo.RansomwareDemo()

    def start(self, subpath, params):
        secure_mode = False
        if subpath == "run_code":
            iao_ransomware_email_code.run()
        else:
            try:
                logging.info("Starting ransomware demo stack")
                if "language" in params:
                    config.EnvironmentConfig.LANGUAGE = params["language"]
                lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
                self.set_state(DemoStates.STARTING)
                self.start_container(lang_env)
                iao_ransomware_email_code.prep()
                self.ransomware_service.check_mail_server_online()
                self.ransomware_service.copy_client_profile()
                self.ransomware_service.delete_mailbox()
                self.ransomware_service.send_mail_files(secure_mode)
                self.set_state(DemoStates.READY)
            except Exception as e:
                logging.error(e)
                self.set_state(DemoStates.ERROR)
                return demo_controller.ErrorCodes.no_docker_error
        return demo_controller.ErrorCodes.start_success

    def stop(self, subpath):
        self.set_state(DemoStates.STOPPING)
        iao_ransomware_email_code.reset()
        try:
            self.stop_container()
        except Exception as e:
            print(e)
        self.ransomware_service.stop_mail_application()
        self.ransomware_service.kill_processes_restore()
        self.set_state(DemoStates.OFFLINE)
        return demo_controller.ErrorCodes.stop_success

    def enter(self, subpath):
        if self.get_state() == DemoStates.READY:
            self.ransomware_service.email_program.start()
            self.set_state(DemoStates.RUNNING)
        return ErrorCodes.start_success


def get_controller():
    return RansomwareController()
