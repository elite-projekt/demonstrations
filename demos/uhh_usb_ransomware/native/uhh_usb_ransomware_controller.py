# SPDX-License-Identifier: AGPL-3.0-only

import logging

from nativeapp.config import config
from nativeapp.controller.demo_controller import (
    DemoController,
    DemoStates,
    ErrorCodes)

from demos.uhh_usb_ransomware.native import uhh_usb_ransomware_demo


class RansomwareController(DemoController):
    def __init__(self):
        super().__init__("uhh_usb_ransomware",
                         "uhh_usb_ransomware/native/stacks/docker-compose.yml")
        self.ransomware_service = uhh_usb_ransomware_demo.RansomwareDemo()

    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        if (self.get_state() != DemoStates.STOPPING and
           self.get_state() != DemoStates.OFFLINE):
            self.set_state(DemoStates.STOPPING)
            self.stop_container()
            self.ransomware_service.stop()
            self.set_state(DemoStates.OFFLINE)
        return ErrorCodes.stop_success

    def start(self, subpath, params):
        """
        Start the demo
        """
        logging.info(f"Start with {subpath=}")
        if subpath == "script_downloaded":
            logging.info("Starting ransomware")
            self.ransomware_service.ransomware()
        if self.get_state() == DemoStates.OFFLINE:
            try:
                if "language" in params:
                    config.EnvironmentConfig.LANGUAGE = params["language"]

                logging.info("Starting uhh_usb_ransomware demo stack")
                if self.get_state() != "offline":
                    return ErrorCodes.invalid_state
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_CONTAINER)
                lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
                self.start_container(lang_env)
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_APPLICATIONS)
                self.ransomware_service.start()
                self.set_state(DemoStates.READY)
            except Exception as e:
                logging.error(e)
                return ErrorCodes.no_docker_error
        return ErrorCodes.start_success

    def enter(self, subpath):
        if self.get_state() == DemoStates.READY:
            self.ransomware_service.send_mails()
            self.set_state(DemoStates.RUNNING)
        return ErrorCodes.start_success


def get_controller():
    return RansomwareController()
