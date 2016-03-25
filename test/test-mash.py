import subprocess
import logging
from gi.repository import Clutter, Mx, Mash, Toggle, Cogl, GObject

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')


Clutter.init(None)
model = Toggle.Model()
#print "cube"
#model.load_from_file(0, "/home/root/.octoprint/uploads/25mm_cube.stl")
#print "hollow cube"
#model.load_from_file(0, "/home/root/.octoprint/uploads/20mm_hollow_cube.stl")
model.load_from_file(0, "/home/root/.octoprint/uploads/reel2.stl")

