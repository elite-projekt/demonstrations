# SPDX-License-Identifier: AGPL-3.0-only

import sys
import logging
import threading
import re

if sys.platform == "win32":
    import pythoncom
    import wmi


class USBInfo:
    def __init__(self):
        self.pid = 0
        self.vid = 0


class USBMonitor:
    def __init__(self, on_connect=None, on_disconnect=None):
        self.running = False
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.usb_thread_connect = threading.Thread(
                target=self._start_usb_monitor_connect)
        self.usb_thread_connect.start()
        self.usb_thread_disconnect = threading.Thread(
                target=self._start_usb_monitor_disconnect)
        self.usb_thread_disconnect.start()

    def stop(self):
        self.running = False
        logging.info("Waiting for USB thread")
        if self.usb_thread_connect is not None and \
           self.usb_thread_connect.is_alive():
            self.usb_thread_connect.join()
        if self.usb_thread_disconnect is not None and \
           self.usb_thread_disconnect.is_alive():
            self.usb_thread_disconnect.join()

    def _create_usbinfo(self, ms_usb):
        info = USBInfo()
        pid_vid_regex = r"USB\\VID_([a-zA-z0-9]{4})&PID_([a-zA-z0-9]{4})"
        p = re.compile(pid_vid_regex)
        m = p.match(ms_usb.DeviceID)
        info.vid = m.group(1)
        info.pid = m.group(2)
        return info

    def _start_usb_monitor(self, sql, callback):
        if sys.platform == "win32":
            pythoncom.CoInitialize()
            c = wmi.WMI()
            watcher = c.watch_for(raw_wql=sql)
            logging.info("Starting usb watcher")
            self.running = True
            while self.running:
                try:
                    usb = watcher(timeout_ms=100)
                    if usb is not None:
                        if callback is not None:
                            callback(self._create_usbinfo(usb))
                        break
                except wmi.x_wmi_timed_out:
                    pass
                except KeyboardInterrupt:
                    self.running = False
            pythoncom.CoUninitialize()
        else:
            pass

    def _start_usb_monitor_connect(self):
        raw_wql = "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"  # noqa: E501
        self._start_usb_monitor(raw_wql, self.on_connect)

    def _start_usb_monitor_disconnect(self):
        raw_wql = "SELECT * FROM __InstanceDeletionEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"  # noqa: E501
        self._start_usb_monitor(raw_wql, self.on_disconnect)


if __name__ == "__main__":
    def cb(info):
        print(f"Got usb event: {info}")
    mon = USBMonitor(cb, cb)
    import time
    for i in range(0, 15):
        print(i)
        time.sleep(1)
    mon.stop()
