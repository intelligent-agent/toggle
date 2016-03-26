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

    model = Toggle.Box()
    #model.load_from_file(0, "/home/root/.octoprint/uploads/reel2.stl")
    model.set_position(400, 200)
    stage.add_child(model)

    stage.show_all()
    Clutter.main()

