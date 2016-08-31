# Plate

from gi.repository import Clutter, Mx, Mash, Toggle
import logging
import math
from operator import attrgetter

class Plate(Toggle.Model):
    def __init__(self, config):
        super(Plate, self).__init__()
        self.config = config
        # I want to subclass this, but I'm uncertain how to..
        self.plate = self.config.ui.get_object("plate")
        self.plate.load_from_file(0, config.get("System", "plate"))
        self.plate.set_specular(Clutter.Color.from_string("#0000")[1])
        self.plate.set_color(Clutter.Color.from_string("#555F")[1])

        # Position it
        (width, height) = self.plate.get_size()
        depth = self.plate.get_model_depth() # Custom method
        self.plate.set_y(depth/2.0)
        self.plate.set_x(-width/2.0)
        self.plate.set_z_position(height/2.0)

        self.plate.set_light_set(self.config.loader.model.light_set)

        self.probe_points = []
        self.scale_points = []
        #self.plate.set_progress(100.0)
        self.plate.set_culling(1)

    def add_probe_point(self, point):
        self.point = self.add_point_to_bed(point)
        self.recalculate_scale()
        self.recolor_points_to_scale()


    def add_point_to_bed(self, point):
        probe = Toggle.Model()
        probe.load_from_file(0, self.config.get("System", "probe-point"))

        probe.set_size(10, 10)
        (width, height) = probe.get_size()
        depth = probe.get_model_depth() # Custom method

        probe.set_y(depth/2.0-point[2])
        probe.set_x(-width/2.0+point[0])
        probe.set_z_position(height/2.0+point[1])
        probe.z = point[2] # Store z-value for rescaling

        probe.set_light_set(self.config.loader.model.light_set)
        probe.set_rotation_angle(Clutter.RotateAxis.X_AXIS, -90.0)
        self.config.ui.get_object("model-flipper").add_actor(probe)
        self.probe_points.append(probe)


    def add_point_to_scale(self, point):
        #logging.debug("Adding point to scale")
        probe = Toggle.Model()
        probe.load_from_file(0, self.config.get("System", "probe-point"))
        probe.z = point[2]

        probe.set_size(30, 30)
        probe.set_x(point[0])
        probe.set_y(point[1])

        probe.set_rotation_angle(Clutter.RotateAxis.X_AXIS, 90.0)
        self.config.ui.get_object("side2-content").insert_child_above(probe)

        text = Clutter.Text.new_with_text("Sans 10", str(point[2]))
        text.set_x(point[0]-50)
        text.set_y(point[1]-10)
        self.config.ui.get_object("side2-content").insert_child_above(text)
        probe.text = text
        text.hide()

        self.scale_points.append(probe)

    def recolor_points_to_scale(self):
        ''' Update probe point color to maximize scale '''
        self.cmax = max(self.probe_points, key=attrgetter('z')).z
        self.cmin = min(self.probe_points, key=attrgetter('z')).z
        for point in self.probe_points:
            color = self.float_rgb(point.z, self.cmin, self.cmax)
            point.set_color(Clutter.Color.from_string(color)[1])

    def remove_probe_points(self):
        ''' Remove all probe points '''
        for point in self.probe_points:
            self.config.ui.get_object("model-flipper").remove_child(point)
        self.probe_points = []
        for point in self.scale_points:
            point.text.hide()
            point.hide()


    def float_rgb(self, mag, cmin, cmax):
        """ Return a tuple of floats between 0 and 1 for R, G, and B. """
        """ Taken from https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch09s11.html """
        # Normalize to 0-1
        try:
            x = self.rescale(float(mag), cmin, cmax, 0.0, 1.0)#float(mag-cmin)/(cmax-cmin)
        except ZeroDivisionError:
            x = 0.5 # cmax == cmin
        blue = max(0, (1.0 - 2*x))*0xFF
        red =  max(0, (2*x - 1.0))*0xFF
        green = 0xFF - blue - red
        color = "#%02x%02x%02xFF" % (red, green, blue)
        return color


    def make_scale(self):
        pass
        #for z in range(11):
        #    self.add_point_to_scale([150, z*20+150, 0])

    def recalculate_scale(self):
        cmax = max(self.probe_points, key=attrgetter('z')).z
        cmin = min(self.probe_points, key=attrgetter('z')).z
        for i, point in enumerate(self.scale_points):
            x  = self.rescale(float(i), 0.0, float(len(self.scale_points)-1), cmin, cmax)
            color = self.float_rgb(x, cmin, cmax)
            point.set_color(Clutter.Color.from_string(color)[1])
            point.text.set_text("{: .2f}".format(x))
            point.text.show()
            point.show()


    def rescale(self, val, in_min, in_max, out_min, out_max):
        return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))
