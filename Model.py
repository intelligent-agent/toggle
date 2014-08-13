# Model

from gi.repository import Clutter, Mx, Mash, Toggle

class Model(Toggle.Model):
    def __init__(self, ui):   
        super(Model, self).__init__()        
        self.load_from_file(0, "models/treefrog.ply")
        self.set_reactive(True)
        self.connect("button-press-event", self.click)
        self.connect("motion-event", self.move)
        self.connect("button-release-event", self.release)
        self.clicked = False
        self.last_x = 0
        self.last_y = 0

    def click(self, actor, event):
        self.last_x = event.x
        self.last_y = event.y
        self.clicked = True

    def release(self, actor, event):
        self.clicked = False

    def move(self, actor, event):
        delta_x = self.last_x-event.x
        delta_y = self.last_y-event.y
        print delta_x
        print delta_y
        if self.clicked:
            self.move_by(delta_x, delta_y)

        
