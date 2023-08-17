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
    def get_char(self, k):
        '''Convert KeyCodes to readable string'''
        try:
            # Try to get the character of the key directly
            pressed_key = str(k.char)
            # Key combos with control
            if self.last_key == " |ctrl| " or self.last_key == " |steuerung| " or "ombo " in self.last_key: # noqa: 501
                if self.last_key == " |ctrl| ":
                    self.log = self.log[:-7]
                if self.last_key == " |steuerung| ":
                    self.log = self.log[:-13]
                # Select all
                if pressed_key == "\u0001":
                    return self.locale.translate("combo_select_all")
                # Copy
                if pressed_key == "\u0003":
                    return self.locale.translate("combo_copy")
                # Insert
                if pressed_key == "\u0016":
                    return self.locale.translate("combo_insert")
                # Undo
                if pressed_key == "\u001a":
                    return self.locale.translate("combo_undo")
            # Uppercase letter, remove shift for easier readability
            if self.last_key == " |shift| ":
                self.log = self.log[:-9]
            return pressed_key
        except AttributeError:
            # Cut out 'Key.' and '_l' or '_r' from KeyCode string
            if "_l" in str(k) or "_r" in str(k):
                try:
                    return self.key_translation_dict[str(k)[4:-2]]
                except Exception:
                    return (" " + str(k)[4:-2] + " ")
            else:
                try:
                    return self.key_translation_dict[str(k)[4:]]
                except Exception:
                    return (" " + str(k)[4:] + " ")

    # Logging function
    def on_press(self, k):
        '''For Keylogger'''
        c = str(self.get_char(k))
        self.last_key = c
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

        self.last_key = ""

        self.locale = locale

        # Add missing keys
        self.keys = ["tab", "enter", "shift", "steuerung",
                     "windows", "escape", "alt", "home", "caps",
                     "backspace"]

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
            "caps_lock": self.locale.translate("key_caps_lock"),
            "backspace": self.locale.translate("key_backspace")}
        self.listener.start()

        self.stop_event.wait()

        # Insert special characters denoting end of user input
        self.log = self.log + "\n\nINJECTED KEYSTROKES\n\n"
        self.listener.stop()

        # Add injected keystroke part to log

        self.log = self.log + self.key_translation_dict["ctrl"] + self.key_translation_dict["shift"] + "j " # noqa: 501

        for func in self.js_function_names:
            self.log = self.log + f"{func}()"
            self.log = self.log + self.key_translation_dict["enter"] # noqa: 501

        self.log = self.log + self.key_translation_dict["ctrl"] + self.key_translation_dict["shift"] + "j " # noqa: 501

        # Beautify log by substituting multiple presses of same key
        for k in self.keys:
            # Old syntax because of regex
            occurances = len(re.findall(r"( \|%s\| )" % (k), self.log))
            self.log = re.sub(r"( \|%s\| ){2,}" % (k), " {0}x|{1}| ".format(occurances, k), self.log) # noqa: 501

        # Split log for request from site
        self.your_keystrokes = self.log.split(
            "\n\nINJECTED KEYSTROKES\n\n")[0]
        self.injected_keystrokes = self.log.split(
            "\n\nINJECTED KEYSTROKES\n\n")[1]

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

    # Simulates key sequences
    def press_keys(self, keys, delay_between_sec, delay_after_sec):
        for key in keys:
            if type(key) is not str: # noqa: 721
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
            if type(key) is not str: # noqa: 721
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
            if type(key) is not str: # noqa: 721
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
        self.simultaneous_press_keys([Key.ctrl, Key.shift, "j"], 2)

        # Scroll to end text
        self.press_keys([Key.space, Key.space], 2, 0.25)


if __name__ == "__main__":
    demo = Keylog_Simulation()
    demo._run()
