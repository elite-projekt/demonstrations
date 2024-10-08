import configparser
import imaplib
import logging
import os
import shutil
import smtplib
# We need this module and the severity is low. See also:
# https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html#b404-import-subprocess
import subprocess  # nosec
import time
import zipfile
import pathlib
import tempfile
from nativeapp.utils.admin import admin_app


import python_on_whales

from nativeapp.config import config
from importlib_resources import files
from nativeapp.utils.mail import mail_client, mail_program
from nativeapp.utils.locale import locale
import importlib.resources


class RansomwareDemo:
    email_client = mail_client.MailClient(
        "127.0.0.1",
        993,
        465,
        "max.mustermann@nimbus.de",
        "123")
    default_email_profile = "jzou4lhc.MPSE"  # name of custom profile
    default_email_server = "localhost"  # online vm server
    default_email_account = "max.mustermann@nimbus.de"
    default_email_account_password = "123"  # nosec This Password is only used
    # for the local Mail Server and is needed for the communication with
    # this Server

    secure_server_smtp_port = 465
    secure_server_imap_port = 143
    unsecure_server_smtp_port = 26
    unsecure_server_imap_port = 144

    profile_dir = pathlib.Path(os.getenv("APPDATA")) / \
        "Thunderbird/Profiles"

    with importlib.resources.path(
        "demos.iao_ransomware_email.native.profiles",
            "mpse_profile.zip") as mail_profile:
        email_program = mail_program.MailProgramThunderbird(
            "MPSE", mail_profile)

    localedir = pathlib.Path(__file__).parent.parent / "locales"
    locale = locale.Locale()
    locale.add_locale_dir(localedir)
    admin_client = admin_app.NativeappAdminClient()

    email_client_config_location = profile_dir / \
        f"{default_email_profile}/prefs.js"

    def prep_domainname(self):
        self.admin_client.send_command(
            admin_app.NativeappCommands.SET_REDIRECT,
            admin_app.create_host_payload(
                True, "mail.nimbus.de", "127.0.0.1"))

    # deletes all mail in a mail box
    def delete_mailbox(
        self,
        local_imap_port=secure_server_imap_port,
        local_email_server=default_email_server,
        local_email_account=default_email_account,
        local_email_account_password=default_email_account_password,
    ):
        box = imaplib.IMAP4_SSL(local_email_server)
        box.login(local_email_account, local_email_account_password)
        box.select("Inbox")
        typ, data = box.search(None, "ALL")
        for num in data[0].split():
            box.store(num, "+FLAGS", "\\Deleted")
        box.expunge()
        box.close()
        box.logout()

    # Ports to be used: secure_server_smtp_port or unsecure_server_smtp_port
    def send_mail(self, message):
        # Try to log in to server and send email
        server = smtplib.SMTP_SSL(self.default_email_server,
                                  self.secure_server_smtp_port)
        try:
            # bare address of user in format: user@domain.com
            sender = message["to"].addresses[0].addr_spec
            server.login(sender, self.default_email_account_password)
            logging.info("Sending mail from {} to {}".format(sender,
                                                             message["to"]))
            server.sendmail(sender, message["to"], message.as_bytes())
        except Exception as e:
            logging.error(e)
        server.close()

    def copy_client_profile(self):
        self.email_program.copy_profile()

        while not self.email_client.wait_for_smtp_server(20):
            pass

        while not self.email_client.wait_for_imap_server(20):
            pass

    # sends mails based on *.txt files specified in the
    # email_files_location-path
    def send_mail_files(self, use_secured_client=True):

        if (config.EnvironmentConfig.LANGUAGE == "de"):
            import demos.iao_ransomware_email.native.emails.de as mails
        else:
            import demos.iao_ransomware_email.native.emails.en as mails

        email_files = [
            "mail.yml"
            # "nina_signed.txt" unused due to invalid smime signature
        ]

        logging.info(
            "Checking for mails in: {}".format(email_files)
        )

        for email_filename in email_files:
            logging.info("Sending mail file: {}".format(email_filename))
            filename = files(mails).joinpath(email_filename)
            self.email_client.send_mail_from_file(filename)

    def change_client_profile(self, use_secured_client=True,
                              change_ports=False):
        """
        Changes the client configuration between a more secure and a less
        secure configuration
        :param use_secured_client: Which client configuration to use
        :param change_ports: Do we want to change ports in the config?
        :return:
        """

        logging.info("Use secure client: {}".format(use_secured_client))
        with open(self.email_client_config_location, "r") as f:
            logging.info("Loading email client configuration")
            f_lines = f.readlines()

            # only touch port configuration if we really want to (multiple
            # email servers with
            # different ports are not in scope of the WS20/21
            if change_ports:
                i = 0
                imap_port_set = False
                smtp_port_set = False
                while i < len(f_lines):
                    if "mail.server.server1.port" in f_lines[i] \
                            and use_secured_client:
                        f_lines[i] = f_lines[i].replace(
                            str(self.unsecure_server_imap_port),
                            str(self.secure_server_imap_port),
                        )
                        imap_port_set = True
                    elif (
                            "mail.server.server1.port" in f_lines[i]
                            and not use_secured_client
                    ):
                        f_lines[i] = f_lines[i].replace(
                            str(self.secure_server_imap_port),
                            str(self.unsecure_server_imap_port),
                        )
                        imap_port_set = True
                    elif (
                            "mail.smtpserver.smtp1.port" in f_lines[i]
                            and use_secured_client
                    ):
                        f_lines[i] = f_lines[i].replace(
                            str(self.unsecure_server_smtp_port),
                            str(self.secure_server_smtp_port),
                        )
                        smtp_port_set = True
                    elif (
                            "mail.smtpserver.smtp1.port" in f_lines[i]
                            and not use_secured_client
                    ):
                        f_lines[i] = f_lines[i].replace(
                            str(self.secure_server_smtp_port),
                            str(self.unsecure_server_smtp_port),
                        )
                        smtp_port_set = True
                    i += 1

                if not imap_port_set:
                    if use_secured_client:
                        f_lines.append(
                            'user_pref("mail.server.server1.port", '
                            + str(self.secure_server_imap_port)
                            + ");\n"
                        )
                    elif not use_secured_client:
                        f_lines.append(
                            'user_pref("mail.server.server1.port", '
                            + str(self.unsecure_server_imap_port)
                            + ");\n"
                        )

                if not smtp_port_set:
                    if use_secured_client:
                        f_lines.append(
                            'user_pref("mail.server.server1.port", '
                            + str(self.secure_server_smtp_port)
                            + ");\n"
                        )
                    elif not use_secured_client:
                        f_lines.append(
                            'user_pref("mail.server.server1.port", '
                            + str(self.unsecure_server_smtp_port)
                            + ");\n"
                        )

            # user_pref("mail.phishing.detection.enabled", false);
            # user_pref("mailnews.message_display.disable_remote_image",
            # false);
            i = 0
            phishing_detection_set = False
            remote_image_set = False
            while i < len(f_lines):
                if (
                        "mail.phishing.detection.enabled" in f_lines[i]
                        and use_secured_client
                ):
                    f_lines[i] = f_lines[i].replace("false", "true")
                    phishing_detection_set = True
                elif (
                        "mail.phishing.detection.enabled" in f_lines[i]
                        and not use_secured_client
                ):
                    f_lines[i] = f_lines[i].replace("true", "false")
                    phishing_detection_set = True
                elif (
                        "mailnews.message_display.disable_remote_image" in
                        f_lines[i]
                        and use_secured_client
                ):
                    f_lines[i] = f_lines[i].replace("false", "true")
                    remote_image_set = True
                elif (
                        "mailnews.message_display.disable_remote_image" in
                        f_lines[i]
                        and not use_secured_client
                ):
                    f_lines[i] = f_lines[i].replace("true", "false")
                    remote_image_set = True
                elif "mailnews.display.disallow_mime_handlers" in f_lines[i]:
                    f_lines[i] = 'user_pref("mailnews.display' \
                                 '.disallow_mime_handlers", 0);\n'
                elif "mailnews.display.html_as" in f_lines[i]:
                    f_lines[i] = 'user_pref("mailnews.display.html_as", 0);\n'
                elif "mailnews.display.prefer_plaintext" in f_lines[i]:
                    f_lines[i] = 'user_pref("mailnews.display' \
                                 '.prefer_plaintext", false);\n'
                i += 1

            if not phishing_detection_set:
                if use_secured_client:
                    f_lines.append(
                        'user_pref("mail.phishing.detection.enabled", true);\n'
                    )
                elif not use_secured_client:
                    f_lines.append(
                        'user_pref("mail.phishing.detection.enabled", '
                        'false);\n')

            if not remote_image_set:
                if use_secured_client:
                    f_lines.append(
                        'user_pref("mailnews.message_display'
                        '.disable_remote_image", true);\n'
                    )
                elif not use_secured_client:
                    f_lines.append(
                        'user_pref("mailnews.message_display'
                        '.disable_remote_image", false);\n'
                    )

        with open(self.email_client_config_location, "w") as f:
            f.writelines(f_lines)
        return (
            "Set client configuration to secure"
            if use_secured_client
            else "Set client configuration to unsecure"
        )

    # Check if Mail Server Status is running
    def check_mail_server_online(self):
        """Checks if the mailserver docker container is up"""
        delay = 10
        retries = 10
        time.sleep(delay)
        try:
            container = python_on_whales.docker.container.inspect(
                "ransomware_mailserver")
            for i in range(retries):
                logging.info(
                    "Checking if mailserver reachable try: {}".format(i + 1))
                if container.state.running:
                    time.sleep(5)  # workaround for slow HW
                    break
                else:
                    time.sleep(delay)
        except Exception as e:
            logging.error(e)

    def stop_mail_application(self):
        """Close mail application"""
        logging.info("Try closing running thunderbird process...")
        try:
            # False positive. See also:
            # https://github.com/PyCQA/bandit/issues/333#issuecomment-404103697
            subprocess.Popen(  # nosec
                ["C:\\Windows\\System32\\taskkill.exe", "/f", "/im",
                 "thunderbird.exe"],
                stdout=subprocess.PIPE, shell=False
            )
            logging.info("Success")
        except Exception as e:
            logging.error(e)

    def start_mail_application(self):
        """Start mail application"""
        logging.info("Try starting thunderbird process...")
        try:
            # False positive. See also:
            # https://github.com/PyCQA/bandit/issues/333#issuecomment-404103697
            subprocess.Popen(  # nosec
                ["C:\\Program Files\\Mozilla Thunderbird\\thunderbird.exe",
                 "-P", "MPSE"], shell=False
            )
            logging.info("Success")
        except Exception as e:
            logging.error(e)

    def thunderbird_init(self):
        """Initializes thunderbird with a predefined profile with already set
        up config, if not already present"""
        logging.info("Thunderbird init")
        # check if profile already present
        try:
            if (self.profile_dir / self.default_email_profile).is_dir():
                logging.info("Nothing to do, exiting init")
                return
            # extract profile to location
            import demos.phishing.native.profiles as profiles
            filename = files(profiles).joinpath("profile.zip")
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(filename, mode="r") as zipObj:
                    zipObj.extractall(temp_dir)

                extracted_profile = pathlib.Path(temp_dir) / \
                    "Profiles" / \
                    self.default_email_profile
                shutil.copytree(extracted_profile,
                                self.profile_dir / self.default_email_profile)

            profile_ini_location = self.profile_dir.parent / "profiles.ini"

            config_parser = configparser.ConfigParser()

            # Needs to do it this, else the key values of config are converted
            # complete to lowercase characters
            config_parser.optionxform = str

            config_parser.read(profile_ini_location)

            max_profile_number = -1
            for key in config_parser.sections():
                if key.startswith("Profile"):
                    current_profile_number \
                        = int("".join(filter(str.isdigit, key)))
                    if max_profile_number < current_profile_number:
                        max_profile_number = current_profile_number

            config_parser[f"Profile{max_profile_number + 1}"] = {
                'Name': 'MPSE',
                'IsRelative': 1,
                'Path': 'Profiles/' + self.default_email_profile
            }

            with open(profile_ini_location, 'w') as config_file:
                config_parser.write(config_file, space_around_delimiters=False)

            logging.info("Init done")
        except Exception as e:
            logging.error(e)

    def stop_excel_application(self):
        """Close excel application"""
        logging.info("Try closing running excel process...")
        try:
            # False positive. See also:
            # https://github.com/PyCQA/bandit/issues/333#issuecomment-404103697
            subprocess.Popen(  # nosec
                ["C:\\Windows\\System32\\taskkill.exe", "/f", "/im",
                 "excel.exe"],
                stdout=subprocess.PIPE, shell=False
            )
            logging.info("Success")
        except Exception as e:
            logging.error(e)

    def kill_processes_restore(self):
        process_list = ["notepad.exe", "winword.exe",
                        "excel.exe", "powerpnt.exe"]
        for process in process_list:
            subprocess.Popen(  # nosec
                ['C:\\Windows\\System32\\taskkill.exe', '/f', '/im',
                 process], shell=False
            )
        self.admin_client.send_command(
            admin_app.NativeappCommands.SET_REDIRECT,
            admin_app.create_host_payload(
                 False, "mail.nimbus.de"))
        time.sleep(1)
