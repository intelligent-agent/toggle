import subprocess
import logging
import gi
gi.require_version('Clutter', '1.0')
gi.require_version('Mx', '2.0')
gi.require_version('Mash', '0.3')
from gi.repository import Clutter, Mx, Mash, Cogl, GObject

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')




if __name__ == '__main__':
    Clutter.init( None )

    stage = Clutter.Stage()
    stage.set_size(800, 500)
    stage.set_title('Test Mash')
    stage.set_user_resizable(True)

    stage.connect("destroy", lambda w: Clutter.main_quit() )

    model = Mash.Model()
    model_data = Mash.Data()
    path = "models/suzanne.ply"
    model_data.load(0, path)
    model.set_data(model_data)
    model.set_color(Clutter.Color.from_string("#55A94BFF")[1])  
    model.set_position(400, 200)
    stage.add_child(model)

    stage.show_all()
    Clutter.main()

