import sys
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QLabel,
                             QPushButton,
                             QVBoxLayout,
                             )
from PyQt5.QtGui import QPixmap, QCursor, QFont
from PyQt5 import QtCore
import keyboard
from random import choice, randint
import threading
import time
import queue
import urllib.request
import pathlib
import logging

from nativeapp.utils.locale import locale
from nativeapp.config import config


class KillState():
    NONE = 0
    GLITCH = 1
    CRASH = 2
    INSTRUCTIONS = 3


KEYS_TO_BLOCK = keyboard.all_modifiers


class KillSimulation():
    def __init__(self):
        self.time_to_crash = 5
        self.gui_thread = threading.Thread(target=self._run)
        self.gui_thread.start()
        self.state_queue = queue.Queue()

    def _run(self):
        self.app = QApplication(sys.argv)
        self.geometry = self.app.desktop().screenGeometry()
        self.running = True
        self.glitch = Glitch(self.geometry.width(), self.geometry.height())
        self.glitch.hide()

        # Crash fullscreen black widget
        self.crash = Crash(self.geometry.width(), self.geometry.height())
        self.crash.hide()

        self.gui_loop()

    def show_glitch(self):
        self.state_queue.put(KillState.GLITCH)

    def show_crash(self):
        self.state_queue.put(KillState.CRASH)

    def show_crash_text(self):
        self.state_queue.put(KillState.INSTRUCTIONS)

    def gui_loop(self):
        while self.running:
            if not self.state_queue.empty():
                next_state = self.state_queue.get()
                if next_state == KillState.NONE:
                    self.glitch.hide()
                    self.crash.hide()
                elif next_state == KillState.GLITCH:
                    self.glitch.show()
                    self.crash.hide()
                elif next_state == KillState.CRASH:
                    self.glitch.hide()
                    self.crash.show()
                    # Block specific keys (f.e. alt-tabbing)
                    for key in KEYS_TO_BLOCK:
                        try:
                            keyboard.block_key(key)
                        except ValueError as e:
                            logging.warning(f"Unable to hook key {key}: {e}")
                elif next_state == KillState.INSTRUCTIONS:
                    self.glitch.hide()
                    self.crash.show()
                    self.crash.show_button()
                    keyboard.unhook_all()
            self.app.processEvents()
            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.gui_thread.join()


class Glitch(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.title = 'Demo'
        self.left = 0
        self.top = 0
        self.width = width
        self.height = height
        # Set how many glitches should appear
        self.num_glitches = 500
        # Set to true to allow Glitches to overlap
        self.overlap = False

        # Overlapping parameter
        # for how much overlapping is allowed if overlap = False
        # Accepted Values are 50 for no overlapping and
        # 0 for entire overlapping
        self.overlap_param = 50

        # Time until backscreen is displayed in seconds
        self.time_to_crash = 5

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Window on top and frameless
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # Hide task symbol
        self.setWindowFlag(QtCore.Qt.ToolTip)

        # Invisible mouse
        self.setCursor(QtCore.Qt.BlankCursor)

        # Transparent background
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Stretch image to full screen
        self.setContentsMargins(0, 0, 0, 0)

        # Collect the five different Glitch Textures
        glitches = []
        file_dir = pathlib.Path(__file__).parent / "resources"
        for i in range(1, 6):
            glitch_img_path = file_dir / f"glitch_cc_{i}.png"
            logging.info(f"{glitch_img_path=} {glitch_img_path.exists()=}")
            glitches.append(QPixmap(str(glitch_img_path)))

        # Overlapping is allowed,
        # so no worries about two glitches at the same position
        if self.overlap:
            for i in range(self.num_glitches):
                label = QLabel(self)
                label.setPixmap(choice(glitches))
                label.setGeometry(QtCore.QRect(randint(0, self.width - 50),
                                  randint(0, self.height - 50), 50, 50))

        # Overlapping is not allowed,
        # positions and their neighbourhood can only be taken once
        else:
            # Positions glitches choose one from
            not_yet_glitched_x = [k + self.overlap_param for k in
                                  range(-self.overlap_param,
                                        self.width - self.overlap_param,
                                        self.overlap_param)]
            not_yet_glitched_y = [k + self.overlap_param for k in
                                  range(-self.overlap_param,
                                        self.height - self.overlap_param,
                                        self.overlap_param)]
            for i in range(self.num_glitches):
                # If there are no more positions available
                # break (no more glitches can be displayed)
                if not_yet_glitched_x != []:
                    label = QLabel(self)
                    label.setPixmap(choice(glitches))
                    x = choice(not_yet_glitched_x)
                    y = choice(not_yet_glitched_y)
                    # Remove positions only from x because x is larger than y
                    not_yet_glitched_x.remove(x)
                    label.setGeometry(QtCore.QRect(x, y, 50, 50))
                else:
                    break

        self.show()


class Crash(QWidget):

    def __init__(self, width, height):
        super().__init__()
        self.title = 'Demo'
        self.left = 0
        self.top = 0
        self.width = width
        self.height = height
        localedir = pathlib.Path(__file__).parent.parent / "locales"
        self.elite_locale = locale.Locale(localedir)
        self.elite_locale.update_locale(config.EnvironmentConfig.LANGUAGE)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Window on top and frameless
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # Hide task symbol
        self.setWindowFlag(QtCore.Qt.ToolTip)

        # Invisible mouse
        self.setCursor(QtCore.Qt.BlankCursor)

        self.setStyleSheet("background-color: black;")

        font = QFont("Montserrat,Helvetica,Arial,serif", 40)

        # Demo End Text
        self.btn = QPushButton(self.elite_locale.translate("end_demo_text"))
        self.btn.setStyleSheet("Background-color: #7367f0; color: white; font-weight: bold; border-radius: 25px;") # noqa: 501
        self.btn.setMinimumWidth(self.width // 2)
        self.btn.setMinimumHeight(self.height // 4)
        self.btn.setFont(font)
        self.btn.hide()

        def stop_demo():
            PROTOCOL = "http"
            HOST = "127.0.0.1:5000"
            PATH = "orchestration/stop/demo/uhh_usb_kill"

            self.hide()
            urllib.request.urlopen(f"{PROTOCOL}://{HOST}/{PATH}")  # nosec
        self.btn.clicked.connect(stop_demo)

        self.text = QLabel()
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setWordWrap(True)
        self.text.setText(self.elite_locale.translate("uhh_crash_text"))

        self.text.setFont(font)
        self.text.setStyleSheet("color: white;")
        self.text.hide()

        layout = QVBoxLayout()

        layout.addWidget(self.text)
        layout.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(layout)

    def show_button(self):
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.text.show()
        self.btn.show()


if __name__ == "__main__":
    kill_test = KillSimulation()
    print("Showing glitch")
    kill_test.show_glitch()
    time.sleep(10)
    print("Crash")
    kill_test.show_crash()
    time.sleep(10)
    print("Crash text")
    kill_test.show_crash_text()
    time.sleep(10)
    kill_test.stop()
