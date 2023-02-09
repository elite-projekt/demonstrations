# SPDX-License-Identifier: AGPL-3.0-only

from subprocess import Popen  # nosec
from pynput.keyboard import Listener as Listener_kb
from pynput.keyboard import Controller as Controller_kb
from pynput.keyboard import Key
from pynput.mouse import Listener as Listener_ms
from pynput.mouse import Controller as Controller_ms
from pynput.mouse import Button
from time import sleep
from time import time
import urllib.request
import tempfile
import pathlib
import logging

cert_url = "http://mitm.it/cert/cer"
cert_proxy = "http://127.0.0.1:8080"
proxy_host = "127.0.0.1:8080"


class ActivityListener:
    def __init__(self):
        self.last_activity = time()
        # Seconds of inactivity before start
        self.inactivity_timer_sec = 5
        self.listener_kb = Listener_kb(on_press=self.on_press_kb)
        self.listener_kb.start()
        self.listener_ms = Listener_ms(on_move=self.on_move_ms,
                                       on_click=self.on_click_ms)
        self.listener_ms.start()

    def on_press_kb(self, key):
        self.last_activity = time()

    def on_move_ms(self, x, y):
        self.last_activity = time()

    def on_click_ms(self, x, y, button, pressed):
        self.last_activity = time()

    def get_inactivity_s(self) -> int:
        return time() - self.last_activity


# Enable proxy and set it to proxy_host
def disable_proxy():
    enable_proxy_command = "powershell $p='HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'; set-itemproperty $p -name ProxyEnable -value 0"  # noqa: E501
    Popen(args=enable_proxy_command, shell=True)  # nosec


# Enable proxy and set it to proxy_host
def enable_and_set_proxy():
    enable_proxy_command = f"powershell $p='HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'; set-itemproperty $p -name ProxyEnable -value 1; set-itemproperty $p -name ProxyServer -value '{proxy_host}'"  # noqa: E501
    Popen(args=enable_proxy_command, shell=True)  # nosec


def __click_cert_dialog():
    mouse = Controller_ms()
    keyboard = Controller_kb()
    old_pos = mouse.position
    mouse.position = (1062, 634)
    mouse.click(Button.left, 1)
    mouse.position = old_pos
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


# Add ca cert to root
def add_cert():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = pathlib.Path(temp_dir)
        cert_path = temp_dir / "cert.cer"
        proxies = {'http': cert_proxy}
        opener = urllib.request.FancyURLopener(proxies)  # nosec
        logging.info(f"Getting cert from {cert_url} with proxy {cert_proxy}")
        with opener.open(cert_url) as in_f:
            with open(cert_path, "wb") as cert_file:
                logging.info(f"Writing cert to {cert_path}")
                cert_file.write(in_f.read())
        logging.info("Running certutil...")
        add_cert_command = \
            f"certutil.exe -addstore -f -user Root {cert_path}"
        p = Popen(args=add_cert_command, shell=True)  # nosec
        sleep(0.5)
        while p.poll() is None:
            __click_cert_dialog()
            sleep(0.5)


# Start add_cert and simulate_keypresses at the same time
if __name__ == '__main__':
    enable_and_set_proxy()
    sleep(2)
    add_cert()

# ca cert can be manually deleted in certmgr.msc
