# Plate

from gi.repository import Clutter, Mx, Mash, Toggle

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
