from abc import ABC, abstractmethod

import logging
import subprocess  # nosec
import sys
import shutil
import re
import configparser
import tempfile
import zipfile
import pathlib
import os


class MailProgram(ABC):

    @abstractmethod
    def stop(self):
        """
        Stops the running mail program
        """

    @abstractmethod
    def start(self):
        """
        Start the mail program
        """

    @abstractmethod
    def copy_profile(self):
        """
        Copy the profile to the corresponsing dir
        """


class MailProgramThunderbird(MailProgram):
    def __init__(self, name, profile_zip_path):
        self.profile_name = name
        self.profile_zip_path = profile_zip_path
        self.profile_dir_name = f"elite.{self.profile_name}"
        app_data_dir = os.getenv("APPDATA")
        if app_data_dir is not None and pathlib.Path(app_data_dir).exists():
            self.profile_dir = pathlib.Path(os.getenv("APPDATA")) / \
                "Thunderbird/Profiles"
        else:
            # env or dir is invalid
            self.profile_dir = pathlib.Path().home() / ".thunderbird"

    def stop(self):
        """Close mail application"""
        logging.info("Try closing running thunderbird process...")
        try:
            # False positive. See also:
            # https://github.com/PyCQA/bandit/issues/333#issuecomment-404103697
            if sys.platform == "win32":
                subprocess.Popen(  # nosec
                    ["C:\\Windows\\System32\\taskkill.exe", "/f", "/im",
                     "thunderbird.exe"],
                    stdout=subprocess.PIPE, shell=False
                )
            else:
                subprocess.Popen("pkill", "thunderbird",  # nosec
                                 stdout=subprocess.PIPE)
            logging.info("Success")
        except Exception as e:
            logging.error(e)

    def start(self):
        """Start mail application"""
        logging.info(f"Try starting thunderbird process \
                with profile {self.profile_name}...")
        try:
            # False positive. See also:
            # https://github.com/PyCQA/bandit/issues/333#issuecomment-404103697
            if sys.platform == "win32":
                subprocess.Popen(  # nosec
                    ["C:\\Program Files\\Mozilla Thunderbird\\thunderbird.exe",
                     "-P", self.profile_name], shell=False
                )
            else:
                subprocess.Popen("thunderbird", "-P",  # nosec
                                 self.profile_name,
                                 stdout=subprocess.PIPE)
            logging.info("Success")
        except Exception as e:
            logging.error(e)

    def copy_profile(self):
        """Initializes thunderbird with a predefined profile with already set
        up config, if not already present"""
        logging.info("Thunderbird init")
        # check if profile already present
        try:
            # extract profile to location
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = pathlib.Path(temp_dir)
                with zipfile.ZipFile(self.profile_zip_path) as zip_obj:
                    zip_obj.extractall(temp_dir)

                extracted_profile = pathlib.Path(temp_dir) / \
                    "Profiles" / self.profile_dir_name
                output_dir = self.profile_dir / self.profile_dir_name
                shutil.rmtree(output_dir, ignore_errors=True)
                shutil.copytree(extracted_profile, output_dir)

            profile_ini_location = self.profile_dir.parent / "profiles.ini"

            config_parser = configparser.ConfigParser()

            # Needs to do it this, else the key values of config are converted
            # complete to lowercase characters
            config_parser.optionxform = str

            config_parser.read(profile_ini_location)
            profile_regex = re.compile(r"^Profile([\d]+)$")

            max_profile_number = -1
            target_profile = None
            for key in config_parser.sections():
                m = profile_regex.match(key)
                if m is not None:
                    num = int(m.groups()[0])
                    max_profile_number = max(max_profile_number, num)
                    if "Name" in config_parser[key]:
                        if config_parser[key]["Name"] == self.profile_name:
                            target_profile = key
                            break
            if target_profile is None:
                target_profile = f"Profile{max_profile_number + 1}"

            config_parser[target_profile] = {
                'Name': self.profile_name,
                'IsRelative': 1,
                'Path': 'Profiles/' + self.profile_dir_name
            }

            with open(profile_ini_location, 'w') as config_file:
                config_parser.write(config_file, space_around_delimiters=False)

            logging.info("Init done")
        except Exception as e:
            logging.error(e)
