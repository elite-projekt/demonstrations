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
import sys
import logging
import threading

if sys.platform == "win32":
    import pythoncom
    import wmi


class USBMonitor:
    def __init__(self, on_connect):
        self.running = False
        self.on_connect = on_connect
        self.usb_thread = threading.Thread(target=self._start_usb_monitor)
        self.usb_thread.start()

    def stop(self):
        self.running = False
        logging.info("Waiting for USB thread")
        if self.usb_thread is not None and self.usb_thread.is_alive():
            self.usb_thread.join()

    def _start_usb_monitor(self):
        if sys.platform == "win32":
            pythoncom.CoInitialize()
            raw_wql = "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"  # noqa: E501
            c = wmi.WMI()
            watcher = c.watch_for(raw_wql=raw_wql)
            logging.info("Starting usb watcher")
            self.running = True
            while self.running:
                try:
                    usb = watcher(timeout_ms=100)
                    if usb is not None:
                        if self.on_connect is not None:
                            self.on_connect()
                        break
                except wmi.x_wmi_timed_out:
                    pass
                except KeyboardInterrupt:
                    self.running = False
            pythoncom.CoUninitialize()
        else:
            pass
