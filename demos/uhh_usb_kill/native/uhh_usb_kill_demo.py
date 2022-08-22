#!/usr/bin/env python3
"""
Copyright (C) 2022 Kevin Köster

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import time
import importlib.resources
import gettext
import pathlib
import threading

from typing import List

from nativeapp.utils.mail import mail_client, mail_program
from nativeapp.utils.admin import admin_app
from nativeapp.utils.usb import usb_monitor
from nativeapp.config import config

from demos.uhh_usb_kill.native import simulate_kill


def update_locale():
    global _
    localedir = pathlib.Path(__file__).parent.parent / "locales"
    lang = gettext.translation("base",
                               localedir=localedir.absolute(),
                               languages=[config.EnvironmentConfig.LANGUAGE])
    lang.install()
    _ = lang.gettext


update_locale()


class KillDemo:

    def __init__(self):
        self.email_client = mail_client.MailClient(
                "127.0.0.1",
                993,
                465,
                "max.mustermann@mpseinternational.com",
                "123")
        mail_profile = importlib.resources.path(
                "demos.uhh_usb_kill.resources.mail", "mpse_profile.zip")
        self.email_program = mail_program.MailProgramThunderbird(
                "MPSE", mail_profile)

        self.running = False
        self.admin_client = admin_app.NativeappAdminClient()

    def start(self):
        if self.running:
            self.stop()
        update_locale()

        # set hosts entry
        self.running = True
        self.email_program.copy_profile()
        self.usb_monitor = usb_monitor.USBMonitor(on_connect=self.kill)

        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"1")

        while not self.email_client.wait_for_smtp_server(20):
            pass
        self.send_mails()

        while not self.email_client.wait_for_imap_server(20):
            pass

        self.email_program.start()

    def stop(self):
        self.running = False
        logging.info("Stopping mail program")
        self.email_program.stop()
        logging.info("reverting admin settings")
        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"0")
        self.usb_monitor.stop()
        self.kill_thread.join()
        logging.info("Stop done")

    def kill(self):
        def kill_thread_func():
            self.kill_simulation = simulate_kill.KillSimulation()
            self.kill_simulation.show_glitch()
            time_waited_ms = 0
            while time_waited_ms < 5000:
                time.sleep(0.1)
                time_waited_ms += 100
            self.kill_simulation.show_crash()
            while time_waited_ms < 10000:
                time.sleep(0.1)
                time_waited_ms += 100
            self.kill_simulation.show_crash_text()

        self.kill_thread = threading.Thread(target=kill_thread_func)
        self.kill_thread.start()

    def _send_mail(self, mail_files: List[str]) -> None:
        print(config.EnvironmentConfig.LANGUAGE)
        for mail_file in mail_files:
            mail_path = (importlib.resources.path(
                "demos.uhh_usb_kill.resources.mail", mail_file))
            logging.info(f"Getting path for file {mail_file}: {mail_path}")
            self.email_client.send_mail_from_file(mail_path, (0, 0), _)

    def send_mails(self) -> None:
        self._send_mail(["pictures.yml"])
