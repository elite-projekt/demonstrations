#!/usr/bin/env python3

# SPDX-License-Identifier: AGPL-3.0-only

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
                "max.mustermann@nimbus.de",
                "123")
        with importlib.resources.path(
                "demos.uhh_usb_kill.resources.mail",
                "mpse_profile.zip") as mail_profile:
            self.email_program = mail_program.MailProgramThunderbird(
                    "MPSE", str(mail_profile))

        self.running = False
        self.admin_client = admin_app.NativeappAdminClient()
        self.kill_thread = None
        self.usb_monitor = None

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
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    True, "mail.nimbus.de", "127.0.0.1"))

        while not self.email_client.wait_for_smtp_server(20):
            pass

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
        if self.usb_monitor:
            self.usb_monitor.stop()
        if self.kill_thread:
            self.kill_thread.join()
        logging.info("Stop done")

    def kill(self, usb_info):
        def kill_thread_func():
            self.kill_simulation = simulate_kill.KillSimulation()
            sequences = [
                    (self.kill_simulation.show_glitch, 5000),
                    (self.kill_simulation.show_crash, 5000),
                    (self.kill_simulation.show_glitch, 5000),
                    (self.kill_simulation.show_crash, 5000),
                        ]
            for func, wait_time in sequences:
                func()
                time_waited_ms = 0
                while time_waited_ms < wait_time:
                    # Use small sleep to be interuptable
                    time.sleep(0.1)
                    time_waited_ms += 100

            self.kill_simulation.show_crash_text()

        self.kill_thread = threading.Thread(target=kill_thread_func)
        self.kill_thread.start()

    def _send_mail(self, mail_files: List[str]) -> None:
        print(config.EnvironmentConfig.LANGUAGE)
        for mail_file in mail_files:
            with importlib.resources.path(
                    "demos.uhh_usb_kill.resources.mail",
                    mail_file) as mail_path:
                logging.info(f"Getting path for file {mail_file}: {mail_path}")
                self.email_client.send_mail_from_file(mail_path, (0, 0), _)

    def send_mails(self) -> None:
        self._send_mail(["pictures.yml"])
