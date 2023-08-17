# SPDX-License-Identifier: AGPL-3.0-only

import urllib.request
import os
import shutil
import pathlib
import psutil
import subprocess


class ObfuscationSimulation():
    def __init__(self, loc):
        self.locale = loc
        # TODO May need adjusting path
        self.dirName_to_copy = "/demos/uhh_obfuscation/native/resources/"
        self.files_to_copy = [self.dirName_to_copy + "RansomWare.py",
                              self.dirName_to_copy + "TestScan.py"]
        self.desktop = pathlib.Path.home() / "Desktop"
        self.webserver = ""
        self.cmd_pids_before = []
        self.cmd_pids_after = []

    def prepare(self):
        # Replace texts in Scan file
        with open(str(pathlib.Path.cwd().resolve()) + self.files_to_copy[1], "r") as s: # noqa: 501
            fc = s.read()
        fc = fc.replace("AAA", self.locale.translate("scan_virus_detected"))
        fc = fc.replace("BBB", self.locale.translate("scan_no_virus_detected"))
        fc = fc.replace("CCC", self.locale.translate("scan_end_demo"))
        fc = fc.replace("DDD", self.locale.translate("scan_end_scan"))
        fc = fc.replace("EEE", self.locale.translate("scan_end_wait"))
        fc = fc.replace("FFF", self.locale.translate("scan_error"))
        with open(str(pathlib.Path.cwd().resolve()) + self.files_to_copy[1], "w+") as s: # noqa: 501
            s.write(fc)
        # Copy files to desktop
        for filename in self.files_to_copy:
            base = pathlib.Path(filename).name
            filename = str(pathlib.Path.cwd().resolve()) + filename
            newPath = self.desktop / base
            shutil.copy(filename, newPath)
        # Generate scan runner file
        with open(self.desktop / "runner.bat", "w+") as runner:
            runner.write(f"@ECHO OFF\ncd {str(self.desktop)}\npython TestScan.py") # noqa: 501
        # Generate list of all cmd.exe processes
        self.cmd_pids_before = self.get_pids_by_name("cmd.exe")

    def get_pids_by_name(self, process_name):
        pids = []
        for process in psutil.process_iter(["pid", "name"]):
            if process.info["name"] == process_name:
                pids.append(process.info["pid"])
        return pids

    def run_obfuscation(self):
        pass

    def scan_ransomware(self):
        os.startfile(self.desktop / "runner.bat")

    def copy_ransomware(self):
        this_path = pathlib.Path.cwd().resolve()
        ransomware_path = str(this_path / "demos/uhh_obfuscation/native/resources/RansomWare_obfuscated.py") # noqa: 501
        ransomware_to_copy_path = self.desktop / "RansomWare_obfuscated.py"
        shutil.copy(ransomware_path, ransomware_to_copy_path)

    def stop_demo(self):
        PROTOCOL = "http"
        HOST = "127.0.0.1:5000"
        PATH = "orchestration/stop/demo/uhh_obfuscation"
        urllib.request.urlopen(f"{PROTOCOL}://{HOST}/{PATH}")  # nosec

    def stop(self):
        # Rename variables in Scan program
        with open(str(str(pathlib.Path.cwd().resolve()) + self.files_to_copy[1]), "r") as s: # noqa: 501
            fc = s.read()
        fc = fc.replace(self.locale.translate("scan_virus_detected"), "AAA")
        fc = fc.replace(self.locale.translate("scan_no_virus_detected"), "BBB")
        fc = fc.replace(self.locale.translate("scan_end_demo"), "CCC")
        fc = fc.replace(self.locale.translate("scan_end_scan"), "DDD")
        fc = fc.replace(self.locale.translate("scan_end_wait"), "EEE")
        fc = fc.replace(self.locale.translate("scan_error"), "FFF")
        with open(str(str(pathlib.Path.cwd().resolve()) + self.files_to_copy[1]), "w+") as s: # noqa: 501
            s.write(fc)
        # Remove files from desktop
        self.desktop_files = [self.desktop / "RansomWare.py",
                              self.desktop / "RansomWare_obfuscated.py",
                              self.desktop / "TestScan.py",
                              self.desktop / "runner.bat"]
        for filename in self.desktop_files:
            try:
                os.remove(filename)
            except: # noqa: 722
                pass
        # Generate list of all cmd.exe processes
        self.cmd_pids_after = self.get_pids_by_name("cmd.exe")
        procs_to_stop = [proc for proc in self.cmd_pids_after if proc not in self.cmd_pids_before] # noqa: 501
        # End all remaining cmd.exe processes
        for p in procs_to_stop:
            subprocess.Popen(  # nosec
                    ["C:\\Windows\\System32\\taskkill.exe", "/f", "/t", "/pid",
                        str(p)])
        # End Edge
        subprocess.Popen(  # nosec
                ["C:\\Windows\\System32\\taskkill.exe", "/f", "/t", "/im",
                    "msedge.exe"])


if __name__ == "__main__":
    obfuscation_test = ObfuscationSimulation(None)
