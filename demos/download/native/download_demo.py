import os
import configparser
import logging
import zipfile
import requests
import shutil
# We need this module and the severity is low. See also:
# https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html#b404-import-subprocess
import subprocess  # nosec

from native.src.config import config
from demos.download.native.download_demo_text import DownloadDemoText


class DownloadDemo:
    @staticmethod
    def create_fake_malware():
        logging.info("creating fake malware...")

        path = os.path.join(
            os.path.join(os.environ['USERPROFILE']), 'Desktop')

        filename_malware = os.path.join(path, "malware.bat")

        filename_info_src =\
            os.path.join(config.EnvironmentConfig.FILEDIR, "download-demo.txt")
        filename_info_dest = os.path.join(path, "download-demo.txt")

        # write fake malware script
        file = open(filename_malware, "w")
        file.write(DownloadDemoText.script)
        file.close()

        # copy info file
        shutil.copy(filename_info_src, filename_info_dest)

        # We need this function and the severity is low. False pos. See also:
        # https://github.com/PyCQA/bandit/issues/333#issuecomment-404103697
        for i in range(10):
            subprocess.Popen(  # nosec
                [
                    "C:\\Windows\\System32\\WindowsPowerShell" +
                    "\\v1.0\\powershell.exe",
                    filename_malware
                ],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                shell=False
            )

    @staticmethod
    def firefox_init():
        """Initializes firefox with a predefined profile with already set
        up config, if not already present"""
        logging.info("firefox init")
        # check if profile already present
        try:
            if not os.path.isdir(
                    os.getenv("APPDATA") +
                    r"\Mozilla\Firefox\Profiles" +
                    r"\1y2st08z.MPSE_download_unsafe"
            ):
                print("start unzip...")
                # extract profile to location
                profile_zip = os.path.join(config.EnvironmentConfig.PROFILEDIR,
                                           "1y2st08z.MPSE_download_unsafe.zip")
                with zipfile.ZipFile(profile_zip, "r") as zipObj:
                    zipObj.extractall(config.EnvironmentConfig.PROFILEDIR)

                print("get location...")

                profile_location \
                    = os.getenv("APPDATA") + f"{os.path.sep}" \
                                             f"Mozilla" \
                                             f"{os.path.sep}" \
                                             f"Firefox" \
                                             f"{os.path.sep}" \
                                             f"Profiles" \
                                             f"{os.path.sep}" \
                                             f"1y2st08z.MPSE_download_unsafe"

                extracted_profile \
                    = os.path.join(config.EnvironmentConfig.PROFILEDIR,
                                   "1y2st08z.MPSE_download_unsafe")
                shutil.copytree(extracted_profile, profile_location)

                profile_ini_location \
                    = os.getenv("APPDATA") + f"{os.path.sep}" \
                                             f"Mozilla" \
                                             f"{os.path.sep}" \
                                             f"Firefox" \
                                             f"{os.path.sep}" \
                                             f"profiles.ini"

                config_parser = configparser.ConfigParser()

                # Needs to do it this, else the key values of config
                # are converted complete to lowercase characters
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
                    'Path': 'Profiles/1y2st08z.MPSE_download_unsafe'
                }

                with open(profile_ini_location, 'w') as config_file:
                    config_parser.write(
                        config_file, space_around_delimiters=False
                    )

                print("unsafe init done...")

            else:
                logging.info("Nothing to do, unsafe profile exiting init")

            if not os.path.isdir(
                    os.getenv("APPDATA") +
                    r"\Mozilla\Firefox\Profiles" +
                    r"\fkstz94l.MPSE_download_safe"
            ):
                # extract profile to location
                profile_zip = os.path.join(config.EnvironmentConfig.PROFILEDIR,
                                           "fkstz94l.MPSE_download_safe.zip")
                with zipfile.ZipFile(profile_zip, "r") as zipObj:
                    zipObj.extractall(config.EnvironmentConfig.PROFILEDIR)

                profile_location \
                    = os.getenv("APPDATA") + f"{os.path.sep}" \
                                             f"Mozilla" \
                                             f"{os.path.sep}" \
                                             f"Firefox" \
                                             f"{os.path.sep}" \
                                             f"Profiles" \
                                             f"{os.path.sep}" \
                                             f"fkstz94l.MPSE_download_safe"

                extracted_profile \
                    = os.path.join(config.EnvironmentConfig.PROFILEDIR,
                                   "fkstz94l.MPSE_download_safe")
                shutil.copytree(extracted_profile, profile_location)

                profile_ini_location \
                    = os.getenv("APPDATA") + f"{os.path.sep}" \
                                             f"Mozilla" \
                                             f"{os.path.sep}" \
                                             f"Firefox" \
                                             f"{os.path.sep}" \
                                             f"profiles.ini"

                config_parser = configparser.ConfigParser()

                # Needs to do it this, else the key values of config
                # are converted complete to lowercase characters
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
                    'Path': 'Profiles/fkstz94l.MPSE_download_safe'
                }

                with open(profile_ini_location, 'w') as config_file:
                    config_parser.write(
                        config_file, space_around_delimiters=False
                    )

            else:
                logging.info("Nothing to do, safe profile exiting init")

            logging.info("Init done")
        except Exception as e:
            print(e)
            logging.error(e)

    @staticmethod
    def start_web_browser(safe):
        """Start web browser"""
        logging.info("Try starting firefox process...")
        try:
            if safe:
                # False positive. See also:
                # https://github.com/PyCQA/bandit/issues/333#issuecomment-404103697
                subprocess.Popen(  # nosec
                    ["C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                     "-P", "MPSE_download_safe",
                     "-url", "http://printer.io:5001/template.html"],
                    shell=False
                )
            if not safe:
                # False positive. See also:
                # https://github.com/PyCQA/bandit/issues/333#issuecomment-404103697
                subprocess.Popen(  # nosec
                    ["C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                     "-P", "MPSE_download_unsafe",
                     "-url", "http://printer.io:5001/template.html"],
                    shell=False
                )

            logging.info("Success")
        except Exception as e:
            logging.error(e)

    @staticmethod
    def probe_container_status():
        try:
            r = requests.get(
                'http://printer.io:5001/template.html'
            )
            if r.status_code == 200:
                return True
            else:
                return False
        except Exception:
            return

    @staticmethod
    def delete_demo_files():
        try:
            path = os.path.join(
                os.path.join(os.environ['USERPROFILE']), 'Desktop')

            filename_malware = os.path.join(path, "malware.bat")

            os.remove(filename_malware)
        except Exception as e:
            logging.error(e)
