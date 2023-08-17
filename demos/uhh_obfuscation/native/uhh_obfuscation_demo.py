#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-only

import logging
import importlib.resources
import pathlib

from typing import List

from nativeapp.utils.mail import mail_client, mail_program
from nativeapp.utils.admin import admin_app
from nativeapp.config import config

from nativeapp.utils.locale import locale

from demos.uhh_obfuscation.native import simulate_obfuscation


class ObfuscationDemo:

    def __init__(self):
        self.email_client = mail_client.MailClient(
                "127.0.0.1",
                993,
                465,
                "max.mustermann@nimbus.de",
                "123")
        with importlib.resources.path(
                "demos.uhh_obfuscation.resources.mail",
                "mpse_profile.zip") as mail_profile:
            self.email_program = mail_program.MailProgramThunderbird(
                    "MPSE", str(mail_profile))

        self.running = False
        self.admin_client = admin_app.NativeappAdminClient()
        self.usb_monitor = None

        localedir = pathlib.Path(__file__).parent.parent / "locales"
        self.locale = locale.Locale()
        self.locale.add_locale_dir(localedir)
        self.locale.update_locale(config.EnvironmentConfig.LANGUAGE)
        self.obfuscation_simulation = simulate_obfuscation.ObfuscationSimulation(self.locale) # noqa: 501

    def start(self):
        if self.running:
            self.stop()

        # set hosts entry
        self.running = True
        self.email_program.copy_profile()

        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_REAL_TIME_MONITORING, b"1")
        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_AUTOMATIC_SAMPLE_SUBMISSION, b"1") # noqa: 501
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    True, "mail.nimbus.de", "127.0.0.1"))

        while not self.email_client.wait_for_smtp_server(20):
            pass

        while not self.email_client.wait_for_imap_server(20):
            pass

        self.email_program.start()
        self.obfuscation_simulation.prepare()

    def stop(self):
        self.running = False
        logging.info("Stopping mail program")
        self.email_program.stop()
        logging.info("reverting admin settings")
        # Enable Real Time Monitoring again
        self.admin_client.send_command(
                admin_app.NativeappCommands.ENABLE_REAL_TIME_MONITORING, b"1")
        # Enable automatic sample submission again
        self.admin_client.send_command(
                admin_app.NativeappCommands.ENABLE_AUTOMATIC_SAMPLE_SUBMISSION, b"1") # noqa: 501
        self.admin_client.send_command(
                admin_app.NativeappCommands.CLEAR_DEFENDER_HISTORY, b"1")
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    False, "mail.nimbus.de"))
        if self.usb_monitor:
            self.usb_monitor.stop()
        if self.obfuscation_simulation:
            self.obfuscation_simulation.stop()
        logging.info("Stop done")

    def obfuscation(self):
        self.obfuscation_simulation.run_obfuscation()

    def _send_mail(self, mail_files: List[str]) -> None:
        print(config.EnvironmentConfig.LANGUAGE)
        for mail_file in mail_files:
            with importlib.resources.path(
                    "demos.uhh_obfuscation.resources.mail",
                    mail_file) as mail_path:
                logging.info(f"Getting path for file {mail_file}: {mail_path}")
                self.email_client.send_mail_from_file(
                    mail_path, (0, 0), self.locale.translate)

    def send_mails(self) -> None:
        self._send_mail(["pictures.yml"])
