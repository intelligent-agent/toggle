import subprocess
import logging
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')




if __name__ == '__main__':
    Clutter.init( None )

    stage = Clutter.Stage()
    stage.set_size(800, 500)
    stage.set_title('Clutter - Cairo content')
    stage.set_user_resizable(True)

    stage.connect("destroy", lambda w: Clutter.main_quit() )

    model = Toggle.Model()
    model.load_from_file(0, "/home/root/.octoprint/uploads/reel2.stl")
    model.set_color(Clutter.Color.from_string("#55A94BFF")[1])  
    model.set_position(400, 200)
    stage.add_child(model)


    #Set up the light
    light_set = Mash.LightSet()
    light_point = Mash.PointLight()
    light_directional = Mash.DirectionalLight()
    light_spot = Mash.SpotLight()

    light_set.add_light(light_point)
    light_set.add_light(light_directional)
    light_set.add_light(light_spot)

    # Add the model the lights to the volume viewport
    stage.add_child(light_point);
    stage.add_child(light_directional);
    stage.add_child(light_spot);

    model.set_light_set(light_set)

    stage.show_all()
    Clutter.main()

