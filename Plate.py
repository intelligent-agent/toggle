# Plate

from gi.repository import Clutter, Mx, Mash, Toggle

class Plate(Toggle.Plate):
    def __init__(self):
        super(Plate, self).__init__()
        self.set_reactive(True)
        self.connect("button-press-event", self.click)

    def click(self):
        print "Plate clicked"
        
