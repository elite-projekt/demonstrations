# SPDX-License-Identifier: AGPL-3.0-only

import logging

from nativeapp.config import config
from nativeapp.controller.demo_controller import (
    DemoController,
    DemoStates,
    ErrorCodes)

from demos.uhh_obfuscation.native import uhh_obfuscation_demo


class ObfuscationController(DemoController):
    def __init__(self):
        super().__init__("uhh_obfuscation",
                         "uhh_obfuscation/native/stacks/docker-compose.yml")
        self.obfuscation_service = uhh_obfuscation_demo.ObfuscationDemo()

    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        if (self.get_state() != DemoStates.STOPPING and
           self.get_state() != DemoStates.OFFLINE):
            self.set_state(DemoStates.STOPPING)
            self.stop_container()
            self.obfuscation_service.stop()
            self.set_state(DemoStates.OFFLINE)
        return ErrorCodes.stop_success

    def start(self, subpath, params):
        """
        Start the demo
        """
        logging.info(f"Start with {subpath=}")
        if subpath == "script_downloaded":
            logging.info("Starting obfuscation")
        # Copy Ransomware to Desktop
        if subpath == "copy_ransomware":
            self.obfuscation_service.obfuscation_simulation.copy_ransomware()
        if subpath == "scan_ransomware":
            self.obfuscation_service.obfuscation_simulation.scan_ransomware()
        self.obfuscation_service.obfuscation()
        if self.get_state() == DemoStates.OFFLINE:
            try:
                if "language" in params:
                    config.EnvironmentConfig.LANGUAGE = params["language"]

                logging.info("Starting uhh_obfuscation demo stack")
                if self.get_state() != "offline":
                    return ErrorCodes.invalid_state
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_CONTAINER)
                lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
                self.start_container(lang_env)
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_APPLICATIONS)
                self.obfuscation_service.start()
                self.set_state(DemoStates.READY)
            except Exception as e:
                logging.error(e)
                return ErrorCodes.no_docker_error
        return ErrorCodes.start_success

    def enter(self, subpath):
        if self.get_state() == DemoStates.READY:
            self.obfuscation_service.send_mails()
            self.set_state(DemoStates.RUNNING)
        return ErrorCodes.start_success

    def get_data(self, subpath):
        ret_val = {}
        if subpath == "translations":
            locale = self.obfuscation_service.locale
            locale_strings = ["obf_title",
                              "obf_desc",
                              "obf_obf_btn",
                              "obf_scan_btn",
                              "obf_theme_btn",
                              "obf_success_header",
                              "obf_success_txt",
                              "dead_code_insertion",
                              "instruction_substitution",
                              "subroutine_reordering",
                              "conditional_obfuscation",
                              "ai_assisted",
                              "environmental_awareness",
                              "packing",
                              "decrypting",
                              "obf_progress_1",
                              "obf_progress_2",
                              "obf_starting_scan",
                              "obf_scan"]
            translation_dict = {s: locale.translate(s) for s in locale_strings}
            ret_val = {"translations": translation_dict}
        return ret_val


def get_controller():
    return ObfuscationController()
