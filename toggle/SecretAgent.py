import NetworkManager
import logging
import gi
import time
gi.require_version('Clutter', '1.0')
from gi.repository import Clutter, Mx, GObject, GLib

class SecretAgent(NetworkManager.SecretAgent):
    ID = 'no.iagent.secret-agent'

    def __init__(self, config):
        self.config = config
        super(SecretAgent, self).__init__(SecretAgent.ID)

        ok_tap = Clutter.TapAction()
        config.ui.get_object("wifi-ok").add_action(ok_tap)
        ok_tap.connect("tap", self.ok_button_tap)
        cancel_tap = Clutter.TapAction()
        config.ui.get_object("wifi-cancel").add_action(cancel_tap)
        cancel_tap.connect("tap", self.cancel_button_tap)
        self.wifi_password = ""

    def GetSecrets(self, settings, connection, setting_name, hints, flags):
        self.request_con = connection
        self.request_settings = settings
        self.make_keyboard()
        self.show_keyboard()
        # We show the keyboard here and assume we are sending back a
        # faulty password. The Connection will be updated on "OK" press.
        return { setting_name: { 'psk': self.wifi_password} }

    def show_keyboard(self):
        self.config.ui.get_object("wifi-input").set_text(self.wifi_password)
        self.config.ui.get_object("wifi-overlay").show()

    def ok_button_tap(self, tap, actor):
        self.wifi_password = self.config.ui.get_object("wifi-input").get_text()
        self.config.ui.get_object("wifi-overlay").hide()
        self.request_settings['802-11-wireless-security']["psk"] = self.wifi_password
        self.request_con.Update(self.request_settings)
        self.config.settings.reconnect_last_ap()

    def cancel_button_tap(self, tap, actor):
        self.config.ui.get_object("wifi-overlay").hide()

    def set_wifi_status(self, text):
        self.config.ui.get_object("wifi-status").set_text(text)

    def make_keyboard(self, keyset=0):
        # yapf: disable
        keys = [[["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", " ⌫ "],
               ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
               ["z", "x", "c", "v", "b", "n", "m", ",", "."],
               [" ?123 ", "                                        ", " ABC "]
               ],
              [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ⌫ "],
               ["=", "-", "+", "*", "/", "\\", ":", ";", "'", "\""],
               ["(", ")", "#", "$", "!", "?", "@", "_", ",", "."],
               [" ABC ", "                                        ", " abc "]
               ],
              [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", " ⌫ "],
               ["A", "S", "D", "F", "G", "H", "J", "K", "L", "'"],
               ["Z", "X", "C", "V", "B", "N", "M", ",", "."],
               [" abc ", "                                        ", " ?123 "]
               ]]
        # yapf: enable
        for i, row in enumerate(keys[keyset]):
          key_row = self.config.ui.get_object("row-" + str(i))
          key_row.remove_all_children()
          for letter in row:
            key = Mx.Button()
            key.set_style_class("keyboard")
            key.set_label(letter)
            key.letter = letter
            key_row.add_actor(key)
            tap = Clutter.TapAction()
            key.add_action(tap)
            tap.connect("tap", self.keyboard_tap)

    def keyboard_tap(self, tap, actor):
        self.wifi_password = self.config.ui.get_object("wifi-input").get_text()
        if actor.letter == " ⌫ ":
          self.wifi_password = self.wifi_password[:-1]
        elif actor.letter == "                                        ":
          self.wifi_password += " "
        elif actor.letter == " ?123 ":
          self.make_keyboard(1)
        elif actor.letter == " ABC ":
          self.make_keyboard(2)
        elif actor.letter == " abc ":
          self.make_keyboard(0)
        else:
          self.wifi_password += actor.letter
        self.config.ui.get_object("wifi-input").set_text(self.wifi_password)

