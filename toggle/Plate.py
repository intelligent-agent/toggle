# Plate

from gi.repository import Clutter, Mx, Mash, Toggle

class Plate(Toggle.Model):
    def __init__(self, config):
        super(Plate, self).__init__()
        self.ui = config.ui
        # I want to subclass this, but I'm uncertain how to..
        self.plate = self.ui.get_object("plate")        
        self.plate.load_from_file(0, config.get("System", "plate"))
        self.plate.set_specular(Clutter.Color.from_string("#0000")[1])
        self.plate.set_color(Clutter.Color.from_string("#555F")[1])

        # Position it
        (width, height) = self.plate.get_size()
        depth = self.plate.get_model_depth() # Custom method
        self.plate.set_y(depth/2.0)
        self.plate.set_x(-width/2.0)
        self.plate.set_z_position(height/2.0)


         #Set up the light
        self.light_set = Mash.LightSet()
        light_point = Mash.PointLight()
        light_directional = Mash.DirectionalLight()
        light_spot = Mash.SpotLight()
    
        self.light_set.add_light(light_point)
        self.light_set.add_light(light_directional)
        self.light_set.add_light(light_spot)

        # Add the model the lights to the volume viewport
        self.ui.get_object("volume-viewport").add_child(light_point);
        self.ui.get_object("volume-viewport").add_child(light_directional);
        self.ui.get_object("volume-viewport").add_child(light_spot);

        self.plate.set_light_set(self.light_set)
