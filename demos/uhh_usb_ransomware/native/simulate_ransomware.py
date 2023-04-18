# SPDX-License-Identifier: AGPL-3.0-only

import urllib.request
import ctypes
import pathlib
import win32con
from cryptography.fernet import Fernet
import pyautogui
import importlib.resources

pyautogui.FAILSAFE = False


def get_encrypted_name(file_path):
    file_path = pathlib.Path(file_path)
    out_path = file_path.with_suffix(f"{file_path.suffix}.aes")
    return out_path


class DesktopFile():
    def __init__(self, filename: str):
        self.file_path = pathlib.Path.home() / "Desktop" / filename


class RansomwareSimulation():
    def __init__(self, loc):
        self.locale = loc
        self.original_wallpaper = ""
        self.key = Fernet.generate_key()
        self.cryptor = Fernet(self.key)
        self.desktop_files = {
                DesktopFile("Suggestion_1.txt"):
                self.locale.translate("file_one"),
                DesktopFile("Suggestion_2.txt"):
                self.locale.translate("file_two"),
                DesktopFile("Suggestion_3.txt"):
                self.locale.translate("file_three"),
                DesktopFile("gehaltsdaten.csv"):
                "max,10000\nsandra,100000\nolaf,30291\nlisa,4910349",
                DesktopFile("projektbericht.odt"): "asdasdl",
                DesktopFile("passwörter.doc"): "asdfk",
                DesktopFile("mitarbeiter.ods"): "a",
                DesktopFile("kundendaten.csv"): "superimportant",
                DesktopFile("kundendaten_backup.csv"): "this is not a backup!",
                DesktopFile("kundendaten_backup (1).csv"):
                "this is not a backup!",
                DesktopFile("kundendaten_backup (2).csv"):
                "this is not a backup!",
                DesktopFile("kundendaten_backup (3).csv"):
                "this is not a backup!",
                              }

    def prepare(self):
        self.generate_files()

    def run_ransomware(self):
        pyautogui.hotkey("winleft", "d")
        self.encrypt_files()
        self.change_background()

    def generate_files(self):
        for path, content in self.desktop_files.items():
            with open(path.file_path, "w") as f:
                f.write(content)

    def encrypt_file(self, file_path):
        file_path = pathlib.Path(file_path)
        if file_path.exists():
            with open(file_path, "rb") as f:
                content = f.read()
                encrypted = self.cryptor.encrypt(content)
                with open(get_encrypted_name(file_path), "wb") as f2:
                    f2.write(encrypted)
            file_path.unlink(missing_ok=True)

    def encrypt_files(self):
        for f in self.desktop_files:
            self.encrypt_file(f.file_path)

    def getWallpaper(self):
        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(
            win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0)
        return ubuf.value

    def change_background(self):
        self.original_wallpaper = self.getWallpaper()
        self.original_wallpaper = bytes(self.original_wallpaper, 'utf-8')
        wallpaper_package = "demos.uhh_usb_ransomware.native.resources"
        wallpaper_path = pathlib.Path()
        with importlib.resources.path(
                wallpaper_package,
                f"wallpaper_{self.locale.locale_identifier}.png") as p:
            wallpaper_path = p

        # Fallback to en wallpaper
        if not wallpaper_path.exists():
            with importlib.resources.path(
                    wallpaper_package, "wallpaper_en.png") as p:
                wallpaper_path = p

        wallpaper = bytes(str(wallpaper_path.absolute()), 'utf-8')
        ctypes.windll.user32.SystemParametersInfoA(20, 0, wallpaper, 0)

    def set_original_background(self):
        if self.original_wallpaper != "":
            ctypes.windll.user32.SystemParametersInfoA(
                20, 0, self.original_wallpaper, 0)

    def remove_files(self):
        for path in self.desktop_files:
            enc_path = get_encrypted_name(path.file_path)
            enc_path.unlink(missing_ok=True)
            path.file_path.unlink(missing_ok=True)

    def stop_demo(self):
        PROTOCOL = "http"
        HOST = "127.0.0.1:5000"
        PATH = "orchestration/stop/demo/uhh_usb_ransomware"
        urllib.request.urlopen(f"{PROTOCOL}://{HOST}/{PATH}")  # nosec

    def stop(self):
        self.set_original_background()
        self.remove_files()


if __name__ == "__main__":
    ransomware_test = RansomwareSimulation(None)
