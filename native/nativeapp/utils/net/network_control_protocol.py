# SPDX-License-Identifier: AGPL-3.0-only

import struct
import socket
import binascii
import threading
import logging

from abc import ABC, abstractmethod
from typing import Tuple


class NativeappControlClient:
    def __init__(self, header, port):
        self.header = header
        self.port = port

    def connect(self):
        self.socket = socket.create_connection(("127.0.0.1", self.port))
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.socket.connect(("127.0.0.1", self.port))

    def send_command(self, command: int, payload: bytes):
        self.connect()
        if isinstance(payload, int):
            payload = payload.to_bytes(8, "big")
        data_len = len(payload)
        header_data = struct.pack(
                "<HII", self.header, command, data_len)
        header_crc = binascii.crc32(header_data)
        header_data = struct.pack(
                "<HIII", self.header, command, data_len, header_crc)
        payload_crc = struct.pack("<I", binascii.crc32(payload))
        complete_packet = header_data + payload + payload_crc
        self.socket.send(complete_packet)


class NativeappControlServer(ABC):
    def __init__(self, header, port):
        self.running = False
        self.header = header
        self.listen_thread = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("127.0.0.1", port))
        self.socket.listen(1)

    def run(self, foreground=True):
        if foreground:
            self._run()
        else:
            self.listen_thread = threading.Thread(target=self._run)
            self.listen_thread.start()

    def stop(self):
        self.running = False
        self.socket.close()
        if self.listen_thread:
            self.listen_thread.join()

    def _run(self):
        self.running = True
        while self.running:
            try:
                conn, addr = self.socket.accept()
                with conn:
                    data = conn.recv(1024)
                    if data:
                        try:
                            command, payload = self.parse_packet(data)
                            self.on_packet(command, payload)
                        except ValueError as e:
                            logging.warning(f"Ignoring invalid packet: {e}")
            except Exception:
                pass

    def parse_packet(self, packet: bytes) -> Tuple[int, bytes]:
        # 14 header + min 1 payload + 4 payload crc
        if len(packet) < 19:
            raise ValueError("Invalid packet length")
        # checking header
        magic, command, data_len, header_crc = struct.unpack("<HIII",
                                                             packet[:14])
        if magic != self.header:
            raise ValueError("Invalid header")
        # check crc
        if header_crc != binascii.crc32(packet[:10]):
            raise ValueError("Invalid header crc")

        payload = packet[14:-4]
        payload_crc = struct.unpack("<I", packet[-4:])[0]
        calc_crc = binascii.crc32(payload)
        if calc_crc != payload_crc:
            raise ValueError("Invalid payload crc")

        return (command, payload)

    @abstractmethod
    def on_packet(self, command, payload):
        """
        Method to call once a new paket arrives
        """
