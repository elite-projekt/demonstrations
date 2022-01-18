import os
import logging
import zipfile
import shutil
import subprocess

from native.src.config import config


class DownloadDemo:
    @staticmethod
    def create_fake_malware():
        logging.info("creating fake malware...")

        path = os.path.join(
            os.path.join(os.environ['USERPROFILE']), 'Desktop')
        filename = os.path.join(path, "malware.bat")

        file = open(filename, "w")
        f = "@echo off\n"
        f += "echo ########################################################"
        f += "####\n"
        f += "echo: \n"
        f += "echo     Waere dies keine Demo, waeren Sie nun gehackt worden\n"
        f += "echo: \n"
        f += "echo #########################################################"
        f += "###\n"
        f += "echo: \n"
        f += "echo Sie waren ungeschuetzt auf einer infizierten Website und"
        f += "sind\n"
        f += "echo Opfer eines Drive-By Downloads geworden. Ein Drive-By"
        f += "Download\n"
        f += "echo ist ein Download, der ohne Ihr Wissen durchgefuehrt werden"
        f += "kann.\n"
        f += "echo: \n"
        f += "echo Im Folgenden wird Ihnen erklaert, wie Sie sich vor"
        f += "solchen\n"
        f += "echo Angriffen schuetzen koennen. Schliessen Sie dieses Fenster"
        f += "und\n"
        f += "echo kehren Sie zu ihrem Browser zurueck.\n"
        f += "echo: "
        f += "pause\n"
        f += "exit"

        file.write(f)
        file.close()

        os.system("start /wait cmd.exe @cmd /k \"" + filename + "\"")

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
                subprocess.Popen(
                    ["C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                     "-P", "MPSE_download_safe",
                     "-url", "http://localhost:5001"]
                )
            if not safe:
                subprocess.Popen(
                    ["C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                     "-P", "MPSE_download_unsafe",
                     "-url", "http://localhost:5001"]
                )

            logging.info("Success")
        except Exception as e:
            logging.error(e)
