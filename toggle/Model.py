# Model
import os.path
import logging
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl

class Model(Toggle.Model):
    def __init__(self, config, filename):   
        super(Model, self).__init__()    

        self.config = config        
        model = config.ui.get_object("model")
        self.filename = filename
        path = config.get("System", "model_folder")+"/"+filename
        if not os.path.isfile(path):
            logging.warning(path+" is not a file") 

        try:
            model.load_from_file(0, path)
            model.set_color(Clutter.Color.from_string("#55A94BFF")[1])  
        except:
            logging.warning("Unable to open model "+path)
            raise
            return    
        (width, height) = model.get_size()
        depth = model.get_model_depth() # Custom method
        model.set_y(depth/2.0)
        model.set_x(-width/2.0)
        model.set_z_position(height/2.0)

        #Set up the light
        self.light_set = Mash.LightSet()
        light_point = Mash.PointLight()
        light_directional = Mash.DirectionalLight()
        light_spot = Mash.SpotLight()
    

        self.light_set.add_light(light_point)
        self.light_set.add_light(light_directional)
        self.light_set.add_light(light_spot)

        # Add the model the lights to the volume viewport
        vp = config.ui.get_object("volume-viewport")
        vp.add_child(light_point);
        vp.add_child(light_directional);
        vp.add_child(light_spot);

        model.set_light_set(self.light_set)
