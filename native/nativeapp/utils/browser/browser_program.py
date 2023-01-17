from abc import ABC, abstractmethod

import logging
import subprocess  # nosec
import shutil
import tempfile
import pathlib

from argparse import ArgumentParser, RawTextHelpFormatter


class BrowserProgram(ABC):

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


class BrowserProgramEdge(BrowserProgram):
    def __init__(self, name, profile_zip_path):
        self.profile_name = name
        self.profile_zip_path = profile_zip_path
        self.process = None
        self.profile_dir = pathlib.Path.home() / f"AppData/Local/Microsoft/Edge/User Data/{self.profile_name}"  # noqa: E501

    def kill_edge(self):
        subprocess.Popen(  # nosec
                    ["C:\\Windows\\System32\\taskkill.exe", "/f", "/t", "/im",
                        "msedge.exe"])

    def save_profile(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.kill_edge()
            temp_dir = pathlib.Path(temp_dir)
            try:
                shutil.copytree(self.profile_dir, temp_dir / self.profile_name)
            except Exception:  # nosec
                # Ignore stupid Windows errors
                pass
            p = subprocess.Popen(  # nosec
                    ["reg",
                     "export",
                     fr"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Edge\PreferenceMACs\{self.profile_name}",  # noqa: E501
                     temp_dir / "edge.reg"])
            p.communicate()
            shutil.make_archive(self.profile_zip_path, "zip", temp_dir)

    def copy_profile(self):
        """Initializes edge with a predefined profile with already set
        up config, if not already present"""
        logging.info("Edge init")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            # FUCK YOU EDGE!!
            self.kill_edge()
            logging.info(f"Removing old profile at \
                    {self.profile_dir} exists {self.profile_dir.exists()}")
            shutil.rmtree(self.profile_dir, ignore_errors=True)
            logging.info(f"Extracting profile {self.profile_zip_path} to \
                    {temp_dir}")
            shutil.unpack_archive(self.profile_zip_path, temp_dir)
            logging.info("Importing reg")
            # nosec
            with subprocess.Popen(["reg",
                                   "import",
                                   temp_dir / "edge.reg"]) as reg_proc:
                reg_proc.communicate()
            logging.info(f"Copying {temp_dir / self.profile_name} to \
                    {self.profile_dir} exists {self.profile_dir.exists()}")
            shutil.copytree(temp_dir / self.profile_name, self.profile_dir,
                            dirs_exist_ok=True)

    def stop(self):
        """Close edge browser"""
        logging.info("Try closing running edge browser process...")
        try:
            if self.process:
                self.process.kill()
            # Edge doesn't seem to care so we just send a SIGKILL
            self.kill_edge()
            shutil.rmtree(self.profile_dir, ignore_errors=True)
            key_path = fr"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Edge\PreferenceMACs\{self.profile_name}"  # noqa: E501
            subprocess.Popen(  # nosec
                    ["reg", "delete", key_path, "/va", "/f"])
            subprocess.Popen(  # nosec
                    ["reg", "delete", key_path + r"\extensions.settings",
                     "/va", "/f"])
            logging.info("Success")
        except Exception as e:
            logging.error(e)

    def start(self):
        """Start edge browser"""
        logging.info(f"Try starting edge process \
                with profile {self.profile_name}...")
        try:
            edge_dir = pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application")  # noqa: E501
            # Since I don't understand how windows is handling arguments
            # we need to start a shell
            cmd = ["powershell",
                   f"./msedge.exe --profile-directory=\"{self.profile_name}\""]
            self.process = subprocess.Popen(  # nosec
                    cmd, cwd=edge_dir
                )
            logging.info("Success")
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("-p", "--profile", dest="profile",
                        help="Name of the Profile", type=str, default=None,
                        required=True)
    parser.add_argument("-o", "--output", dest="output",
                        help="Path to the output file", type=str, default=None,
                        required=True)
    args = parser.parse_args()

    edge = BrowserProgramEdge(args.profile, args.output)
    edge.save_profile()
