"""
Copyright (C) 2022 Kevin Köster

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""
import struct
import socket
import binascii
import pathlib
import sys
import re
import tempfile
import os
import signal

from subprocess import Popen, PIPE  # nosec

from argparse import ArgumentParser, RawTextHelpFormatter

from typing import List

from nativeapp.config import config


NATIVEAPP_ADMIN_HEADER = 0xe11e
# network header identifier
NATIVEAPP_ADMIN_PORT = config.AdminConfig.LISTEN_PORT

if sys.platform == "win32":
    HOSTS_PATH = pathlib.Path("C:/Windows/System32/Drivers/etc/hosts")
else:
    HOSTS_PATH = pathlib.Path("/etc/hosts")


IP_REGEX = re.compile(r"((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))")  # noqa: E501


def call_cmd(command_list: List[str], workdir: pathlib.Path = None):
    with Popen(  # nosec
            command_list, stdout=PIPE, cwd=workdir) as process:
        process.communicate()


class NativeappCommands:
    DISABLE_USB = 1
    SET_REDIRECT = 2


class NativeappAdminClient:
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect(("127.0.0.1", NATIVEAPP_ADMIN_PORT))

    def send_command(self, command: int, payload: bytes):
        self.connect()
        data_len = len(payload)
        header_data = struct.pack(
                "<HII", NATIVEAPP_ADMIN_HEADER, command, data_len)
        header_crc = binascii.crc32(header_data)
        header_data = struct.pack(
                "<HIII", NATIVEAPP_ADMIN_HEADER, command, data_len, header_crc)
        payload_crc = struct.pack("<I", binascii.crc32(payload))
        self.socket.send(header_data + payload + payload_crc)


def create_host_payload(
            enable: bool, domain: str, ip: str = "127.0.0.1") -> bytes:
    return f"{int(enable)};{ip};{domain}".encode()


class NativeappAdmin:

    def __init__(self):
        self.running = False

    def run_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("127.0.0.1", NATIVEAPP_ADMIN_PORT))
        self.socket.listen(1)
        self.running = True
        while self.running:
            conn, addr = self.socket.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    self.parse_packet(data)

    def parse_packet(self, packet: bytes) -> None:
        # 14 header + min 1 payload + 4 payload crc
        if len(packet) < 19:
            print("Invalid packet len")
            return
        # checking header
        magic, command, data_len, header_crc = struct.unpack("<HIII",
                                                             packet[:14])
        if magic != NATIVEAPP_ADMIN_HEADER:
            print("Invalid header")
            return
        # check crc
        if header_crc != binascii.crc32(packet[:10]):
            print("Invalid header crc")
            return

        payload = packet[14:-4]
        payload_crc = struct.unpack("<I", packet[-4:])[0]
        calc_crc = binascii.crc32(payload)
        if calc_crc != payload_crc:
            print("Invalid payload crc")
            return
        print("crc correct")
        print(f"{command=} {data_len=} {header_crc=}")
        print(payload)

        if command == NativeappCommands.DISABLE_USB:
            val = 4
            if payload == b"0":
                val = 3
            cmd = fr"powershell Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\USBSTOR\' -Name 'start' -Value {val}"  # noqa: E501
            call_cmd(cmd.split(" "))
        elif command == NativeappCommands.SET_REDIRECT:
            mode, target_ip, target_host = payload.decode().split(";")
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


def main():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("--mode", dest="mode", help="Set the mode. \
            Client disables usb access and adds an entry in the hosts. \
            Currently only there for test purposes",
                        type=str, required=True, choices=["server", "client"])
    args = parser.parse_args()

    if args.mode == "server":
        temp_dir = pathlib.Path(tempfile.gettempdir())
        pid_file_path = pathlib.Path(temp_dir / "admin_app.pid")
        if pid_file_path.exists():
            with open(pid_file_path, "r") as pid_file:
                pid = pid_file.read()
                try:
                    os.kill(int(pid), signal.SIGKILL)
                except Exception:
                    print("Failed to kill old process. Trying to continue")

        with open(pid_file_path, "w") as pid_file:
            pid_file.write(str(os.getpid()))

        app = NativeappAdmin()
        app.run_socket()

        pid_file_path.unlink()

    elif args.mode == "client":
        client = NativeappAdminClient()
        client.send_command(NativeappCommands.DISABLE_USB, b"1")
        client.send_command(NativeappCommands.SET_REDIRECT,
                            create_host_payload(True, "127.0.0.1",
                                                "projekt-elite.de"))


if __name__ == "__main__":
    main()
