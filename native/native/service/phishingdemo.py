import smtplib
import imaplib
import glob
import ssl
import email
import os, subprocess
import re
import random
import socket
import time
from python_on_whales import docker
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from python_on_whales import docker
from os import path

t_path = path.abspath(path.dirname(__file__))
email_files_location = path.join(path.dirname(path.dirname(t_path)), 'mails',)


class PhishingDemo():

    default_email_server = "localhost"  # online vm server
    default_email_account = "max.mustermann@mpseinternational.com"
    default_email_account_password = "123"

    secure_server_smtp_port = 465
    secure_server_imap_port = 143
    unsecure_server_smtp_port = 26
    unsecure_server_imap_port = 144

    email_client_config_location = os.getenv(
        'APPDATA') + r"\Thunderbird\Profiles"

    # deletes all mail in a mail box
    def delete_mailbox(self,
                       local_imap_port=secure_server_imap_port,
                       local_email_server=default_email_server,
                       local_email_account=default_email_account,
                       local_email_account_password=default_email_account_password):
        box = imaplib.IMAP4_SSL(local_email_server)
        box.login(local_email_account, local_email_account_password)
        box.select('Inbox')
        typ, data = box.search(None, 'ALL')
        for num in data[0].split():
            box.store(num, '+FLAGS', '\\Deleted')
        box.expunge()
        box.close()
        box.logout()

    # Ports to be used: secure_server_smtp_port or unsecure_server_smtp_port
    def send_mail(self, sender, password, port, recipient, message, local_server):
        print(sender, password, port, recipient, local_server)
        # Try to log in to server and send email
        server = smtplib.SMTP_SSL(local_server, port)
        try:
            # server.auth_plain()
            server.login(sender, password)
            # server.auth_plain()
            print("Sending mail from " + sender + " to " + recipient)
            server.sendmail(sender, recipient, message)
        except Exception as e:
            # Print any error messages to stdout
            print("Could not send mail. Error: " + e)
        server.close()

    # sends mails based on .txt files specified in the email_files_location-path
    def send_mail_files(self,
                        local_password=default_email_account_password,
                        local_smtp_port=secure_server_smtp_port,
                        local_server=default_email_server):
        for file in glob.glob(email_files_location + "/*.txt"):
            print('sending mail file: ' + file)
            email_file = open(file, "r")
            email_text = email_file.read()
            email_mime = email.message_from_string(email_text)

            # Extract the sender of the email
            # If the form '"name" <name@domain>' is used the raw address is extracted
            local_sender = email_mime["From"]
            local_left_bracket = local_sender.find("<")
            local_right_bracket = local_sender.find(">")
            if -1 < local_left_bracket < local_right_bracket:
                local_sender = re.split('[<>]', local_sender)[1]

            # Extract the "Sent" time from the email source
            email_date = email_mime["Date"]
            email_time = datetime.strptime(
                email_date, "%a, %d %b %Y %H:%M:%S +0100")

            # Substract one day so the sent date is yesterday
            date_object = date.today() - timedelta(days=1)
            # If more randomness in the dates is desired: timedelta(days=random.randint(1, 3))

            # Email date format "Fri, 01 Jan 2021 00:00:00 +0100"
            email_date = date_object.strftime(
                "%a, %d %b %Y " + email_time.strftime("%H:%M:%S") + " +0100")

            # Replace date in header with the newly generated datetime
            email_mime.replace_header("Date", email_date)
            email_text = email_mime.as_string()

            self.send_mail(local_sender, local_password, local_smtp_port,
                      email_mime["To"], email_text, local_server)
            email_file.close()

    def change_client_profile(self, use_secured_client=True, change_ports=False):
        """
        Changes the client configuration between a more secure and a less secure configuration
        :param use_secured_client: Which client configuration to use
        :param change_ports: Do we want to change ports in the config?
        :return:
        """
        skip = False
        for root, dirs, files in os.walk(self.email_client_config_location):
            for name in files:
                if name == "prefs.js":
                    self.email_client_config_location = (str(root) + "\\prefs.js")
                    skip = True
                    break
            if skip:
                break
        print("Use secured client: " + str(use_secured_client))
        with open(self.email_client_config_location, "r") as f:
            f_lines = f.readlines()

            # only touch port configuration if we really want to (multiple email servers with
            # different ports are not in scope of the WS20/21
            if change_ports:
                i = 0
                imap_port_set = False
                smtp_port_set = False
                while i < len(f_lines):
                    if "mail.server.server1.port" in f_lines[i] and use_secured_client:
                        f_lines[i] = f_lines[i].replace(
                            str(self.unsecure_server_imap_port), str(self.secure_server_imap_port))
                        imap_port_set = True
                    elif "mail.server.server1.port" in f_lines[i] and not use_secured_client:
                        f_lines[i] = f_lines[i].replace(
                            str(self.secure_server_imap_port), str(self.unsecure_server_imap_port))
                        imap_port_set = True
                    elif "mail.smtpserver.smtp1.port" in f_lines[i] and use_secured_client:
                        f_lines[i] = f_lines[i].replace(
                            str(self.unsecure_server_smtp_port), str(self.secure_server_smtp_port))
                        smtp_port_set = True
                    elif "mail.smtpserver.smtp1.port" in f_lines[i] and not use_secured_client:
                        f_lines[i] = f_lines[i].replace(
                            str(self.secure_server_smtp_port), str(self.unsecure_server_smtp_port))
                        smtp_port_set = True
                    i += 1

                if not imap_port_set:
                    if use_secured_client:
                        f_lines.append(
                            "user_pref(\"mail.server.server1.port\", " + str(self.secure_server_imap_port) + ");\n")
                    elif not use_secured_client:
                        f_lines.append(
                            "user_pref(\"mail.server.server1.port\", " + str(self.unsecure_server_imap_port) + ");\n")

                if not smtp_port_set:
                    if use_secured_client:
                        f_lines.append(
                            "user_pref(\"mail.server.server1.port\", " + str(self.secure_server_smtp_port) + ");\n")
                    elif not use_secured_client:
                        f_lines.append(
                            "user_pref(\"mail.server.server1.port\", " + str(self.unsecure_server_smtp_port) + ");\n")

            # user_pref("mail.phishing.detection.enabled", false);
            # user_pref("mailnews.message_display.disable_remote_image", false);
            i = 0
            phishing_detection_set = False
            remote_image_set = False
            while i < len(f_lines):
                if "mail.phishing.detection.enabled" in f_lines[i] and use_secured_client:
                    f_lines[i] = f_lines[i].replace("false", "true")
                    phishing_detection_set = True
                elif "mail.phishing.detection.enabled" in f_lines[i] and not use_secured_client:
                    f_lines[i] = f_lines[i].replace("true", "false")
                    phishing_detection_set = True
                elif "mailnews.message_display.disable_remote_image" in f_lines[i] and use_secured_client:
                    f_lines[i] = f_lines[i].replace("false", "true")
                    remote_image_set = True
                elif "mailnews.message_display.disable_remote_image" in f_lines[i] and not use_secured_client:
                    f_lines[i] = f_lines[i].replace("true", "false")
                    remote_image_set = True
                elif "mailnews.display.disallow_mime_handlers" in f_lines[i]:
                    f_lines[i] = "user_pref(\"mailnews.display.disallow_mime_handlers\", 0);\n"
                elif "mailnews.display.html_as" in f_lines[i]:
                    f_lines[i] = "user_pref(\"mailnews.display.html_as\", 0);\n"
                elif "mailnews.display.prefer_plaintext" in f_lines[i]:
                    f_lines[i] = "user_pref(\"mailnews.display.prefer_plaintext\", false);\n"
                i += 1

            if not phishing_detection_set:
                if use_secured_client:
                    f_lines.append(
                        "user_pref(\"mail.phishing.detection.enabled\", true);\n")
                elif not use_secured_client:
                    f_lines.append(
                        "user_pref(\"mail.phishing.detection.enabled\", false);\n")

            if not remote_image_set:
                if use_secured_client:
                    f_lines.append(
                        "user_pref(\"mailnews.message_display.disable_remote_image\", true);\n")
                elif not use_secured_client:
                    f_lines.append(
                        "user_pref(\"mailnews.message_display.disable_remote_image\", false);\n")

        with open(self.email_client_config_location, "w") as f:
            f.writelines(f_lines)
        return "Set client configuration to secure" if use_secured_client else "Set client configuration to unsecure"

    # Check if Mail Server Status is running
    def check_mail_server_online(self):
        delay = 10
        retries = 10
        time.sleep(delay)
        container = docker.container.inspect("phising_mailserver")

        for i in range(retries):
            if container.state.running:
                break
            else:
                time.sleep(delay)
    
    def stop_mail_application(self):
        """Close mail application
        """
        print("[ i ] - Try closing running thunderbird process...")
        try:
            res = os.system("taskkill /im thunderbird.exe")
            print("[ i ] - success!")
        except Exception as e:
            print("[ e ] - {}".format(e))
    
    def start_mail_application(self):
        """Start mail application
        """
        print("[ i ] - Try starting thunderbird process...")
        try:
            res = subprocess.Popen(['C:\\Program Files\\Mozilla Thunderbird\\thunderbird.exe'])
            print("[ i ] - success!")
        except Exception as e:
            print(e)