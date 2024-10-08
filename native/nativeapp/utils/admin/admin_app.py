# SPDX-License-Identifier: AGPL-3.0-only

import pathlib
import sys
import re
import tempfile
import os
import signal
import traceback
import logging

from subprocess import Popen, PIPE  # nosec

from argparse import ArgumentParser, RawTextHelpFormatter

from typing import List

from nativeapp.config import config

from nativeapp.utils.net import network_control_protocol


NATIVEAPP_ADMIN_HEADER = 0xe11e
# network header identifier
NATIVEAPP_ADMIN_PORT = config.AdminConfig.LISTEN_PORT

if sys.platform == "win32":
    HOSTS_PATH = pathlib.Path("C:/Windows/System32/Drivers/etc/hosts")
else:
    HOSTS_PATH = pathlib.Path("/etc/hosts")


IP_REGEX = re.compile(r"((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))")  # noqa: E501


def call_cmd(command_list: List[str],
             workdir: pathlib.Path = None,
             shell=False):
    with Popen(  # nosec
            command_list, stdout=PIPE, cwd=workdir, shell=shell) as process:
        process.communicate()


class NativeappCommands:
    DISABLE_USB = 1
    SET_REDIRECT = 2
    DISABLE_REAL_TIME_MONITORING = 3
    ENABLE_REAL_TIME_MONITORING = 4
    CLEAR_DEFENDER_HISTORY = 5
    DISABLE_AUTOMATIC_SAMPLE_SUBMISSION = 6
    ENABLE_AUTOMATIC_SAMPLE_SUBMISSION = 7


def create_host_payload(
            enable: bool, domain: str, ip: str = "127.0.0.1") -> bytes:
    return f"{int(enable)};{ip};{domain}".encode()


class NativeappAdmin(network_control_protocol.NativeappControlServer):

    def __init__(self):
        super().__init__(NATIVEAPP_ADMIN_HEADER, NATIVEAPP_ADMIN_PORT)
        self.running = False

    def set_host_entry(self, target_host: str, target_ip: str, mode: str):
        # WSL
        cmd = ["wsl", "--user", "root", "bash", "-c",
               f"sed -i\"\" '/{target_host}/d' /etc/hosts"]
        call_cmd(cmd)

        if mode == "1":
            cmd = ["wsl", "--user", "root", "bash", "-c",
                   f"echo '{target_ip} {target_host}' >> /etc/hosts"]
            call_cmd(cmd)

        # native
        with open(HOSTS_PATH, "r+") as host_file:
            hosts_dict = {}
            for line in host_file:
                split = line.split(maxsplit=1)
                if len(split) > 1:
                    m = IP_REGEX.match(split[0])
                    if m:
                        print(split)
                        all_hosts = split[1].strip().split()
                        for h in all_hosts:
                            hosts_dict[h] = split[0].strip()
            if mode == "0":
                try:
                    del hosts_dict[target_host]
                except KeyError:
                    pass
            elif mode == "1":
                hosts_dict[target_host] = target_ip
            print(hosts_dict)
            host_file.seek(0)
            for h, i in hosts_dict.items():
                host_file.write(f"{i} {h}\n")
            host_file.truncate()

    def on_packet(self, command, payload):
        if command == NativeappCommands.DISABLE_REAL_TIME_MONITORING:
            # Disable Defender Real Time Monitoring for ransomware
            call_cmd(["powershell",
                      "Set-MpPreference",
                      "-DisableRealTimeMonitoring",
                      "$true"])
        elif command == NativeappCommands.ENABLE_REAL_TIME_MONITORING:
            # Enable Defender Real Time Monitoring for ransomware
            call_cmd(["powershell",
                      "Set-MpPreference",
                      "-DisableRealTimeMonitoring",
                      "$false"])
        elif command == NativeappCommands.DISABLE_AUTOMATIC_SAMPLE_SUBMISSION:
            # Disable Defender automatic sample submission for ransomware
            call_cmd(["powershell",
                      "Set-MpPreference",
                      "-SubmitSamplesConsent",
                      "2"])
        elif command == NativeappCommands.ENABLE_AUTOMATIC_SAMPLE_SUBMISSION:
            # Enable Defender automatic sample submission for ransomware
            call_cmd(["powershell",
                      "Set-MpPreference",
                      "-SubmitSamplesConsent",
                      "1"])
        elif command == NativeappCommands.CLEAR_DEFENDER_HISTORY:
            # Clear Defender History after Demo so scan results do not stay
            call_cmd(["powershell",
                      "Remove-Item",
                      "-recurse",
                      "'C:\ProgramData\Microsoft\Windows Defender\Scans\History\Service'"])
        elif command == NativeappCommands.DISABLE_USB:
            val = 4
            if payload == b"0":
                val = 3
            cmd = fr"powershell Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\USBSTOR\' -Name 'start' -Value {val}"  # noqa: E501
            call_cmd(cmd.split(" "))
        elif command == NativeappCommands.SET_REDIRECT:
            mode, target_ip, target_host = payload.decode().split(";")
            self.set_host_entry(target_host, target_ip, mode)


class NativeappAdminClient(network_control_protocol.NativeappControlClient):
    def __init__(self):
        super().__init__(NATIVEAPP_ADMIN_HEADER, NATIVEAPP_ADMIN_PORT)


def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("--mode", dest="mode", help="Set the mode. \
            Client disables usb access and adds an entry in the hosts. \
            Currently only there for test purposes",
                        type=str, required=True, choices=["server", "client"])
    args = parser.parse_args()
    logging_path = pathlib.Path("admin.log")
    logging.basicConfig(
        filename=logging_path,
        datefmt="%y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s - [%(module)s:%(funcName)s] : "
               "%(message)s",
        level=logging.INFO,
    )
    logging.info("Starting service: admin app")

    if args.mode == "server":
        temp_dir = pathlib.Path(tempfile.gettempdir())
        pid_file_path = pathlib.Path(temp_dir / "admin_app.pid")
        if pid_file_path.exists():
            with open(pid_file_path, "r") as pid_file:
                pid = pid_file.read()
                try:
                    os.kill(int(pid), signal.SIGKILL)
                except Exception:
                    logging.info("Failed to kill old process. Trying to continue")  # noqa: 501

        with open(pid_file_path, "w") as pid_file:
            pid_file.write(str(os.getpid()))

        try:
            app = NativeappAdmin()
            app.run()
        except Exception:
            logging.info(traceback.format_exc())

        pid_file_path.unlink()

    elif args.mode == "client":
        client = NativeappAdminClient()
        client.send_command(NativeappCommands.DISABLE_USB, b"1")
        client.send_command(NativeappCommands.SET_REDIRECT,
                            create_host_payload(True, "127.0.0.1",
                                                "projekt-elite.de"))


if __name__ == "__main__":
    main()
