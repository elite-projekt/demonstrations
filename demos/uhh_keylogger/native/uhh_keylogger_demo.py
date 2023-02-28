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
import importlib.resources
import pathlib
import threading
from keyboard import unhook_all

from typing import List

from nativeapp.utils.mail import mail_client, mail_program
from nativeapp.utils.browser import browser_program
from nativeapp.utils.admin import admin_app
from nativeapp.config import config

from nativeapp.utils.locale import locale

from demos.uhh_keylogger.native import simulate_keylogger


class KeyloggerDemo:

    def __init__(self):
        self.email_client = mail_client.MailClient(
                "127.0.0.1",
                993,
                465,
                "max.mustermann@nimbus.de",
                "123")
        with importlib.resources.path(
            "demos.uhh_keylogger.resources.mail",
                "mpse_profile.zip") as mail_profile:
            self.email_program = mail_program.MailProgramThunderbird(
                "MPSE", str(mail_profile))

        with importlib.resources.path(
                "demos.uhh_ducky_mitm.resources.edge",
                "profile_uhh.zip") as browser_profile:
            self.browser_program = browser_program.BrowserProgramEdge(
                "elite.uhh_mitm", browser_profile)

        self.stop_event = threading.Event()
        self.running = False
        self.admin_client = admin_app.NativeappAdminClient()

        localedir = pathlib.Path(__file__).parent.parent / "locales"
        self.locale = locale.Locale()
        self.locale.add_locale_dir(localedir)
        self.keylog_simulation = None

    def execute(self):
        if self.keylog_simulation:
            self.keylog_simulation.execute()

    # Set the hosts entry
    def prepare(self):
        # get wsl ip
        ip = "127.0.0.1"

        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"1")
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    True, "mail.nimbus.de", "127.0.0.1"))
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    True, "nimbus.de", f"{ip}"))

    def start(self):
        if self.running:
            self.stop()
        self.locale.update_locale(config.EnvironmentConfig.LANGUAGE)

        # set hosts entry
        self.running = True
        self.email_program.copy_profile()
        self.browser_program.copy_profile()
        self.browser_program.set_default()

        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"1")

        self.stop_event.clear()
        self.keylog_simulation = simulate_keylogger.Keylog_Simulation(
                self.stop_event, self.locale)

        while not self.email_client.wait_for_smtp_server(20):
            pass

        while not self.email_client.wait_for_imap_server(20):
            pass

        self.email_program.start()

    def stop(self):
        self.running = False
        logging.info("Stopping mail program")
        self.email_program.stop()
        self.browser_program.stop()
        logging.info("reverting admin settings")
        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"0")
        self.stop_event.set()
        self.keylog_thread.join()
        unhook_all()
        logging.info("Stop done")

    def keylog(self):
        def keylog_thread_func():
            self.keylog_simulation._run()

        self.keylog_thread = threading.Thread(target=keylog_thread_func)
        self.keylog_thread.start()

    def _send_mail(self, mail_files: List[str]) -> None:
        print(config.EnvironmentConfig.LANGUAGE)
        for mail_file in mail_files:
            with importlib.resources.path(
                "demos.uhh_keylogger.resources.mail",
                    mail_file) as mail_path:
                logging.info(
                    f"Getting path for file {mail_file}: {mail_path}")
                self.email_client.send_mail_from_file(
                    mail_path, (0, 0), self.locale.translate)

    def send_mails(self) -> None:
        self._send_mail(["erinnerung.yml"])
