# Plate

from gi.repository import Clutter, Mx, Mash, Toggle

class Plate(Toggle.Plate):
    def __init__(self, ui):
        super(Plate, self).__init__()
        self.ui = ui
        # I want to subclass this, but I'm uncertain how to..
        self.p = ui.get_object("plate")
        self.p.load_from_file(0, "/etc/toggle/platforms/thing.ply")
        self.p.set_color(Clutter.Color.from_string("#555A")[1])
        self.p.set_reactive(True)
        #ui.get_object("stage").connect("motion-event", self.move)

        #Set up the light
        light_set = Mash.LightSet()
        light_point = Mash.PointLight()
        light_directional = Mash.DirectionalLight()
        light_spot = Mash.SpotLight()

        # Add the model the lights to the volume viewport
        self.p.add_child(light_point);
        self.p.add_child(light_directional);
        self.p.add_child(light_spot);

    def click(self):
        print "Plate clicked"

    def move(self, actor, event):
        vs = self.ui.get_object("volume-stage")
        vs.set_rotation_angle(Clutter.RotateAxis.X_AXIS, event.x)
        vs.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, event.y)
