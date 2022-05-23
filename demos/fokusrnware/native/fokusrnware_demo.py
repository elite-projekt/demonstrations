import configparser
import ctypes
import datetime
import glob
import imaplib
import logging
import os
import shutil
import smtplib
# We need this module and the severity is low. See also:
# https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html#b404-import-subprocess
import subprocess  # nosec
import time
import win32con
import zipfile


import python_on_whales

from nativeapp.config import config
from importlib_resources import files
from demos.fokusrnware.native.ransomware.Controller import Controller

global original_wallpaper


class fokusrnwareDemo:
    default_email_profile = "jzou4lhc.MPSE"  # name of custom profile
    default_email_server = "localhost"  # online vm server
    default_email_account = "max.mustermann@mpseinternational.com"
    default_email_account_password = "123"  # nosec This Password is only used
    # for the local Mail Server and is needed for the communication with
    # this Server

    secure_server_smtp_port = 465
    secure_server_imap_port = 143
    unsecure_server_smtp_port = 26
    unsecure_server_imap_port = 144

    email_client_config_location = os.getenv("APPDATA") + \
        r"\Thunderbird\Profiles\{}\prefs.js".format(default_email_profile)

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

    # sends mails based on *.txt files specified in the
    # email_files_location-path
    def send_mail_files(self, use_secured_client=True):
        import yaml
        from email.headerregistry import Address
        from email.message import EmailMessage
        from email import policy
        from email.parser import BytesParser

        if (config.EnvironmentConfig.LANGUAGE == "de"):
            import demos.fokusrnware.native.emails.de as mails
        else:
            import demos.fokusrnware.native.emails.en as mails

        email_files = [
            "Nina.yml", "Erika.yml", "Marius.yml",
            "Marius2.yml"
            # "nina_signed.txt" unused due to invalid smime signature
        ]

        logging.info(
            "Checking for mails in: {}".format(email_files)
        )

        for email_filename in email_files:
            logging.info("Sending mail file: {}".format(email_filename))
            filename = files(mails).joinpath(email_filename)

            if (filename.suffix == ".yml"):
                try:
                    with open(filename, 'r',  encoding='utf-8') as file:
                        yml_data = yaml.safe_load(file)
                except Exception as e:
                    logging.error(e)

                msg = EmailMessage()
                msg['Subject'] = yml_data["subject"]
                msg['From'] = Address(
                    display_name=yml_data["from"]["display_name"],
                    addr_spec=yml_data["from"]["email"])
                msg['To'] = Address(
                    display_name=yml_data["to"]["display_name"],
                    addr_spec=yml_data["to"]["email"])
                msg['Date'] = datetime.datetime.strptime(
                    "2020-01-01 " + str(yml_data["time"]), '%Y-%d-%m %H:%M')
                msg.set_content(yml_data["content"])

            elif (filename.suffix == ".txt"):
                with open(filename, 'rb') as fp:
                    msg = BytesParser(policy=policy.default).parse(fp)

            # TODO
            # check if secure mode, if no do not process smime mails
            # if not use_secured_client:
            #    if "Content-Type: multipart/signed;" in email_text:
            #        print("skipping because smime", email_filename)
            #        continue

            day_offset = 1  # nosec B311
            date_obj = datetime.date.today() - \
                datetime.timedelta(days=day_offset)
            # replace msg header with new date and remain previous time
            date_str = date_obj.strftime(
                "%a, %d %b %Y {}".format(
                    msg["Date"].datetime.strftime("%H:%M")))
            msg.replace_header("date", date_str)

            self.send_mail(msg)

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
                "phishing_mailserver")
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
            if os.path.isdir(
                    os.getenv("APPDATA") + r"\Thunderbird\Profiles\{}".format(
                        self.default_email_profile)
            ):
                logging.info("Nothing to do, exiting init")
                return

            # extract profile to location
            import demos.phishing.native.profiles as profiles
            filename = files(profiles).joinpath("profile.zip")
            with zipfile.ZipFile(filename, mode="r") as zipObj:
                zipObj.extractall(os.getenv("TEMP"))

            profile_location = os.getenv("APPDATA") + \
                f"{os.path.sep}Thunderbird" \
                f"{os.path.sep}Profiles" \
                f"{os.path.sep}{self.default_email_profile}"

            extracted_profile = os.path.join(
                os.getenv("TEMP"),
                f"Profiles{os.path.sep}{self.default_email_profile}")
            shutil.copytree(extracted_profile, profile_location)

            profile_ini_location = os.getenv("APPDATA") + f"{os.path.sep}" \
                                                          f"Thunderbird" \
                                                          f"{os.path.sep}" \
                                                          f"profiles.ini"

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

    def exec_rnsm(self):
        controller = Controller()
        controller.run()

    def create_desktop_files(self):
        global original_wallpaper
        dirName = "demos\\fokusrnware\\native\\desktop_files"
        desktop_files = self.getListOfFiles(dirName)

        # desktop path of current user
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']),
                               'Desktop')

        # copy files to desktop
        for filename in desktop_files:
            try:
                base = os.path.basename(filename)
                newPath = desktop + '\\' + base
                # os.system(command)
                shutil.copy(filename, newPath)
                # subprocess.call(command, shell=true)

            except:
                pass
        original_wallpaper = self.getWallpaper()
        original_wallpaper = bytes(original_wallpaper, 'utf-8')

    def getListOfFiles(self, dirName):
        # create a list of file and sub directories
        # names in the given directory
        listOfFile = os.listdir(dirName)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this
            # directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)
        return allFiles

    def getWallpaper(self):
        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(
            win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)
        return ubuf.value

    def reset(self):
        global original_wallpaper
        desktop = os.path.join(
            os.path.join(os.environ['USERPROFILE']), 'Desktop')
        files = glob.glob(
            os.path.join(desktop, '**', '*.enc'), recursive=True)
        ctypes.windll.user32.SystemParametersInfoA(
                20, 0, original_wallpaper, 0)
        for file in files:
            os.remove(file)
