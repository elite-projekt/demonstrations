import datetime
import email
import glob
import imaplib
import logging
import os
import re
import smtplib
import subprocess
import time
import zipfile

import python_on_whales

from native.src.config import config


class PhishingDemo:
    default_email_server = "localhost"  # online vm server
    default_email_account = "max.mustermann@mpseinternational.com"
    default_email_account_password = "123"  # nosec This Password is only used
    # for the local Mail Server and is needed for the communication with
    # this Server

    secure_server_smtp_port = 465
    secure_server_imap_port = 143
    unsecure_server_smtp_port = 26
    unsecure_server_imap_port = 144

    email_client_config_location = os.getenv(
        "APPDATA") + r"\Thunderbird\Profiles"

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
    def send_mail(self, sender, password, port, recipient, message,
                  local_server):
        # Try to log in to server and send email
        server = smtplib.SMTP_SSL(local_server, port)
        try:
            # server.auth_plain()
            server.login(sender, password)
            # server.auth_plain()
            logging.info("Sending mail from {} to {}".format(sender,
                                                             recipient))
            server.sendmail(sender, recipient, message)
        except Exception as e:
            logging.error(e)
        server.close()

    # sends mails based on .txt files specified in the
    # email_files_location-path
    def send_mail_files(
            self,
            use_secured_client=True,
            local_password=default_email_account_password,
            local_smtp_port=secure_server_smtp_port,
            local_server=default_email_server,
    ):
        logging.info(
            "Checking for mails in: {}".format(
                config.EnvironmentConfig.DOCKERSTACKDIR + "phishing\\mails\\"
            )
        )
        for file in glob.glob(
                config.EnvironmentConfig.DOCKERSTACKDIR + "phishing\\mails\\"
                + "/*.txt"
        ):
            # print('sending mail file: ' + file)
            logging.info("Sending mail file: {}".format(file))
            email_file = open(file, "r")
            email_text = email_file.read()
            email_mime = email.message_from_string(email_text)

            # check if secure mode, if no do not process smime mails
            if not use_secured_client:
                if "Content-Type: multipart/signed;" in email_text:
                    continue

            # Extract the sender of the email
            # If the form '"name" <name@domain>' is used the raw address is
            # extracted
            local_sender = email_mime["From"]
            local_left_bracket = local_sender.find("<")
            local_right_bracket = local_sender.find(">")
            if -1 < local_left_bracket < local_right_bracket:
                local_sender = re.split("[<>]", local_sender)[1]

            # Extract the "Sent" time from the email source
            email_date = email_mime["Date"]
            email_time = datetime.datetime.strptime(email_date,
                                                    "%a, %d %b %Y %H:%M:%S "
                                                    "+0100")

            # Substract one day so the sent date is yesterday
            date_object = datetime.date.today() - datetime.timedelta(days=1)
            # If more randomness in the dates is desired:
            # timedelta(days=random.randint(1, 3))

            # Email date format "Fri, 01 Jan 2021 00:00:00 +0100"
            email_date = date_object.strftime(
                "%a, %d %b %Y " + email_time.strftime("%H:%M:%S") + " +0100"
            )

            # Replace date in header with the newly generated datetime
            email_mime.replace_header("Date", email_date)
            email_text = email_mime.as_string()

            self.send_mail(
                local_sender,
                local_password,
                local_smtp_port,
                email_mime["To"],
                email_text,
                local_server,
            )
            email_file.close()

    def change_client_profile(self, use_secured_client=True,
                              change_ports=False):
        """
        Changes the client configuration between a more secure and a less
        secure configuration
        :param use_secured_client: Which client configuration to use
        :param change_ports: Do we want to change ports in the config?
        :return:
        """
        skip = False
        for root, dirs, files in os.walk(self.email_client_config_location):
            for name in files:
                if name == "prefs.js":
                    self.email_client_config_location = str(root) \
                                                        + "\\prefs.js"
                    skip = True
                    break
            if skip:
                break

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
                "phising_mailserver")
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
            subprocess.check_output(
                ["taskkill", "/f", "/im", "thunderbird.exe"]
            )
            logging.info("Success")
        except Exception as e:
            logging.error(e)

    def start_mail_application(self):
        """Start mail application"""
        logging.info("Try starting thunderbird process...")
        try:
            subprocess.check_output(
                ["C:\\Program Files\\Mozilla Thunderbird\\thunderbird.exe"]
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
            if os.path.isdir(
                    os.getenv(
                        "APPDATA") + r"\Thunderbird\Profiles\jzou4lhc.MPSE"
            ):
                logging.info("Nothing to do, exiting init")
                return

            profile_location = os.getenv("APPDATA") + r"\Thunderbird"
            profile_zip = config.EnvironmentConfig.PROFILEDIR + "profile.zip"

            # extract profile to location => overrides existing files
            with zipfile.ZipFile(profile_zip, "r") as zipObj:
                zipObj.extractall(profile_location)

            logging.info("Init done")
        except Exception as e:
            logging.error(e)
