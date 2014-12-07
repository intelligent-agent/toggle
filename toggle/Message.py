# Display a message. 
from gi.repository import Clutter, Mx, Mash, Toggle

class Message:
    def __init__(self, config):
        self.ui = config.ui
        self.msg = config.ui.get_object("msg")
        self.msg.save_easing_state()
        self.msg.set_easing_duration (500)
        self.txt = config.ui.get_object("txt")
        self.fade = Clutter.Timeline.new(2000)
        self.fade.connect("completed", self.remove)

    def display(self, text):
        self.txt.set_text(text)
        self.txt.set_x(400-self.txt.get_width()/2)
        self.msg.set_opacity(255)
        self.fade.start()

    def remove(self, event):
        self.msg = self.ui.get_object("msg")
        self.msg.set_opacity(0)

