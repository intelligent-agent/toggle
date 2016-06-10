# Model
import os.path
import logging
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl

class Model(Toggle.Model):
    def __init__(self, config):   
        super(Model, self).__init__()    

        self.config = config        
        self.model = config.ui.get_object("model")
        color_str = config.get("System", "model-color")
        self.color = Clutter.Color.from_string(color_str)[1]
        self.model.set_color(self.color)

        self.loader = config.ui.get_object("loader")
        self.loader.set_from_file(config.get("System", "loader"))
  
        self.t = Clutter.PropertyTransition(property_name='rotation-angle-z')
        self.t.set_from(0)
        self.t.set_to(360)
        self.t.set_duration(3000)
        self.t.set_animatable(self.loader)
        self.t.set_repeat_count(-1)
        self.t.start()

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

        self.model.connect("show", self.model_loaded)
        cm = Cogl.Matrix()
        m = Clutter.matrix_init_from_array(cm, [
             1, 0, 0, 0,   
             0, 1, 0, 0,
             0, 0, 1, 0, 
             0, 0, 0, 1])
        mf = config.ui.get_object("model-flipper")
        mf.set_transform(m)

        self.model.set_light_set(self.light_set)

    # Load model is a fairly CPU intensive 
    # operation on complex models. On BBB it can take several seconds to load
    # Treefrog or Benchy etc. It would therefore be better to have the 
    # data loading happen in a separate thread, so that the loading icon can be 
    # shown uninterrupted. UI operations must then be separated out, since they 
    # are required to run in the min thread.   
    def load_model(self, filename):
        self.model.hide()
        self.filename = filename
        path = self.config.get("System", "model_folder")+"/"+filename
        if not os.path.isfile(path):
            logging.warning(path+" is not a file")
        try:
            self.model.load_from_file(0, path)
            self.model.set_color(self.color)
        except:
            logging.warning("Unable to open model "+path)
            raise
            return    
        (width, height) = self.model.get_size()
        depth = self.model.get_model_depth() # Custom method
        self.model.set_y(depth/2.0)
        self.model.set_x(-width/2.0)
        self.model.set_z_position(height/2.0)
        self.model.show()

    # Hide the spinner/loader when done.  
    def model_loaded(self, model):
        self.loader.hide()

    def select_none(self):
        self.loader.hide()
        self.model.hide()
        

