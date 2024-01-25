# SPDX-License-Identifier: AGPL-3.0-only

import logging
import flask
import pathlib
import fitz
import importlib.resources
import urllib
import time
import threading
from subprocess import Popen, PIPE  # nosec

from typing import List

from nativeapp.config import config
from nativeapp.controller.demo_controller import (
    DemoController,
    DemoStates,
    ErrorCodes)
from nativeapp.utils.mail import mail_client, mail_program
from nativeapp.utils.locale import locale


class PrinterController(DemoController):
    def __init__(self):
        super().__init__("uhh_hda_printer_demo",
                         "uhh_hda_printer_demo/native/stacks/docker-compose.yml")  # noqa: 501
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
        self.email_program = mail_program.MailProgramThunderbird(
                "MPSE", mail_profile)
        localedir = pathlib.Path(__file__).parent.parent / "locales"
        self.locale = locale.Locale()
        self.locale.add_locale_dir(localedir)

    def stop(self, subpath) -> int:
        """
        Stops the demo
        """
        self.stop_container()
        self.set_state(DemoStates.OFFLINE)
        logging.info("Stopping mail program")
        self.email_program.stop()
        return ErrorCodes.stop_success

    def start(self, subpath, params):
        """
        Start the demo
        """
        logging.info(f"Start with {subpath=}")
        if subpath == "print_job":
            logging.info(f"Got print job file {params=}")
            logging.info(f"Flask request {flask.request.files=}")
            if 'file' in flask.request.files:
                received_pdf = flask.request.files['file']
                logging.info(f"{received_pdf}")
                # XXX: Sorry I am lazy right now
                received_pdf.save("printed.pdf")
                doc = fitz.open("printed.pdf")

                search_text = "IBAN: DE12 3456 0123 4560 00"
                replace_text = "IBAN: DE66 7777 8888 9999 99"
                for page in doc:
                    # TODO: extract correct font
                    # fonts = page.get_fonts()
                    # list of rectangles where to replace
                    hits = page.search_for(search_text)

                    for rect in hits:
                        page.add_redact_annot(rect, replace_text,
                                              fontname="helv",
                                              fontsize=11,
                                              align=fitz.TEXT_ALIGN_LEFT)
                    # don't touch images
                    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
                doc.save("rechnung.pdf", garbage=3, deflate=True)
                message = self.email_client.get_message(
                        "uhh_hda_second_mail_subject",
                        "uhh_hda_printer_email_name",
                        "uhh_hda_printer_email_address",
                        "Max", "max.mustermann@nimbus.de",
                        "uhh_hda_second_mail_content", "rechnung.pdf",
                        self.locale.translate)

                self.email_client.send_mail(message,
                                            "max.mustermann@nimbus.de")
                self.send_attacked_mails()
        if self.get_state() == DemoStates.OFFLINE:
            try:
                if "language" in params:
                    config.EnvironmentConfig.LANGUAGE = params["language"]
                self.locale.update_locale(config.EnvironmentConfig.LANGUAGE)

                logging.info("Starting uhh_hda_printer demo stack")
                if self.get_state() != "offline":
                    return ErrorCodes.invalid_state
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_CONTAINER)
                lang_env = {"ELITE_LANG": config.EnvironmentConfig.LANGUAGE}
                self.start_container(lang_env)
                self.set_state(DemoStates.STARTING,
                               DemoStates.STARTING_APPLICATIONS)
                self.email_program.copy_profile()

                while not self.email_client.wait_for_smtp_server(20):
                    pass

                while not self.email_client.wait_for_imap_server(20):
                    pass

                self.email_program.start()

                self.add_printer()

                self.set_state(DemoStates.READY)
            except Exception as e:
                logging.error(e)
                return ErrorCodes.no_docker_error
        return ErrorCodes.start_success

    def enter(self, subpath):
        self.set_state(DemoStates.RUNNING)
        self._send_mail(["first_mail.yml"])
        return ErrorCodes.start_success

    def _send_mail(self, mail_files: List[str]) -> None:
        print(config.EnvironmentConfig.LANGUAGE)
        for mail_file in mail_files:
            with importlib.resources.path(
                    "demos.uhh_hda_printer_demo.resources.mail",
                    mail_file) as mail_path:
                logging.info(f"Getting path for file {mail_file}: {mail_path}")
                self.email_client.send_mail_from_file(mail_path, (0, 0),
                                                      self.locale.translate)

    def add_printer(self):
        printer_url = "http://localhost:631/printers/email-sample"
        while True:
            try:
                resp = urllib.request.urlopen(printer_url)  # nosec
                if 200 <= resp.getcode() < 300:
                    logging.info("Website online!")
                    # Sleep just in case. For whatever reason there is no force
                    # parameter for Add-Printer. So the printer has to be
                    # online when we add one. So stupid

                    time.sleep(3)
                    # Website is online -> break loop
                    break
            except Exception:
                pass

        # Since windows is really stupid "Add-Printer" is not an executable
        # like on sane operating systems, but a powershell specific command. So
        # we have to call powershell first. Just wow...
        cmd = ["powershell", "-command",
               f"Add-Printer -Name Printer -DriverName 'Microsoft IPP Class Driver' -PortName '{printer_url}'"]  # noqa: 501
        logging.info("Calling {}".format(" ".join(cmd)))
        call_cmd(cmd)

    def send_attacked_mails(self) -> None:
        threading.Timer(5.0, self._send_mail,
                        args=[["iban_fraud.yml"]]).start()
        threading.Timer(15.0, self._send_mail,
                        args=[["boss.yml"]]).start()
        threading.Timer(30.0, self._send_mail,
                        args=[["it_admin.yml"]]).start()
        threading.Timer(40.0, self._send_mail,
                        args=[["boss_second.yml"]]).start()


def call_cmd(command_list: List[str],
             workdir: pathlib.Path = None,
             shell=False):
    with Popen(  # nosec
            command_list, stdout=PIPE, cwd=workdir, shell=shell) as process:
        logging.info(process.communicate())


def get_controller():
    return PrinterController()
