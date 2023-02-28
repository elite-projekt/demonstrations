# Custom imports for demo
from pynput.keyboard import Key, Listener, Controller
from pynput.mouse import Controller as Controller_ms
from pynput.mouse import Button
from keyboard import block_key, unblock_key, unhook_all
from time import sleep
import re
import string
import pyperclip


# Keylogger Demo Class
class Keylog_Simulation():

    # Helper for formatting logged keys
    def get_char(self, key):
        '''Convert KeyCodes to readable string'''
        try:
            # Try to get the character of the key directly
            return key.char
        except AttributeError:
            # Cut out 'Key.' and '_l' or '_r' from KeyCode string
            if "_l" in str(key) or "_r" in str(key):
                try:
                    return self.key_translation_dict[str(key)[4:-2]]
                except Exception:
                    return (" " + str(key)[4:-2] + " ")
            else:
                try:
                    return self.key_translation_dict[str(key)[4:]]
                except Exception:
                    return (" " + str(key)[4:] + " ")

    # Logging function
    def on_press(self, key):
        '''For Keylogger'''
        c = str(self.get_char(key))
        self.log = self.log + c

    def __init__(self, stop_event, locale):
        self.kb = Controller()
        self.log = ""
        self.listener = Listener(on_press=self.on_press)
        self.stop_event = stop_event
        self.js_function_names = ["Hack", "Now", "Complete"]
        # Tracks if the injection should be triggered
        self.inject = False
        self.key_translation_dict = {}

        self.locale = locale

        # Add missing keys
        self.keys = [["tab", "enter", "shift", "steuerung",
                      "windows", "escape", "alt", "home", "caps"]]

    def execute(self):
        self.inject = True
        self.stop_event.set()

    def _run(self):
        self.key_translation_dict = {
            "tab": self.locale.translate("key_tab"),
            "enter": self.locale.translate("key_enter"),
            "shift": self.locale.translate("key_shift"),
            "ctrl": self.locale.translate("key_ctrl"),
            "cmd": self.locale.translate("key_cmd"),
            "space": self.locale.translate("key_space"),
            "esc": self.locale.translate("key_esc"),
            "alt": self.locale.translate("key_alt"),
            "home": self.locale.translate("key_home"),
            "caps_lock": self.locale.translate("key_caps_lock")}
        self.listener.start()

        self.stop_event.wait()

        # Insert special characters denoting end of user input
        self.log = self.log + "\n\nINJECTED KEYSTROKES\n\n"
        if self.inject:
            # Block characters of the alphabet
            for key in string.ascii_lowercase:
                block_key(key)
            # Block special characters needed
            for key in ["(", ")", ".", "!", "?", "|", "_", "-", ","]:
                block_key(key)
            # Block special keys
            for key in [Key.alt, Key.alt_gr, Key.backspace, Key.caps_lock,
                        Key.cmd, Key.ctrl, Key.delete, Key.down, Key.end,
                        Key.enter, Key.esc, Key.f1, Key.home, Key.insert,
                        Key.left, Key.menu, Key.num_lock, Key.right,
                        Key.shift, Key.space, Key.tab, Key.up]:
                block_key(key.name)
            self.keystroke_injection()
            unhook_all()
        else:
            self.listener.stop()

    # Simulates key sequences
    def press_keys(self, keys, delay_between_sec, delay_after_sec):
        for key in keys:
            if type(key) != str:
                key_name = key.name
            else:
                # Replace special keys
                if key == " ":
                    key = Key.space
                    key_name = "space"
                elif key == "\n":
                    key = Key.enter
                    key_name = "enter"
                else:
                    key = key.lower()
                    key_name = key
            unblock_key(key_name)
            sleep(delay_between_sec)
            self.kb.press(key)
            self.kb.release(key)
            sleep(delay_between_sec)
            block_key(key_name)
            sleep(delay_between_sec)
        sleep(delay_after_sec)

    # Simulates pressing keys at once
    def simultaneous_press_keys(self, keys, delay_after_sec):
        for key in keys:
            if type(key) != str:
                key_name = key.name
            else:
                # Replace special keys
                if key == " ":
                    key = Key.space
                    key_name = "space"
                elif key == "\n":
                    key = Key.enter
                    key_name = "enter"
                else:
                    key = key.lower()
                    key_name = key
            unblock_key(key_name)
            self.kb.press(key)
        for key in keys:
            if type(key) != str:
                key_name = key.name
            else:
                # Replace special characters
                if key == " ":
                    key = "space"
                elif key == "\n":
                    key = Key.enter
                    key_name = "enter"
                else:
                    key = key.lower()
                    key_name = key
            self.kb.release(key)
            block_key(key_name)
        sleep(delay_after_sec)

    def __click_console(self):
        mouse = Controller_ms()
        old_pos = mouse.position
        mouse.position = (1700, 500)
        mouse.click(Button.left, 1)
        mouse.position = old_pos

    # Keystroke injection
    def keystroke_injection(self):

        # Open Browser Console
        self.simultaneous_press_keys([Key.ctrl, Key.shift, "j"], 5)

        # Execute Javascript functions
        for func in self.js_function_names:
            self.__click_console()
            pyperclip.copy(f"{func}()")
            self.simultaneous_press_keys([Key.ctrl, "v"], 0.25)
            self.press_keys([Key.enter], 0, 0.25)

        # Close Browser Console
        self.simultaneous_press_keys([Key.ctrl, Key.shift, "j"], .5)

        # Stop listening for keystrokes
        self.listener.stop()

        # Beautify log by substituting multiple presses of same key
        for k in self.keys:
            # Old syntax because of regex
            occurances = len(re.findall(r"( \|%s\| )" % (k), self.log))
            self.log = re.sub(r"( \|%s\| ){2,}" % (k), " {0}x|{1}| ".format(occurances, k), self.log) # noqa: 501

        self.your_keystrokes = self.log.split(
            "\n\nINJECTED KEYSTROKES\n\n")[0]
        self.injected_keystrokes = self.log.split(
            "\n\nINJECTED KEYSTROKES\n\n")[1]

        # End text
        self.end_text = self.locale.translate(
            "uhh_keylogger_end_text").split("\n")

        # Show logged Keys
        self.press_keys([Key.tab], 0.25, 0.25)
        pyperclip.copy(self.your_keystrokes)
        self.simultaneous_press_keys([Key.ctrl, "v"], 0.25)
        self.press_keys([Key.tab], 0.25, 0.25)
        pyperclip.copy(self.injected_keystrokes)
        self.simultaneous_press_keys([Key.ctrl, "v"], 0.25)
        self.press_keys([Key.tab], 0.25, 0.25)

        for sentence in self.end_text:
            pyperclip.copy(sentence)
            self.simultaneous_press_keys([Key.ctrl, "v"], 0.15)
            self.press_keys([Key.enter], 0, 0.15)


if __name__ == "__main__":
    demo = Keylog_Simulation()
    demo._run()
