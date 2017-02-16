import subprocess
import logging
import gi
gi.require_version('Clutter', '1.0')
gi.require_version('Mx', '1.0')
gi.require_version('Mash', '0.3')
gi.require_version('Toggle', '0.6')
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')




if __name__ == '__main__':
    Clutter.init( None )

    stage = Clutter.Stage()
    model = Toggle.Model()
    model.load_from_file(0, "/home/root/.octoprint/uploads/reel2.stl")
    model.get_z_min()
