# Plate

from gi.repository import Clutter, Mx, Mash

class Splash():
    def __init__(self, config):
        self.ui = config.ui
        splash = config.ui.get_object("splash")
        splash.set_from_file(config.get("System", "splash"))
        self.status = config.ui.get_object("splash-status")

    def set_status(self, status):
        self.status.set_text (status)

    def enable_next(self):
        next = self.ui.get_object("side5-btn-next")
        next.set_opacity(255)
        prev = self.ui.get_object("side5-btn-prev")
        prev.set_opacity(255)


